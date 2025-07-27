# 🏗️ Project Raseed - System Architecture

## 🎯 **Architecture Overview**

Project Raseed follows a **microservices-inspired architecture** with clear separation of concerns, enabling scalability and maintainability.

## 🌐 **System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PROJECT RASEED ECOSYSTEM                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           USER INTERFACE LAYER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │   Upload    │  │  Dashboard  │  │   Wallet    │  │  Settings   │      │ │
│  │  │     📸      │  │     📊      │  │     🎫      │  │     ⚙️      │      │ │
│  │  │  Component  │  │  Analytics  │  │   Passes    │  │   Config    │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                      React 19 + Tailwind CSS                           │ │ │
│  │  │                     Progressive Web App (PWA)                          │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                          │
│                                        │ HTTP/REST API                            │
│                                        │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                             API GATEWAY LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                           FastAPI Server                               │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │ │
│  │  │  │   Receipt   │  │  Dashboard  │  │   Wallet    │  │   Status    │  │ │ │
│  │  │  │   Routes    │  │   Routes    │  │   Routes    │  │   Routes    │  │ │ │
│  │  │  │   📄 /api   │  │   📊 /api   │  │   🎫 /api   │  │   ✓ /api    │  │ │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │ │
│  │  │  │                      Middleware Stack                              │ │ │ │
│  │  │  │  • CORS Handling    • Request Validation    • Error Handling      │ │ │ │
│  │  │  │  • Authentication   • Rate Limiting         • Logging             │ │ │ │
│  │  │  └─────────────────────────────────────────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                          │
│                                        │ Service Calls                            │
│                                        │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           INTELLIGENCE LAYER                               │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                          AI Services                                   │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │ │
│  │  │  │   Gemini    │  │  Predictive │  │   Insight   │  │ Notification│  │ │ │
│  │  │  │   Vision    │  │   Engine    │  │   Engine    │  │   Engine    │  │ │ │
│  │  │  │   🤖 OCR    │  │   🔮 ML     │  │   💡 Rules  │  │   📢 Alerts │  │ │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │ │
│  │  │  │                    AI Processing Pipeline                          │ │ │ │
│  │  │  │                                                                     │ │ │ │
│  │  │  │  Receipt → Vision AI → Data Extract → Pattern Analysis →           │ │ │ │
│  │  │  │  Insight Generation → Recommendation Engine → Action Triggers      │ │ │ │
│  │  │  └─────────────────────────────────────────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                          │
│                                        │ Data Operations                          │
│                                        │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                    │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │   MongoDB   │  │   Google    │  │  External   │  │    Cache    │      │ │
│  │  │  Database   │  │   Wallet    │  │    APIs     │  │    Layer    │      │ │
│  │  │   💾 NoSQL  │  │   🎫 API    │  │   🌐 HTTP   │  │   ⚡ Redis  │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                        Data Collections                                │ │ │
│  │  │                                                                         │ │ │
│  │  │  • receipts          • insights           • wallet_passes             │ │ │
│  │  │  • status_checks     • user_preferences   • ai_training_data          │ │ │
│  │  │  • spending_patterns • merchant_data      • prediction_models         │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 **Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW PIPELINE                                │
│                                                                                 │
│  📸 User Upload                                                                 │
│       │                                                                         │
│       ├─ Image Validation ─────────────────────────┐                           │
│       │                                            │                           │
│       ├─ Base64 Encoding ──────────────────────────┼─ Store in MongoDB         │
│       │                                            │                           │
│       └─ Send to Gemini AI ────────────────────────┘                           │
│                │                                                               │
│  🤖 AI Processing                                                               │
│       │                                                                         │
│       ├─ Vision OCR ────────────────────────────────┐                          │
│       │                                            │                           │
│       ├─ Data Extraction ──────────────────────────┼─ Structured Data          │
│       │                                            │                           │
│       ├─ Category Classification ───────────────────┼─ Smart Categorization     │
│       │                                            │                           │
│       └─ Insight Generation ────────────────────────┘                          │
│                │                                                               │
│  💾 Data Storage                                                                │
│       │                                                                         │
│       ├─ Receipt Document ─────────────────────────┐                           │
│       │                                            │                           │
│       ├─ Spending Analytics ────────────────────────┼─ MongoDB Collections      │
│       │                                            │                           │
│       └─ User Insights ────────────────────────────┘                           │
│                │                                                               │
│  📊 Analytics Processing                                                        │
│       │                                                                         │
│       ├─ Pattern Analysis ─────────────────────────┐                           │
│       │                                            │                           │
│       ├─ Trend Identification ──────────────────────┼─ Predictive Models       │
│       │                                            │                           │
│       └─ Recommendation Engine ────────────────────┘                           │
│                │                                                               │
│  🎫 Wallet Pass Generation                                                      │
│       │                                                                         │
│       ├─ Pass Data Creation ───────────────────────┐                           │
│       │                                            │                           │
│       ├─ Google Wallet Integration ─────────────────┼─ Dynamic Passes          │
│       │                                            │                           │
│       └─ Notification Triggers ───────────────────┘                           │
│                │                                                               │
│  📱 User Interface Update                                                       │
│       │                                                                         │
│       ├─ Dashboard Refresh ────────────────────────┐                           │
│       │                                            │                           │
│       ├─ Insight Display ──────────────────────────┼─ Real-time Updates        │
│       │                                            │                           │
│       └─ Notification Delivery ───────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🧠 **AI Intelligence Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AI INTELLIGENCE STACK                               │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          INPUT PROCESSING                                  │ │
│  │                                                                             │ │
│  │  📸 Receipt Image                                                           │ │
│  │       │                                                                     │ │
│  │       ├─ Image Preprocessing ─────────────────────────────────────────────── │ │
│  │       │   • Noise Reduction    • Contrast Enhancement                      │ │
│  │       │   • Rotation Correction • Size Optimization                       │ │
│  │       │                                                                     │ │
│  │       └─ Format Standardization ─────────────────────────────────────────── │ │
│  │           • Base64 Encoding    • Metadata Extraction                       │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        GEMINI AI PROCESSING                                │ │
│  │                                                                             │ │
│  │  🤖 Gemini 2.0 Flash Vision                                                 │ │
│  │       │                                                                     │ │
│  │       ├─ OCR Engine ─────────────────────────────────────────────────────── │ │
│  │       │   • Text Recognition   • Handwriting Support                       │ │
│  │       │   • Multi-language     • Format Detection                          │ │
│  │       │                                                                     │ │
│  │       ├─ Contextual Understanding ─────────────────────────────────────────── │ │
│  │       │   • Merchant Recognition • Item Classification                     │ │
│  │       │   • Price Validation    • Date Parsing                            │ │
│  │       │                                                                     │ │
│  │       └─ Intelligent Extraction ─────────────────────────────────────────── │ │
│  │           • Structured Data     • Confidence Scoring                       │ │
│  │           • Error Detection     • Quality Assessment                       │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        INTELLIGENCE ENGINES                                │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    PATTERN ANALYSIS ENGINE                             │ │ │
│  │  │                                                                         │ │ │
│  │  │  📈 Spending Patterns                                                   │ │ │
│  │  │       │                                                                 │ │ │
│  │  │       ├─ Temporal Analysis ─────────────────────────────────────────────── │ │ │
│  │  │       │   • Daily/Weekly/Monthly Trends                                │ │ │ │
│  │  │       │   • Seasonal Variations                                        │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       ├─ Category Analysis ─────────────────────────────────────────────── │ │ │
│  │  │       │   • Food vs Non-Food     • Necessity vs Luxury                 │ │ │ │
│  │  │       │   • Merchant Preferences • Brand Loyalty                      │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       └─ Behavioral Analysis ────────────────────────────────────────────── │ │ │
│  │  │           • Impulse Purchases    • Bulk Buying Patterns               │ │ │ │
│  │  │           • Location-based Spending • Time-based Habits               │ │ │ │
│  │  │                                                                         │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    PREDICTIVE ENGINE                                   │ │ │
│  │  │                                                                         │ │ │
│  │  │  🔮 Future Insights                                                     │ │ │
│  │  │       │                                                                 │ │ │
│  │  │       ├─ Consumption Forecasting ────────────────────────────────────────── │ │ │
│  │  │       │   • When you'll need items   • Quantity predictions            │ │ │ │
│  │  │       │   • Seasonal adjustments     • Usage pattern analysis         │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       ├─ Price Prediction ─────────────────────────────────────────────────── │ │ │
│  │  │       │   • Market trend analysis    • Seasonal price changes         │ │ │ │
│  │  │       │   • Optimal purchase timing  • Bulk buying recommendations    │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       └─ Budget Optimization ────────────────────────────────────────────── │ │ │
│  │  │           • Dynamic budget allocation • Spending limit suggestions     │ │ │ │
│  │  │           • Emergency fund planning   • Savings goal optimization      │ │ │ │
│  │  │                                                                         │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    RECOMMENDATION ENGINE                               │ │ │
│  │  │                                                                         │ │ │
│  │  │  💡 Intelligent Suggestions                                             │ │ │
│  │  │       │                                                                 │ │ │
│  │  │       ├─ Savings Opportunities ────────────────────────────────────────────── │ │ │
│  │  │       │   • Cheaper alternatives     • Bulk buying benefits           │ │ │ │
│  │  │       │   • Loyalty program usage    • Cashback optimization          │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       ├─ Health & Wellness ──────────────────────────────────────────────── │ │ │
│  │  │       │   • Nutritional insights     • Healthy alternatives           │ │ │ │
│  │  │       │   • Portion size analysis    • Dietary trend tracking         │ │ │ │
│  │  │       │                                                                 │ │ │ │
│  │  │       └─ Sustainability Impact ──────────────────────────────────────────── │ │ │
│  │  │           • Carbon footprint analysis • Eco-friendly alternatives      │ │ │ │
│  │  │           • Local sourcing benefits  • Packaging waste reduction      │ │ │ │
│  │  │                                                                         │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🛠️ **TECHNICAL SPECIFICATIONS**

### **Backend Architecture**
```python
# Core Technologies
- FastAPI: High-performance async API
- MongoDB: Document-based storage
- Google Gemini AI: Advanced vision and reasoning
- Motor: Async MongoDB driver
- Pydantic: Data validation and serialization

# AI Integration
- emergentintegrations: Unified LLM interface
- Gemini 2.0 Flash: Latest vision model
- Custom prompt engineering for receipt analysis
- Predictive analytics pipeline
```

### **Frontend Architecture**
```javascript
// Core Technologies
- React 19: Modern UI framework
- Tailwind CSS: Utility-first styling
- Axios: HTTP client
- React Router: Client-side routing

// UI/UX Features
- Responsive design
- Drag-and-drop file upload
- Real-time updates
- Progressive Web App capabilities
```

### **Database Schema**
```javascript
// Collections
receipts: {
  id: UUID,
  merchant_name: String,
  total_amount: Number,
  items: [ReceiptItem],
  category: String,
  image_base64: String,
  insights: [String],
  savings_suggestions: [String],
  created_at: DateTime
}

insights: {
  id: UUID,
  title: String,
  description: String,
  category: String,
  suggestion: String,
  type: String, // warning, tip, achievement
  created_at: DateTime
}

wallet_passes: {
  id: UUID,
  title: String,
  description: String,
  merchant: String,
  amount: Number,
  status: String,
  created_at: DateTime
}
```

This comprehensive architecture documentation provides a complete technical overview of Project Raseed's innovative approach to receipt management and financial intelligence.