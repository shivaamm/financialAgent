import re
from typing import List, Dict
from nutrition_analysis import Receipt, ReceiptItem

# Define keywords for processed foods
PROCESSED_KEYWORDS = ["instant", "frozen", "canned", "packaged", "microwave", "ready-to-eat"]

# Function to classify food items

def classify_food_items(receipts: List[Receipt]) -> Dict[str, float]:
    """Classify food items as whole or processed and calculate a freshness score."""
    whole_food_count = 0
    processed_food_count = 0
    
    for receipt in receipts:
        for item in receipt.items:
            # Check for processed keywords
            if any(keyword in item.name.lower() for keyword in PROCESSED_KEYWORDS):
                processed_food_count += item.quantity
            else:
                whole_food_count += item.quantity

    total_items = whole_food_count + processed_food_count
    freshness_score = (whole_food_count / total_items) * 100 if total_items > 0 else 0
    
    return {
        "whole_food_count": whole_food_count,
        "processed_food_count": processed_food_count,
        "freshness_score": freshness_score
    }

# Function for AI-Powered Meal Suggestions

def generate_meal_suggestions(receipts: List[Receipt]) -> List[str]:
    """Generate meal suggestions based on purchased items."""
    # Extract unique item names
    unique_items = set(item.name.lower() for receipt in receipts for item in receipt.items)
    
    # Example heuristic for meal suggestions
    meal_suggestions = []
    if "chicken" in unique_items and "rice" in unique_items and "broccoli" in unique_items:
        meal_suggestions.append("How about making a healthy teriyaki stir-fry with chicken, rice, and broccoli?")
    if "eggs" in unique_items and "spinach" in unique_items:
        meal_suggestions.append("Try a spinach and egg omelette for a nutritious breakfast.")
    if "avocado" in unique_items and "bread" in unique_items:
        meal_suggestions.append("Make a delicious avocado toast for a quick snack.")

    return meal_suggestions

# Placeholder for Train Your Diet AI Coach

import os
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage

# ... (rest of your code) ...

import csv

# Utility to summarize receipt items for LLM context
def summarize_receipts(receipts):
    items = []
    for r in receipts:
        for item in getattr(r, 'items', []):
            items.append(f"{item.quantity} x {item.name}")
    return ", ".join(items) if items else "No items found."

# Utility to summarize CSV data (e.g., nutrition_cache.csv)
def summarize_nutrition_cache():
    cache_path = os.path.join(os.path.dirname(__file__), 'nutrition_cache.csv')
    if not os.path.exists(cache_path):
        return "Nutrition database not available."
    summary = []
    with open(cache_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            summary.append(f"{row['item']} (Protein: {row['protein']}g, Fiber: {row['fiber']}g, Calories: {row['calories']})")
    return "; ".join(summary[:30])  # Limit for prompt size

async def train_your_diet_ai_coach(user_query: str, receipts: list) -> str:
    """Agentic dietary/finance coach using Gemini: answers any user query, using all available user data as context."""
    import os
    api_key = os.environ.get('GOOGLE_GEMINI_KEY')
    if not api_key:
        return "AI key not configured."
    query_lower = user_query.lower()
    # Finance/insight keywords
    finance_keywords = [
        'spending', 'expense', 'expenses', 'total', 'breakdown', 'category', 'savings', 'save', 'finance', 'budget', 'prediction', 'insight', 'how much', 'how many', 'how often', 'trend', 'average', 'cost', 'price', 'cheapest', 'most expensive', 'compare', 'bill', 'utility', 'electricity', 'water', 'gas', 'monthly', 'weekly', 'yearly', 'per month', 'per week', 'per year'
    ]
    # Collect all keywords from receipts and CSV
    item_keywords = set()
    for r in receipts:
        for item in getattr(r, 'items', []):
            item_keywords.add(item.name.lower())
    # Scan nutrition CSV for more keywords
    csv_keywords = set()
    cache_path = os.path.join(os.path.dirname(__file__), 'nutrition_cache.csv')
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_keywords.add(row['item'].lower())
    all_keywords = item_keywords | csv_keywords
    matched_keywords = [kw for kw in all_keywords if kw in query_lower]
    matched_finance = any(kw in query_lower for kw in finance_keywords)

    chat = LlmChat(
        api_key=api_key,
        session_id=f"dietary-coach-{os.urandom(6).hex()}",
        system_message=(
            "You are an expert dietary, grocery, and financial assistant. Use the user's receipts, nutrition, and spending data to answer their question. Always be practical, specific, and concise."
        )
    ).with_model("gemini", "gemini-2.0-flash")

    # If finance/savings/insight question, summarize finance data
    if matched_finance:
        # Calculate total spending and category breakdown
        total_spending = sum(getattr(r, 'total_amount', 0) for r in receipts)
        category_spending = {}
        for r in receipts:
            cat = getattr(r, 'category', 'Other')
            category_spending[cat] = category_spending.get(cat, 0) + getattr(r, 'total_amount', 0)
        # Simple savings estimate (mock, you can improve)
        savings = max(0, 1000 - total_spending)  # e.g. $1000/month budget
        insights = []
        # Add more advanced insight logic here if desired
        receipt_summary = summarize_receipts(receipts)
        nutrition_summary = summarize_nutrition_cache()
        prompt = (
            f"User's grocery history: {receipt_summary}\n"
            f"Nutrition database: {nutrition_summary}\n"
            f"Total spending: ${total_spending:.2f}\n"
            f"Category breakdown: {category_spending}\n"
            f"Estimated savings: ${savings:.2f}\n"
            f"User's question: {user_query}\n"
            "---\n"
            "Instructions: Answer using the user's financial and grocery data. Be concise, use bullet points, and provide actionable insights or calculations."
        )
    elif matched_keywords:
        # Build focused grocery/nutrition prompt
        receipt_summary = summarize_receipts(receipts)
        nutrition_summary = summarize_nutrition_cache()
        prompt = (
            f"User's grocery history: {receipt_summary}\n"
            f"Nutrition database: {nutrition_summary}\n"
            f"User's question: {user_query}\n"
            f"Relevant keywords: {', '.join(matched_keywords)}\n"
            "---\n"
            "Instructions: Answer in a concise, clear way. Use bullet points for suggestions. Only include the most relevant and actionable information. Do not repeat the full data. Limit your response to a few sentences or 4-5 bullet points maximum."
        )
    else:
        # No keyword match, ask Gemini as general assistant, but provide receipts summary for context
        receipt_summary = summarize_receipts(receipts)
        nutrition_summary = summarize_nutrition_cache()
        prompt = (
            f"User's grocery history: {receipt_summary}\n"
            f"Nutrition database: {nutrition_summary}\n"
            f"User's question: {user_query}\n"
            "---\n"
            "Instructions: Answer as a helpful dietary, grocery, and financial assistant. Be concise, use bullet points if possible, and provide actionable advice."
        )
    try:
        response = await chat.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        return f"Sorry, AI coaching failed: {e}"
