import pandas as pd
import uuid
from datetime import datetime, timedelta
import random

# Function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Sample categories and merchants
categories = ['Electronics', 'Clothing', 'Food', 'Health', 'Transport', 'Shopping', 'Dining', 'Utilities']
merchants = ['Amazon', 'Walmart', 'Target', 'Best Buy', 'Whole Foods', 'Uber', 'Lyft', 'Costco', 'Apple Store']

# Sample items for different categories
items_pool = {
    'Electronics': [{'name': 'Bluetooth Headphones', 'price': 79.99}, {'name': 'Smartphone', 'price': 699.99}],
    'Clothing': [{'name': 'T-Shirt', 'price': 19.99}, {'name': 'Jeans', 'price': 49.99}],
    'Food': [{'name': 'Organic Apples', 'price': 5.99}, {'name': 'Almond Milk', 'price': 3.99}],
    'Health': [{'name': 'Vitamins', 'price': 15.99}, {'name': 'Protein Powder', 'price': 29.99}],
    'Transport': [{'name': 'Bus Pass', 'price': 30.00}, {'name': 'Taxi Ride', 'price': 20.00}],
    'Shopping': [{'name': 'Shoes', 'price': 89.99}, {'name': 'Watch', 'price': 199.99}],
    'Dining': [{'name': 'Dinner', 'price': 50.00}, {'name': 'Lunch', 'price': 30.00}],
    'Utilities': [{'name': 'Electricity Bill', 'price': 100.00}, {'name': 'Water Bill', 'price': 50.00}]
}

# Generate email_receipts.csv data
email_data = []
for _ in range(100):
    category = random.choice(categories)
    merchant = random.choice(merchants)
    created_at = datetime.now().isoformat()
    received_date = random_date(datetime(2025, 1, 1), datetime(2025, 7, 26)).isoformat()
    email_id = str(uuid.uuid4())
    id = email_id
    items = random.sample(items_pool[category], 2)
    total_amount = sum(item['price'] for item in items)
    email_content = f"""
        Thanks for shopping with {merchant}!
        
        Order Details:
        Date: {received_date}
        
        Items Ordered:
        1. {items[0]['name']}   ${items[0]['price']}
        2. {items[1]['name']}   ${items[1]['price']}
        
        Total: ${total_amount}
        """
    insights = f"['Spent ${total_amount} on {category} items from {merchant}.']"
    savings_suggestions = "['Look for discounts.', 'Consider loyalty programs for savings.']"
    email_data.append([category, created_at, email_content, email_id, id, insights, str(items), merchant, True, received_date, savings_suggestions, f"{merchant}@receipts.com", "email", f"Order Confirmation", total_amount])

# Save to email_receipts.csv
email_df = pd.DataFrame(email_data, columns=['category', 'created_at', 'email_content', 'email_id', 'id', 'insights', 'items', 'merchant_name', 'processed', 'received_date', 'savings_suggestions', 'sender', 'source', 'subject', 'total_amount'])
email_df.to_csv('/Users/5108912/Downloads/AgenticAI-master/backend/email_receipts.csv', mode='a', header=False, index=False)
