from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import firestore, storage, credentials
import os
from export_firestore_to_csv import append_to_csv
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import base64
import json
import asyncio
from PIL import Image
import io
import re
import random
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
import firebase_admin
from fastapi import Request
# Add the path to emergentintegrations if it's in backend/emergentintegrations
sys.path.append(str(Path(__file__).parent / "emergentintegrations"))

# Gemini Integration
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

# Database Configuration
# MongoDB Version:
# from motor.motor_asyncio import AsyncIOMotorClient
# mongo_url = os.environ['MONGO_URL']
# client = AsyncIOMotorClient(mongo_url)
# db = client[os.environ['DB_NAME']]

# Firebase Version:
from firebase_config import db, storage_bucket

# --- Models (keep only one definition here) ---
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
    image_base64: str = ""
    analysis_text: str = ""
    insights: List[str] = []
    savings_suggestions: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = "manual"

class EmailReceipt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email_id: str = ""
    sender: str = ""
    subject: str = ""
    received_date: datetime = Field(default_factory=datetime.utcnow)
    email_content: str = ""
    merchant_name: str = ""
    total_amount: float = 0.0
    items: List[Dict[str, Any]] = []
    category: str = ""
    insights: List[str] = []
    savings_suggestions: List[str] = []
    processed: bool = False
    source: str = "email"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- Helper for Firestore dicts ---
def parse_receipt_dict(d):
    # Convert date fields if needed
    if 'created_at' in d and isinstance(d['created_at'], str):
        try:
            d['created_at'] = datetime.fromisoformat(d['created_at'])
        except Exception:
            pass
    if 'date' in d and isinstance(d['date'], str):
        try:
            d['date'] = datetime.fromisoformat(d['date'])
        except Exception:
            pass
    if 'received_date' in d and isinstance(d['received_date'], str):
        try:
            d['received_date'] = datetime.fromisoformat(d['received_date'])
        except Exception:
            pass
    # Convert items if needed
    if 'items' in d and isinstance(d['items'], list):
        d['items'] = [
            item.model_dump() if isinstance(item, ReceiptItem) else item
            for item in d['items']
        ]
    return d

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
# app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (if needed) goes here
    yield
    # Shutdown code
    # client.close()

app = FastAPI(lifespan=lifespan)

from dietary_coaching import train_your_diet_ai_coach

# ... (rest of your code)

api_router = APIRouter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models

# --- Agentic Store Recommendation ---
from store_recommendation import recommend_stores_for_groceries
from fastapi import Body

class StoreRecommendationRequest(BaseModel):
    items: List[str]
    location: str  # e.g., city name or pincode

class StoreRecommendationResponse(BaseModel):
    store: str
    item: str
    price: float
    availability: bool
    store_location: str
    store_address: str
    nearby_store: dict = None

@api_router.post("/dietary-coaching")
async def dietary_coaching_endpoint(request: Request):
    data = await request.json()
    user_query = data.get("query")
    # Fetch recent receipts from Firestore (limit to 10 for performance)
    receipts_ref = db.collection('receipts')
    receipts_query = receipts_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(10)
    receipts = [Receipt(**parse_receipt_dict(doc.to_dict())) for doc in receipts_query.stream()]
    response = await train_your_diet_ai_coach(user_query, receipts)
    return {"response": response}

@api_router.post("/recommend-stores", response_model=List[StoreRecommendationResponse])
async def recommend_stores(request: StoreRecommendationRequest = Body(...)):
    """Agentic endpoint: Given grocery items and user location, returns top 2 store recommendations (real data)."""
    results = recommend_stores_for_groceries(request.items, request.location)
    return results

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ReceiptItem(BaseModel):
    name: str
    price: float
    quantity: int = 1














class ReceiptAnalysis(BaseModel):
    merchant_name: str
    total_amount: float
    date: str
    items: List[Dict[str, Any]]
    category: str
    insights: List[str]
    savings_suggestions: List[str]

class SpendingInsight(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    amount: float
    suggestion: str
    type: str  # "warning", "tip", "achievement"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WalletPass(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    amount: float
    category: str
    merchant: str
    date: datetime
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Gmail Integration Models

















class GmailConnection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    connected: bool = True
    last_sync: datetime = Field(default_factory=datetime.utcnow)
    total_emails_processed: int = 0
    auto_processing: bool = True

class EmailReceiptAnalysis(BaseModel):
    merchant_name: str
    total_amount: float
    items: List[Dict[str, Any]]
    category: str
    insights: List[str]
    savings_suggestions: List[str]

# Gmail Receipt Analyzer
class GmailReceiptAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_GEMINI_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_GEMINI_KEY not found in environment variables")
    
    async def analyze_email_receipt(self, email_content: str, subject: str, sender: str) -> EmailReceiptAnalysis:
        """Analyze email receipt content using Gemini AI"""
        try:
            # Create new chat instance for email analysis
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"email-receipt-analysis-{uuid.uuid4()}",
                system_message="""You are an expert email receipt analyzer for Project Raseed. 
                Analyze email content to extract purchase information from email receipts.
                
                Return your analysis in this exact JSON format:
                {
                    "merchant_name": "Name of store/company",
                    "total_amount": 0.00,
                    "items": [
                        {"name": "Item name", "price": 0.00, "quantity": 1}
                    ],
                    "category": "Category (Food, Shopping, Transport, Entertainment, etc.)",
                    "insights": [
                        "Insight about spending pattern from email",
                        "Analysis of purchase timing/frequency"
                    ],
                    "savings_suggestions": [
                        "Specific savings suggestion based on email content"
                    ]
                }
                
                Be intelligent about extracting data from various email formats (HTML, plain text, different merchants)."""
            ).with_model("gemini", "gemini-2.0-flash")
            
            # Create email analysis prompt
            email_prompt = f"""
            Analyze this email receipt:
            
            Subject: {subject}
            Sender: {sender}
            Content: {email_content}
            
            Extract all purchase information and return only the JSON response with no additional text.
            """
            
            # Send analysis request
            user_message = UserMessage(text=email_prompt)
            response = await chat.send_message(user_message)
            
            # Parse JSON response
            try:
                # Clean response if it has markdown formatting
                response_text = response.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:-3]
                elif response_text.startswith('```'):
                    response_text = response_text[3:-3]
                
                analysis_data = json.loads(response_text)
                return EmailReceiptAnalysis(**analysis_data)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse email analysis response: {e}")
                logger.error(f"Response: {response}")
                # Return default analysis if parsing fails
                return EmailReceiptAnalysis(
                    merchant_name=self.extract_merchant_from_sender(sender),
                    total_amount=0.0,
                    items=[],
                    category="Other",
                    insights=["Email receipt processed but details extraction failed"],
                    savings_suggestions=["Keep digital receipts for better tracking"]
                )
                
        except Exception as e:
            logger.error(f"Email analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Email receipt analysis failed: {str(e)}")
    
    def extract_merchant_from_sender(self, sender: str) -> str:
        """Extract merchant name from email sender"""
        # Remove email domain and clean up
        if '@' in sender:
            merchant = sender.split('@')[0]
            # Clean common email prefixes
            merchant = re.sub(r'^(no-reply|noreply|receipt|order)', '', merchant, flags=re.IGNORECASE)
            merchant = merchant.replace('-', ' ').replace('_', ' ').title()
            return merchant.strip() or "Unknown Merchant"
        return sender

# Gmail Demo Service
class GmailDemoService:
    def __init__(self):
        self.demo_emails = [
            {
                "sender": "receipt@starbucks.com",
                "subject": "Your Starbucks Receipt",
                "content": """
                Thank you for your purchase at Starbucks!
                
                Order #: 12345
                Date: {date}
                Location: Downtown Store
                
                Items:
                - Grande Latte                 $5.25
                - Blueberry Muffin            $3.45
                - Extra Shot                  $0.75
                
                Subtotal:                     $9.45
                Tax:                         $0.85
                Total:                       $10.30
                
                Thank you for choosing Starbucks!
                """,
                "category": "Food"
            },
            {
                "sender": "orders@amazon.com",
                "subject": "Your Amazon Order Confirmation",
                "content": """
                Your order has been shipped!
                
                Order #: 123-4567890-1234567
                Order Date: {date}
                
                Items Ordered:
                1. Wireless Bluetooth Headphones   $79.99
                2. Phone Case - Clear              $12.99
                3. USB Cable - 6ft                 $8.99
                
                Subtotal:                         $101.97
                Shipping:                          FREE
                Tax:                              $8.16
                Total:                           $110.13
                
                Expected Delivery: Tomorrow
                """,
                "category": "Shopping"
            },
            {
                "sender": "receipts@uber.com",
                "subject": "Trip Receipt",
                "content": """
                Thanks for riding with Uber!
                
                Trip Details:
                Date: {date}
                From: Home
                To: Downtown Office
                Distance: 5.2 miles
                Duration: 18 minutes
                
                Fare Breakdown:
                Base Fare:                        $2.50
                Distance:                         $8.75
                Time:                            $3.20
                Booking Fee:                      $2.55
                
                Total:                           $17.00
                Payment: Visa ****1234
                """,
                "category": "Transport"
            },
            {
                "sender": "receipt@target.com",
                "subject": "Target Receipt - Store #1234",
                "content": """
                Thank you for shopping at Target!
                
                Store #1234
                Date: {date}
                REF# 1234-5678-9012
                
                Items:
                - Organic Bananas 2lb             $3.49
                - Bread - Whole Wheat             $2.99
                - Milk - 2% Gallon                $3.79
                - Greek Yogurt 4-pack             $5.49
                - Laundry Detergent               $11.99
                - Paper Towels 6-pack             $8.99
                
                Subtotal:                        $36.74
                Tax:                             $2.94
                Total:                          $39.68
                
                You saved $5.50 today!
                """,
                "category": "Grocery"
            },
            {
                "sender": "noreply@netflix.com",
                "subject": "Netflix - Your monthly bill",
                "content": """
                Your Netflix subscription has been renewed.
                
                Plan: Premium (4 screens, Ultra HD)
                Billing Date: {date}
                Next Billing Date: {next_month}
                
                Amount Charged: $19.99
                Payment Method: Visa ending in 1234
                
                Enjoy your Netflix subscription!
                """,
                "category": "Entertainment"
            }
        ]
    
    async def simulate_incoming_email(self) -> Dict[str, Any]:
        """Simulate receiving a random email receipt"""
        email_template = random.choice(self.demo_emails)
        
        # Generate realistic timestamps
        now = datetime.utcnow()
        email_date = now - timedelta(minutes=random.randint(1, 1440))  # Within last 24 hours
        next_month = now + timedelta(days=30)
        
        # Fill in dynamic content
        content = email_template["content"].format(
            date=email_date.strftime("%Y-%m-%d %H:%M:%S"),
            next_month=next_month.strftime("%Y-%m-%d")
        )
        
        return {
            "email_id": f"email-{uuid.uuid4()}",
            "sender": email_template["sender"],
            "subject": email_template["subject"],
            "content": content,
            "received_date": email_date,
            "category": email_template["category"]
        }

class ReceiptAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_GEMINI_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_GEMINI_KEY not found in environment variables")
    
    async def analyze_receipt(self, image_base64: str) -> ReceiptAnalysis:
        """Analyze receipt image using Gemini AI"""
        try:
            # Create new chat instance for each analysis
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"receipt-analysis-{uuid.uuid4()}",
                system_message="""You are an expert receipt analyzer for Project Raseed. 
                Extract structured data from receipt images and provide financial insights.
                
                Return your analysis in this exact JSON format:
                {
                    "merchant_name": "Name of store/restaurant",
                    "total_amount": 0.0,
                    "date": "YYYY-MM-DD",
                    "items": [
                        {"name": "Item name", "price": 0.0, "quantity": 1}
                    ],
                    "category": "Category",
                    "insights": ["Insight 1", "Insight 2"],
                    "savings_suggestions": ["Suggestion 1", "Suggestion 2"]
                }
                """
            ).with_model("gemini", "gemini-2.0-flash")
            
            # Create image content
            image_content = ImageContent(image_base64=image_base64)
            
            # Send message with image
            user_message = UserMessage(
                text="Analyze this receipt and extract all information. Return only the JSON response with no additional text.",
                file_contents=[image_content]
            )
            
            response = await chat.send_message(user_message)
            
            # Parse JSON response
            try:
                # Clean response if it has markdown formatting
                response_text = response.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:-3]
                elif response_text.startswith('```'):
                    response_text = response_text[3:-3]
                
                analysis_data = json.loads(response_text)
                return ReceiptAnalysis(**analysis_data)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Gemini response: {e}")
                logger.error(f"Response: {response}")
                # Return default analysis if parsing fails
                return ReceiptAnalysis(
                    merchant_name="Unknown Merchant",
                    total_amount=0.0,
                    date=datetime.now().strftime("%Y-%m-%d"),
                    items=[],
                    category="Other",
                    insights=["Receipt analyzed but details could not be extracted clearly"],
                    savings_suggestions=["Consider keeping digital receipts for better tracking"]
                )
                
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Receipt analysis failed: {str(e)}")

# Initialize analyzers
receipt_analyzer = ReceiptAnalyzer()
gmail_analyzer = GmailReceiptAnalyzer()
gmail_demo_service = GmailDemoService()

# Helper Functions
def generate_insights(receipts: List[Receipt]) -> List[SpendingInsight]:
    """Generate spending insights from receipts"""
    insights = []
    
    if not receipts:
        return insights
    
    # Calculate total spending
    total_spending = sum(r.total_amount for r in receipts)
    
    # Category analysis
    category_spending = {}
    for receipt in receipts:
        category_spending[receipt.category] = category_spending.get(receipt.category, 0) + receipt.total_amount
    
    # Top spending category
    if category_spending:
        top_category = max(category_spending, key=category_spending.get)
        insights.append(SpendingInsight(
            title=f"Top Spending: {top_category}",
            description=f"You've spent ${category_spending[top_category]:.2f} on {top_category} recently",
            category=top_category,
            amount=category_spending[top_category],
            suggestion=f"Consider setting a budget limit for {top_category} expenses",
            type="tip"
        ))
    
    # Recent spending
    from datetime import timezone
    now = datetime.now(timezone.utc)
    recent_receipts = [r for r in receipts if (now - r.created_at.astimezone(timezone.utc)).days <= 7]
    if recent_receipts:
        recent_total = sum(r.total_amount for r in recent_receipts)
        insights.append(SpendingInsight(
            title="This Week's Spending",
            description=f"You've spent ${recent_total:.2f} in the last 7 days",
            category="General",
            amount=recent_total,
            suggestion="Track daily expenses to identify spending patterns",
            type="warning" if recent_total > 200 else "tip"
        ))
    
    return insights

def create_wallet_pass(receipt: Receipt) -> WalletPass:
    """Create a wallet pass from receipt"""
    return WalletPass(
        title=f"{receipt.merchant_name} - ${receipt.total_amount:.2f}",
        description=f"Receipt from {receipt.merchant_name} on {receipt.date.strftime('%B %d, %Y')}",
        amount=receipt.total_amount,
        category=receipt.category,
        merchant=receipt.merchant_name,
        date=receipt.date
    )

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Project Raseed - AI Receipt Management System"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    # Save status check to database
    status_check_ref = db.collection('status_checks').document(status_obj.id)
    status_check_ref.set(status_obj.dict())
    append_to_csv('status_checks', status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks_ref = db.collection('status_checks')
    status_checks_query = status_checks_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1000)
    return [StatusCheck(**doc.to_dict()) for doc in status_checks_query.stream()]

@api_router.post("/receipts/upload")
async def upload_receipt(file: UploadFile = File(...)):
    """Upload and analyze receipt image"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and encode image
        image_data = await file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Analyze receipt with Gemini
        logger.info("Starting receipt analysis with Gemini...")
        analysis = await receipt_analyzer.analyze_receipt(image_base64)
        
        # Create receipt object
        receipt = Receipt(
            merchant_name=analysis.merchant_name,
            total_amount=analysis.total_amount,
            date=datetime.fromisoformat(analysis.date),
            items=[item.model_dump() if isinstance(item, ReceiptItem) else item for item in analysis.items],
            category=analysis.category,
            image_base64=image_base64,
            analysis_text=f"Analysis complete for {analysis.merchant_name}",
            insights=analysis.insights,
            savings_suggestions=analysis.savings_suggestions
        )
        
        # Save to database
        receipt_ref = db.collection('receipts').document(receipt.id)
        receipt_ref.set(receipt.dict())
        append_to_csv('receipts', receipt.dict())
        
        # Create wallet pass
        wallet_pass = create_wallet_pass(receipt)
        wallet_pass_ref = db.collection('wallet_passes').document(wallet_pass.id)
        wallet_pass_ref.set(wallet_pass.dict())
        
        logger.info(f"Receipt analyzed successfully: {receipt.merchant_name}")
        
        # --- Nutrition summary and dietary insights (updated after upload) ---
        from nutrition_analysis import calculate_nutritional_summary, get_combined_dietary_insights
        receipts = [Receipt(**doc.to_dict()) for doc in db.collection('receipts').stream()]
        summary = calculate_nutritional_summary(receipts)
        dietary_insights = await get_combined_dietary_insights(summary)

        return {
            "success": True,
            "receipt": receipt.dict(),
            "wallet_pass": wallet_pass.dict(),
            "nutritional_summary": summary.dict() if hasattr(summary, 'dict') else summary.__dict__,
            "dietary_insights": dietary_insights,
            "message": "Receipt analyzed successfully!"
        }
        
    except Exception as e:
        logger.error(f"Receipt upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/receipts", response_model=List[Receipt])
async def get_receipts():
    """Get all receipts"""
    receipts_ref = db.collection('receipts')
    receipts_query = receipts_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(1000)
    return [Receipt(**doc.to_dict()) for doc in receipts_query.stream()]

@api_router.get("/receipts/{receipt_id}")
async def get_receipt(receipt_id: str):
    """Get specific receipt"""
    receipt_ref = db.collection('receipts').document(receipt_id)
    receipt_doc = receipt_ref.get()
    if not receipt_doc.exists:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return Receipt(**receipt_doc.to_dict())

@api_router.get("/insights", response_model=List[SpendingInsight])
async def get_insights():
    """Get spending insights"""
    # Get recent receipts
    receipts_ref = db.collection('receipts')
    receipts_query = receipts_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(100)
    receipts = [Receipt(**doc.to_dict()) for doc in receipts_query.stream()]
    
    # Generate insights
    insights = generate_insights(receipts)
    
    # Save insights to database
    for insight in insights:
        insight_ref = db.collection('insights').document(insight.id)
        insight_ref.set(insight.dict())
        append_to_csv('insights', insight.dict())
    
    return insights

@api_router.get("/dashboard")
async def get_dashboard():
    """Get dashboard data"""
    # Get recent receipts
    receipts_ref = db.collection('receipts')
    receipts_query = receipts_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(100)
    receipts = [Receipt(**doc.to_dict()) for doc in receipts_query.stream()]

    # Calculate statistics
    total_receipts = len(receipts)
    total_spending = sum(r.total_amount for r in receipts)

    # Category breakdown
    category_spending = {}
    for receipt in receipts:
        category_spending[receipt.category] = category_spending.get(receipt.category, 0) + receipt.total_amount

    # Recent activity
    recent_receipts = receipts[:5]  # Last 5 receipts

    # Generate insights (existing logic)
    insights = generate_insights(receipts)

    # --- Nutrition summary and dietary insights ---
    from nutrition_analysis import calculate_nutritional_summary, get_combined_dietary_insights
    summary = calculate_nutritional_summary(receipts)
    dietary_insights = await get_combined_dietary_insights(summary)

    return {
        "total_receipts": total_receipts,
        "total_spending": total_spending,
        "category_breakdown": category_spending,
        "recent_receipts": [r.dict() for r in recent_receipts],
        "insights": [i.dict() for i in insights],
        "nutritional_summary": summary.dict() if hasattr(summary, 'dict') else summary.__dict__,
        "dietary_insights": dietary_insights
    }

@api_router.get("/wallet-passes", response_model=List[WalletPass])
async def get_wallet_passes():
    """Get wallet passes"""
    passes_ref = db.collection('wallet_passes')
    passes_query = passes_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(1000)
    return [WalletPass(**doc.to_dict()) for doc in passes_query.stream()]

# Gmail Integration Endpoints
@api_router.post("/gmail/connect")
async def connect_gmail():
    """Simulate connecting Gmail account"""
    # In real implementation, this would handle OAuth flow
    gmail_connection = GmailConnection(
        user_email="user@gmail.com",
        connected=True,
        last_sync=datetime.utcnow(),
        total_emails_processed=0,
        auto_processing=True
    )
    
    # Save Gmail connection
    connection_ref = db.collection('gmail_connections').document(gmail_connection.user_email)
    connection_ref.set(gmail_connection.dict())
    append_to_csv('gmail_connections', gmail_connection.dict())
    
    return {
        "success": True,
        "message": "Gmail connected successfully! Email receipts will be processed automatically.",
        "connection": gmail_connection.dict()
    }

@api_router.get("/gmail/status")
async def get_gmail_status():
    """Get Gmail connection status"""
    connection_ref = db.collection('gmail_connections').document('user@gmail.com')
    connection_doc = connection_ref.get()
    
    if not connection_doc.exists:
        return {"connected": False, "message": "Gmail not connected"}
    
    # Get email receipts count
    email_receipts_ref = db.collection('email_receipts')
    email_receipts_count = len(list(email_receipts_ref.stream()))
    
    doc_dict = connection_doc.to_dict()
    return {
        "connected": doc_dict.get("connected", False),
        "last_sync": doc_dict.get("last_sync"),
        "total_emails_processed": email_receipts_count,
        "auto_processing": doc_dict.get("auto_processing", True)
    }

@api_router.post("/gmail/simulate-email")
async def simulate_incoming_email():
    """Simulate receiving an email receipt for demo purposes"""
    try:
        # Generate demo email
        demo_email = await gmail_demo_service.simulate_incoming_email()
        
        # Analyze email content with Gemini
        logger.info(f"Analyzing simulated email from {demo_email['sender']}")
        analysis = await gmail_analyzer.analyze_email_receipt(
            email_content=demo_email["content"],
            subject=demo_email["subject"],
            sender=demo_email["sender"]
        )
        
        # Create email receipt object
        email_receipt = EmailReceipt(
            email_id=demo_email["email_id"],
            sender=demo_email["sender"],
            subject=demo_email["subject"],
            received_date=demo_email["received_date"],
            email_content=demo_email["content"],
            merchant_name=analysis.merchant_name,
            total_amount=analysis.total_amount,
            items=analysis.items,  # Use items directly as dictionaries
            category=analysis.category,
            insights=analysis.insights,
            savings_suggestions=analysis.savings_suggestions,
            processed=True,
            source="email"
        )
        
        # Save to database
        email_receipt_ref = db.collection('email_receipts').document(email_receipt.email_id)
        email_receipt_ref.set(email_receipt.dict())
        append_to_csv('email_receipts', email_receipt.dict())
        
        # Create wallet pass for email receipt
        wallet_pass = WalletPass(
            title=f"{email_receipt.merchant_name} - Email Receipt",
            description=f"Auto-processed from email: ${email_receipt.total_amount:.2f}",
            amount=email_receipt.total_amount,
            category=email_receipt.category,
            merchant=email_receipt.merchant_name,
            date=email_receipt.received_date
        )
        wallet_pass_ref = db.collection('wallet_passes').document(wallet_pass.id)
        wallet_pass_ref.set(wallet_pass.dict())
        
        # Update Gmail connection stats
        connection_ref = db.collection('gmail_connections').document('user@gmail.com')
        # Fetch current value for total_emails_processed
        connection_doc = connection_ref.get()
        doc_dict = connection_doc.to_dict() if connection_doc.exists else {}
        total_emails_processed = doc_dict.get("total_emails_processed", 0) + 1
        connection_ref.update({
            "total_emails_processed": total_emails_processed,
            "last_sync": datetime.utcnow()
        })
        
        logger.info(f"Email receipt processed successfully: {email_receipt.merchant_name}")
        
        return {
            "success": True,
            "message": f"Email receipt from {email_receipt.merchant_name} processed automatically!",
            "email_receipt": email_receipt.dict(),
            "wallet_pass": wallet_pass.dict(),
            "processing_time": "< 2 seconds"
        }
        
    except Exception as e:
        logger.error(f"Email simulation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/gmail/email-receipts", response_model=List[EmailReceipt])
async def get_email_receipts():
    """Get all processed email receipts"""
    email_receipts_ref = db.collection('email_receipts')
    email_receipts_query = email_receipts_ref.order_by('received_date', direction=firestore.Query.DESCENDING).limit(1000)
    return [EmailReceipt(**doc.to_dict()) for doc in email_receipts_query.stream()]

@api_router.get("/gmail/email-receipts/{email_id}")
async def get_email_receipt(email_id: str):
    """Get specific email receipt"""
    email_receipt_ref = db.collection('email_receipts').document(email_id)
    email_receipt_doc = email_receipt_ref.get()
    if not email_receipt_doc.exists:
        raise HTTPException(status_code=404, detail="Email receipt not found")
    return EmailReceipt(**email_receipt_doc.to_dict())

@api_router.post("/gmail/auto-process")
async def toggle_auto_processing():
    """Toggle automatic email processing"""
    connection_ref = db.collection('gmail_connections').document('user@gmail.com')
    connection_doc = connection_ref.get()
    
    if not connection_doc.exists:
        raise HTTPException(status_code=404, detail="Gmail not connected")
    
    doc_dict = connection_doc.to_dict()
    new_status = not doc_dict.get("auto_processing", True)
    
    connection_ref.update({"auto_processing": new_status})
    
    return {
        "success": True,
        "auto_processing": new_status,
        "message": f"Auto-processing {'enabled' if new_status else 'disabled'}"
    }

@api_router.get("/dashboard/enhanced")
async def get_enhanced_dashboard():
    """Get enhanced dashboard with email receipts data"""
    # Get regular receipts
    receipts_ref = db.collection('receipts')
    receipts_query = receipts_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(100)


    receipts = [Receipt(**parse_receipt_dict(doc.to_dict())) for doc in receipts_query.stream()]
    
    # Get email receipts
    email_receipts_ref = db.collection('email_receipts')
    email_receipts_query = email_receipts_ref.order_by('received_date', direction=firestore.Query.DESCENDING).limit(100)
    email_receipts = [EmailReceipt(**parse_receipt_dict(doc.to_dict())) for doc in email_receipts_query.stream()]
    
    # Combine for analytics
    total_receipts = len(receipts) + len(email_receipts)
    total_spending = sum(r.total_amount for r in receipts) + sum(r.total_amount for r in email_receipts)
    
    # Category breakdown (combined)
    category_spending = {}
    for receipt in receipts + email_receipts:
        category_spending[receipt.category] = category_spending.get(receipt.category, 0) + receipt.total_amount
    
    # Email processing stats
    gmail_status = await get_gmail_status()
    
    # Recent activity (combined, sorted by date)
    all_receipts = []
    for r in receipts:
        all_receipts.append({
            **r.dict(),
            "source": "manual",
            "date_for_sorting": r.created_at
        })
    for r in email_receipts:
        all_receipts.append({
            **r.dict(),
            "source": "email",
            "date_for_sorting": r.received_date
        })
    
    # Sort by date and take top 10
    all_receipts.sort(key=lambda x: x["date_for_sorting"], reverse=True)
    recent_receipts = all_receipts[:10]
    
    # Generate insights
    combined_receipts = receipts + email_receipts
    insights = generate_insights(combined_receipts)
    
    # --- Nutrition summary breakdown: latest, weekly, monthly ---
    from nutrition_analysis import calculate_nutritional_summary, get_combined_dietary_insights
    import datetime
    now = datetime.datetime.utcnow()

    # Helper to filter receipts by date
    def filter_by_days(receipts, days):
        cutoff = now - datetime.timedelta(days=days)
        # Make cutoff naive for comparison
        if hasattr(cutoff, 'tzinfo') and cutoff.tzinfo is not None:
            cutoff = cutoff.replace(tzinfo=None)
        filtered = []
        for r in receipts:
            date_val = getattr(r, 'created_at', None) or getattr(r, 'received_date', None)
            if date_val:
                if hasattr(date_val, 'tzinfo') and date_val.tzinfo is not None:
                    date_val = date_val.replace(tzinfo=None)
                if date_val >= cutoff:
                    filtered.append(r)
        return filtered

    # Latest receipt (most recent manual or email)
    latest_receipt = None
    if len(all_receipts) > 0:
        latest_receipt_data = all_receipts[0]
        # Rebuild a Receipt/EmailReceipt object from dict
        if latest_receipt_data['source'] == 'manual':
            latest_receipt = Receipt(**{k: v for k, v in latest_receipt_data.items() if k in Receipt.__fields__})
        else:
            latest_receipt = EmailReceipt(**{k: v for k, v in latest_receipt_data.items() if k in EmailReceipt.__fields__})
    nutrition_latest = calculate_nutritional_summary([latest_receipt]) if latest_receipt else None
    # Weekly/monthly
    last7 = filter_by_days(receipts + email_receipts, 7)
    last30 = filter_by_days(receipts + email_receipts, 30)
    nutrition_week = calculate_nutritional_summary(last7) if last7 else None
    nutrition_month = calculate_nutritional_summary(last30) if last30 else None

    # Dietary insights for monthly summary
    try:
        dietary_insights = await get_combined_dietary_insights(nutrition_month)
    except Exception as e:
        logger.error(f"[GEMINI ERROR] Dietary insights: {e}")
        dietary_insights = {'current': ["AI error: could not generate insights"], 'historical': []}

    logger.info(f"[DASHBOARD ENHANCED] Nutrition latest: {nutrition_latest.dict() if nutrition_latest else None}")
    logger.info(f"[DASHBOARD ENHANCED] Nutrition week: {nutrition_week.dict() if nutrition_week else None}")
    logger.info(f"[DASHBOARD ENHANCED] Nutrition month: {nutrition_month.dict() if nutrition_month else None}")
    logger.info(f"[DASHBOARD ENHANCED] Dietary insights: {dietary_insights}")

    return {
        "total_receipts": total_receipts,
        "manual_receipts": len(receipts),
        "email_receipts": len(email_receipts),
        "total_spending": total_spending,
        "category_breakdown": category_spending,
        "recent_receipts": recent_receipts,
        "insights": [i.dict() for i in insights],
        "gmail_integration": gmail_status,
        "automation_savings": {
            "time_saved_hours": len(email_receipts) * 0.05,  # 3 minutes per receipt
            "emails_processed": len(email_receipts),
            "accuracy_rate": "95%"
        },
        "nutrition": {
            "latest": nutrition_latest.formatted_dict() if nutrition_latest else None,
            "weekly": nutrition_week.formatted_dict() if nutrition_week else None,
            "monthly": nutrition_month.formatted_dict() if nutrition_month else None
        },
        "dietary_insights": dietary_insights
    }

# Include the router in the main app
app.include_router(api_router, prefix="/api")

origins = [
    "http://localhost:3001",
    "https://financialagent-109221590536.europe-west1.run.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)