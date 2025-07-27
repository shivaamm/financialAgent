import os
import uuid
import json
import logging
import requests
import csv
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from collections import Counter, defaultdict

# It's good practice to move shared models to a central file (e.g., models.py) in the future.
# For now, we define the necessary models here to avoid circular imports with server.py.

class ReceiptItem(BaseModel):
    name: str
    price: float
    quantity: int = 1

class Receipt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    merchant_name: str
    total_amount: float
    date: datetime
    items: List[ReceiptItem]
    category: str
    image_base64: str
    analysis_text: str
    insights: List[str] = []
    savings_suggestions: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = "manual"

class NutritionalSummary(BaseModel):
    total_calories: float = 0
    total_protein: float = 0
    total_carbs: float = 0
    total_fat: float = 0
    total_fiber: float = 0
    item_count: int = 0

    def formatted_dict(self):
        return {
            "total_calories": f"{self.total_calories:.2f}",
            "total_protein": f"{self.total_protein:.2f}",
            "total_carbs": f"{self.total_carbs:.2f}",
            "total_fat": f"{self.total_fat:.2f}",
            "total_fiber": f"{self.total_fiber:.2f}",
            "item_count": self.item_count
        }

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the path to emergentintegrations if it's in backend/emergentintegrations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "emergentintegrations"))
from emergentintegrations.llm.chat import LlmChat, UserMessage

def filter_grocery_items(receipts: List[Receipt]) -> List[ReceiptItem]:
    """Filter grocery items from receipts, ensuring uniqueness by item name."""
    grocery_items = []
    seen = set()
    for receipt in receipts:
        if isinstance(receipt.category, str) and "grocery" in receipt.category.lower():
            for item in receipt.items:
                key = (item.name.lower(), item.price)
                if key not in seen:
                    grocery_items.append(item)
                    seen.add(key)
    return grocery_items

def fetch_nutritional_data(item_name: str) -> Dict[str, Any]:
    """Fetch nutritional data for a grocery item using cache, fallback to USDA API."""
    cache_path = os.path.join(os.path.dirname(__file__), 'nutrition_cache.csv')
    # Try cache first
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cache[row['item'].lower()] = row
    item_key = item_name.lower()
    if item_key in cache:
        row = cache[item_key]
        return {
            'item': item_name,
            'protein': float(row.get('protein', 0)),
            'fiber': float(row.get('fiber', 0)),
            'carbs': float(row.get('carbs', 0)),
            'fat': float(row.get('fat', 0)),
            'calories': float(row.get('calories', 0)),
        }
    # If not in cache, use USDA API
    api_key = os.getenv("USDA_API_KEY")
    if not api_key:
        logger.warning("USDA_API_KEY not found. Nutritional data will be zero.")
        return {"item": item_name, "protein": 0, "fiber": 0, "carbs": 0, "fat": 0, "calories": 0}
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": item_name,
        "pageSize": 1,
        "api_key": api_key
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if "foods" in data and len(data["foods"]) > 0:
                food = data["foods"][0]
                nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food.get("foodNutrients", [])}
                result = {
                    "item": item_name,
                    "protein": nutrients.get("Protein", 0),
                    "fiber": nutrients.get("Fiber, total dietary", 0),
                    "carbs": nutrients.get("Carbohydrate, by difference", 0),
                    "fat": nutrients.get("Total lipid (fat)", 0),
                    "calories": nutrients.get("Energy", 0)
                }
                # Write to cache
                fieldnames = ["item", "protein", "fiber", "carbs", "fat", "calories"]
                write_header = not os.path.exists(cache_path)
                with open(cache_path, 'a', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    if write_header:
                        writer.writeheader()
                    writer.writerow(result)
                return result
        else:
            logger.error(f"USDA API error: {resp.status_code} - {resp.text}")
    except Exception as e:
        logger.error(f"Error fetching nutritional data for {item_name}: {e}")
    return {"item": item_name, "protein": 0, "fiber": 0, "carbs": 0, "fat": 0, "calories": 0}

def calculate_nutritional_summary(receipts: List[Receipt]) -> NutritionalSummary:
    """Calculate the nutritional summary for a list of receipts."""
    summary = NutritionalSummary()
    grocery_items = filter_grocery_items(receipts)
    for item in grocery_items:
        nutritional_data = fetch_nutritional_data(item.name)
        if nutritional_data:
            summary.total_calories += nutritional_data.get("calories", 0) * item.quantity
            summary.total_protein += nutritional_data.get("protein", 0) * item.quantity
            summary.total_carbs += nutritional_data.get("carbs", 0) * item.quantity
            summary.total_fat += nutritional_data.get("fat", 0) * item.quantity
            summary.total_fiber += nutritional_data.get("fiber", 0) * item.quantity
            summary.item_count += item.quantity
    return summary

def analyze_purchase_history(receipts_csv_path: str = None) -> Dict[str, Any]:
    """
    Analyze user's purchase history from receipts.csv for personalization.
    Returns most frequent items, categories, and spending trends.
    """
    if receipts_csv_path is None:
        receipts_csv_path = os.path.join(os.path.dirname(__file__), 'firestore_exports', 'receipts.csv')
    items_counter = Counter()
    categories_counter = Counter()
    monthly_spending = defaultdict(float)
    if not os.path.exists(receipts_csv_path):
        return {}
    with open(receipts_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get('category', 'Unknown')
            categories_counter[category] += 1
            try:
                total = float(row.get('total_amount', 0))
            except Exception:
                total = 0
            date_str = row.get('date') or row.get('created_at')
            if date_str:
                month = date_str[:7]  # YYYY-MM
                monthly_spending[month] += total
            # Parse items field
            items_str = row.get('items', '')
            try:
                items_list = eval(items_str) if items_str else []
                for item in items_list:
                    name = item.get('name') if isinstance(item, dict) else None
                    if name:
                        items_counter[name] += item.get('quantity', 1) if isinstance(item, dict) else 1
            except Exception:
                pass
    return {
        'top_items': [item for item, _ in items_counter.most_common(5)],
        'top_categories': [cat for cat, _ in categories_counter.most_common(3)],
        'monthly_spending': dict(monthly_spending)
    }

async def generate_dietary_insights(summary: NutritionalSummary, user_context: Dict[str, Any] = None) -> List[str]:
    # Existing code for generate_dietary_insights (unchanged)
    # ...
    pass  # (keep or fill in as before)

# --- Move get_combined_dietary_insights to top level ---
async def get_combined_dietary_insights(summary: NutritionalSummary, user_context: Dict[str, Any] = None) -> Dict[str, List[str]]:
    """
    Returns both current receipt-based and historical personalized dietary insights.
    Usage:
        summary = calculate_nutritional_summary(receipts)
        insights = await get_combined_dietary_insights(summary)
        # insights['current'] -> insights for just this upload
        # insights['historical'] -> trend-based suggestions
    """
    current_insights = await generate_dietary_insights(summary, user_context=None)
    # For historical, pass dummy summary (since only context matters)
    if summary.item_count == 0:
        return {
            'current': ["Start logging your groceries to receive personalized dietary insights!"],
            'historical': []
        }
    if user_context is None:
        user_context = analyze_purchase_history()
    top_items = ', '.join(user_context.get('top_items', []))
    top_categories = ', '.join(user_context.get('top_categories', []))
    monthly_trend = user_context.get('monthly_spending', {})
    trend_str = ', '.join([f"{month}: ${amt:.2f}" for month, amt in sorted(monthly_trend.items())[-3:]])
    try:
        chat = LlmChat(
            api_key=os.environ.get('GOOGLE_GEMINI_KEY'),
            session_id=f"dietary-insights-{uuid.uuid4()}",
            system_message="""You are a helpful and encouraging AI Dietician for Project Raseed. Your goal is to provide actionable, positive, and non-judgmental advice based on the user's weekly nutritional intake and their real purchase history. Use their most frequent items and categories, and mention any spending trends if relevant. Do not give medical advice. Frame your response as a helpful coach. Return the insights as a JSON array of strings, like [\"Insight 1\", \"Insight 2\"]."""
        ).with_model("gemini", "gemini-2.0-flash")
        prompt = f"""Here is the user's nutritional summary for the past week:\n- Calories: {summary.total_calories:.0f} kcal\n- Protein: {summary.total_protein:.1f} g\n- Carbohydrates: {summary.total_carbs:.1f} g\n- Fat: {summary.total_fat:.1f} g\n- Fiber: {summary.total_fiber:.1f} g\n\nMost frequently purchased items: {top_items}\nMost common categories: {top_categories}\nRecent spending trend: {trend_str}\n\nPlease provide 2-3 encouraging and actionable insights based on this data and the user's real purchase history. Return only the JSON array."""
        response = await chat.send_message(UserMessage(text=prompt))
        response_text = response.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        historical_insights = json.loads(response_text)
    except Exception as e:
        print(f"Error generating dietary insights: {e}")
        historical_insights = ["Sorry, we couldn't generate insights due to an internal error."]
    return {
        'current': current_insights,
        'historical': historical_insights
    }
