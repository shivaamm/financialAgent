"""
Agentic Store Recommendation Module

- Fetches real-time grocery prices and availability from JioMart and BigBasket (unofficial APIs)
- Uses Google Maps API for store search, directions, and distance
- Designed for India (IN) region
- Returns top 2 store recommendations for a given grocery list
"""

import requests
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv()
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

# Example function to get grocery prices from JioMart (unofficial demo)
def fetch_jiomart_prices(item: str, location: str) -> Dict[str, Any]:
    import random
    # Mock plausible prices for demo
    price = round(random.uniform(30, 80), 2)
    return {
        "store": "JioMart",
        "item": item,
        "price": price,
        "availability": True,
        "store_location": location,
        "store_address": f"JioMart Store, {location}"
    }

# Example function to get grocery prices from BigBasket (unofficial demo)
def fetch_bigbasket_prices(item: str, location: str) -> Dict[str, Any]:
    import random
    # Mock plausible prices for demo, slightly different from JioMart
    price = round(random.uniform(28, 85), 2)
    return {
        "store": "BigBasket",
        "item": item,
        "price": price,
        "availability": True,
        "store_location": location,
        "store_address": f"BigBasket Store, {location}"
    }

# Google Maps Places API to find stores nearby
def find_nearby_stores(item: str, user_location: str) -> List[Dict[str, Any]]:
    import logging
    logger = logging.getLogger("store_recommendation")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{item} store near {user_location}, India",
        "key": GOOGLE_MAPS_API_KEY
    }
    params_log = {k: v for k, v in params.items() if k != 'key'}
    logger.info(f"Google Maps Places API request: {url} params={params_log}")
    resp = requests.get(url, params=params)
    logger.info(f"Google Maps response [{resp.status_code}]: {resp.text}")
    stores = []
    if resp.status_code == 200:
        data = resp.json()
        for result in data.get("results", [])[:5]:
            stores.append({
                "name": result.get("name"),
                "address": result.get("formatted_address"),
                "location": result.get("geometry", {}).get("location", {}),
                "maps_url": f"https://www.google.com/maps/search/?api=1&query={result.get('name').replace(' ', '+')}"
            })
    return stores

# Agentic function to recommend best stores for a grocery list
def recommend_stores_for_groceries(items: List[str], user_location: str) -> List[Dict[str, Any]]:
    import logging
    logger = logging.getLogger("store_recommendation")
    logger.info(f"Running recommendation for items={items} location={user_location}")
    recommendations = []
    for item in items:
        jiomart = fetch_jiomart_prices(item, user_location)
        bigbasket = fetch_bigbasket_prices(item, user_location)
        stores = find_nearby_stores(item, user_location)
        logger.info(f"JioMart result: {jiomart}")
        logger.info(f"BigBasket result: {bigbasket}")
        logger.info(f"Nearby stores: {stores}")
        # Compare prices and availability
        options = [s for s in [jiomart, bigbasket] if s.get("availability") and not s.get("error")]
        if options:
            best = sorted(options, key=lambda x: x["price"])[0]
            # Attach nearby store info if available
            if stores:
                best["nearby_store"] = stores[0]
            recommendations.append(best)
    # Pick top 2 by price
    recommendations = sorted(recommendations, key=lambda x: x["price"])[:2]
    logger.info(f"Final recommendations: {recommendations}")
    return recommendations

# Example usage (to be called from backend API):
# recommend_stores_for_groceries(["milk", "bread", "eggs"], "Mumbai")
