import unittest
from datetime import datetime
from dietary_coaching import train_your_diet_ai_coach, Receipt, ReceiptItem

class TestDietaryCoaching(unittest.TestCase):
    def setUp(self):
        # Mock data setup
        self.mock_receipts = [
            Receipt(
                id="receipt1", merchant_name="GroceryMart", total_amount=35.50,
                date=datetime.now(), image_base64="", analysis_text="",
                items=[
                    ReceiptItem(name="apple", price=1.50, quantity=2),
                    ReceiptItem(name="chicken breast", price=8.00, quantity=1),
                    ReceiptItem(name="brown rice", price=4.00, quantity=1)
                ],
                category="Groceries"
            ),
            Receipt(
                id="receipt2", merchant_name="Super Savers", total_amount=22.00,
                date=datetime.now(), image_base64="", analysis_text="",
                items=[
                    ReceiptItem(name="spinach", price=3.00, quantity=1),
                    ReceiptItem(name="eggs", price=4.50, quantity=1),
                    ReceiptItem(name="whole wheat bread", price=3.50, quantity=1),
                    ReceiptItem(name="avocado", price=2.00, quantity=2),
                ],
                category="Groceries"
            )
        ]

    def test_energy_query(self):
        response = train_your_diet_ai_coach("I need more energy", self.mock_receipts)
        print(f"Energy Query Response: {response}")
        self.assertIn("sugary snacks", response)

    def test_protein_query(self):
        response = train_your_diet_ai_coach("How's my protein intake?", self.mock_receipts)
        print(f"Protein Query Response: {response}")
        self.assertIn("protein intake", response)

    def test_weight_loss_query(self):
        response = train_your_diet_ai_coach("Any tips for weight loss?", self.mock_receipts)
        print(f"Weight Loss Query Response: {response}")
        self.assertIn("weight loss", response)

if __name__ == "__main__":
    unittest.main()
