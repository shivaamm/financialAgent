# Agentic Features Implementation Record

This file tracks all agentic (AI-driven, autonomous) enhancements added to the project, including real-time data integrations and decision-making logic.

## [2025-07-22] Real-Time Grocery Store Recommendation Agent

**Features:**
- Integrates with (unofficial) JioMart and BigBasket APIs to fetch real-time grocery prices and availability for India.
- Uses Google Maps Places API to find nearby stores and fetch directions.
- Agentic backend function recommends the best 2 stores for a user's grocery list, comparing price, availability, and distance.
- Returns Google Maps links for store directions.

**Files Created:**
- `backend/store_recommendation.py`: Module containing all logic for fetching, comparing, and recommending stores and prices.
- `backend/AGENTIC_RECORD.md`: This record file.

**How It Works:**
- After receipt upload and item extraction, the agent automatically queries APIs, compares results, and returns actionable recommendations to the user—no manual intervention required.

**Next Steps:**
- Expose this logic via a backend API endpoint.
- Update the frontend to display recommendation cards with price, store, and directions.

---

This record will be updated as more agentic/autonomous features are added.
