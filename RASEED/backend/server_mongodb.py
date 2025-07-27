from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
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
# Add the path to emergentintegrations if it's in backend/emergentintegrations
sys.path.append(str(Path(__file__).parent / "emergentintegrations"))

# Gemini Integration
from emergentintegrations.llm.chat import LlmChat

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
# app = FastAPI()

app = FastAPI(lifespan=lifespan)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models
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

# ... rest of the MongoDB version code ...
