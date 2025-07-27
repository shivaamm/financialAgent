import pandas as pd
import uuid
from datetime import datetime, timedelta
import random

# Function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Expanded categories and merchants
categories = ['Grocery', 'Electronics', 'Transport', 'Retail', 'Shopping', 'Pharmacy', 'Dining', 'Utilities', 'Entertainment']
merchants = ['BIG BAZAAR', 'DMART', 'RELIANCE FRESH', 'MORE SUPERMARKET', "SPENCER'S", 'PHARMA PLUS', 'EATERY', 'CITY UTILITIES', 'MOVIEPLEX']

# Sample items for different categories
items_pool = {
    'Grocery': [{'name': 'RICE', 'price': 20.00}, {'name': 'LENTILS', 'price': 15.50}, {'name': 'SPICES', 'price': 10.00}],
    'Electronics': [{'name': 'HEADPHONES', 'price': 150.00}, {'name': 'CHARGER', 'price': 50.00}],
    'Transport': [{'name': 'BUS PASS', 'price': 30.00}, {'name': 'TAXI RIDE', 'price': 100.00}],
    'Retail': [{'name': 'SHIRT', 'price': 40.00}, {'name': 'JEANS', 'price': 60.00}],
    'Shopping': [{'name': 'SHOES', 'price': 70.00}, {'name': 'WATCH', 'price': 120.00}],
    'Pharmacy': [{'name': 'VITAMINS', 'price': 25.00}, {'name': 'PAINKILLERS', 'price': 15.00}],
    'Dining': [{'name': 'LUNCH', 'price': 50.00}, {'name': 'DINNER', 'price': 80.00}],
    'Utilities': [{'name': 'ELECTRICITY BILL', 'price': 100.00}, {'name': 'WATER BILL', 'price': 50.00}],
    'Entertainment': [{'name': 'MOVIE TICKET', 'price': 15.00}, {'name': 'CONCERT TICKET', 'price': 100.00}]
}

# Generate wallet_passes.csv data
wallet_data = []
for _ in range(50):
    category = random.choice(categories)
    merchant = random.choice(merchants)
    amount = round(sum(item['price'] for item in random.sample(items_pool[category], 2)), 2)
    created_at = datetime.now().isoformat()
    date = random_date(datetime(2025, 1, 1), datetime(2025, 7, 26)).isoformat()
    description = f"Receipt from {merchant} on {date[:10]}"
    id = str(uuid.uuid4())
    status = 'active'
    title = f"{merchant} - ₹{amount}"
    wallet_data.append([amount, category, created_at, date, description, id, merchant, status, title])

# Save to wallet_passes.csv
wallet_df = pd.DataFrame(wallet_data, columns=['amount', 'category', 'created_at', 'date', 'description', 'id', 'merchant', 'status', 'title'])
wallet_df.to_csv('/Users/5108912/Downloads/AgenticAI-master/backend/wallet_passes.csv', mode='a', header=False, index=False)

# Generate receipts.csv data
receipts_data = []
for record in wallet_data:
    analysis_text = f"Analysis complete for {record[6]}"
    insights = "['Purchased various items.', 'Consider loyalty programs for savings.']"
    items = str(random.sample(items_pool[record[1]], 2))
    savings_suggestions = "['Look for discounts.', 'Consider bulk buying.']"
    receipts_data.append([analysis_text, record[1], record[2], record[3], record[5], insights, items, record[6], savings_suggestions, record[0]])

# Save to receipts.csv
receipts_df = pd.DataFrame(receipts_data, columns=['analysis_text', 'category', 'created_at', 'date', 'id', 'insights', 'items', 'merchant_name', 'savings_suggestions', 'total_amount'])
receipts_df.to_csv('/Users/5108912/Downloads/AgenticAI-master/backend/receipts.csv', mode='a', header=False, index=False)