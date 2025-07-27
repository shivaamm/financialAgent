import asyncio
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import json

# Import the functions and models to be tested
from nutrition_analysis import (
    Receipt,
    ReceiptItem,
    NutritionalSummary,
    calculate_nutritional_summary,
    generate_dietary_insights
)

# --- Mock Data Setup ---

def create_mock_receipts():
    """Creates a list of mock grocery receipts for the last 7 days."""
    now = datetime.utcnow()
    return [
        Receipt(
            id="receipt1", merchant_name="GroceryMart", total_amount=35.50, date=now - timedelta(days=1),
            items=[
                ReceiptItem(name="apple", price=1.50, quantity=2),
                ReceiptItem(name="chicken breast", price=8.00, quantity=1),
                ReceiptItem(name="brown rice", price=4.00, quantity=1)
            ],
            category="Groceries", image_base64="", analysis_text="", created_at=now - timedelta(days=1)
        ),
        Receipt(
            id="receipt2", merchant_name="Super Savers", total_amount=22.00, date=now - timedelta(days=3),
            items=[
                ReceiptItem(name="spinach", price=3.00, quantity=1),
                ReceiptItem(name="eggs", price=4.50, quantity=1),
                ReceiptItem(name="whole wheat bread", price=3.50, quantity=1),
                ReceiptItem(name="avocado", price=2.00, quantity=2),
            ],
            category="Groceries", image_base64="", analysis_text="", created_at=now - timedelta(days=3)
        ),
        Receipt(
            id="receipt3", merchant_name="Quick Foods", total_amount=15.75, date=now - timedelta(days=5),
            items=[
                ReceiptItem(name="banana", price=0.75, quantity=3),
                ReceiptItem(name="greek yogurt", price=5.00, quantity=1),
                ReceiptItem(name="almonds", price=8.00, quantity=1)
            ],
            category="Groceries", image_base64="", analysis_text="", created_at=now - timedelta(days=5)
        ),
        Receipt(
            id="receipt4", merchant_name="Gas Station", total_amount=55.00, date=now - timedelta(days=2),
            items=[ReceiptItem(name="gasoline", price=55.00, quantity=1)],
            category="Transport", image_base64="", analysis_text="", created_at=now - timedelta(days=2)
        )
    ]

# Mock for fetch_nutritional_data to avoid actual API calls
@patch('nutrition_analysis.fetch_nutritional_data')
def test_nutritional_summary(mock_fetch_data):
    print("--- Testing Nutritional Summary Calculation ---")
    
    # Define the return values for our mock API call
    mock_nutrition_db = {
        "apple": {'item': 'apple', 'protein': 0.3, 'fiber': 2.4, 'carbs': 14, 'fat': 0.2, 'calories': 52},
        "chicken breast": {'item': 'chicken breast', 'protein': 31, 'fiber': 0, 'carbs': 0, 'fat': 3.6, 'calories': 165},
        "brown rice": {'item': 'brown rice', 'protein': 2.6, 'fiber': 1.8, 'carbs': 23, 'fat': 0.9, 'calories': 111},
        "spinach": {'item': 'spinach', 'protein': 2.9, 'fiber': 2.2, 'carbs': 3.6, 'fat': 0.4, 'calories': 23},
        "eggs": {'item': 'eggs', 'protein': 6, 'fiber': 0, 'carbs': 0.6, 'fat': 5, 'calories': 72},
        "whole wheat bread": {'item': 'whole wheat bread', 'protein': 13, 'fiber': 7, 'carbs': 41, 'fat': 3.4, 'calories': 247},
        "avocado": {'item': 'avocado', 'protein': 2, 'fiber': 7, 'carbs': 9, 'fat': 15, 'calories': 160},
        "banana": {'item': 'banana', 'protein': 1.1, 'fiber': 2.6, 'carbs': 23, 'fat': 0.3, 'calories': 89},
        "greek yogurt": {'item': 'greek yogurt', 'protein': 10, 'fiber': 0, 'carbs': 3.6, 'fat': 0.4, 'calories': 59},
        "almonds": {'item': 'almonds', 'protein': 21, 'fiber': 12.5, 'carbs': 21.6, 'fat': 49.9, 'calories': 579},
    }
    mock_fetch_data.side_effect = lambda item_name: mock_nutrition_db.get(item_name)

    receipts = create_mock_receipts()
    summary = calculate_nutritional_summary(receipts)

    print(f"Calculation complete. Items processed: {summary.item_count}")
    print(f"Total Calories: {summary.total_calories:.2f} kcal")
    print(f"Total Protein: {summary.total_protein:.2f} g")
    print(f"Total Carbs: {summary.total_carbs:.2f} g")
    print(f"Total Fat: {summary.total_fat:.2f} g")
    print(f"Total Fiber: {summary.total_fiber:.2f} g")
    print("---------------------------------------------")
    return summary

# Mock for generate_dietary_insights to avoid actual AI calls
@patch('nutrition_analysis.LlmChat')
def test_ai_insights(summary, mock_llm_chat):
    print("\n--- Testing AI Dietary Insights Generation ---")

    # Mock the response from the Gemini AI
    mock_ai_response = [
        f"Great job! You've consumed {summary.total_protein:.1f}g of protein, which is {summary.total_protein/50*100:.0f}% of the daily recommended intake.",
        f"Consider increasing your fiber intake. You've consumed {summary.total_fiber:.1f}g, which is {summary.total_fiber/25*100:.0f}% of the daily recommended intake.",
        f"Your fat intake is {summary.total_fat:.1f}g, making up {summary.total_fat/70*100:.0f}% of the daily recommended limit."
    ]
    
    # Setup the mock to return our desired response
    mock_chat_instance = MagicMock()
    future = asyncio.Future()
    future.set_result(json.dumps(mock_ai_response))
    mock_chat_instance.send_message.return_value = future
    mock_llm_chat.return_value.with_model.return_value = mock_chat_instance

    # Run the function
    insights = asyncio.run(generate_dietary_insights(summary))

    print("AI Dietician says:")
    for insight in insights:
        print(f"- {insight}")
    print("-------------------------------------------")

if __name__ == "__main__":
    nutritional_summary = test_nutritional_summary()
    if nutritional_summary.item_count > 0:
        test_ai_insights(nutritional_summary)