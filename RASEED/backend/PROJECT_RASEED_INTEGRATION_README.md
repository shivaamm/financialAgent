# Project Raseed: Integration Vision & Implementation Notes

## Google Wallet Integration Vision

**Project Raseed** aims to be a comprehensive AI-powered receipt manager and financial assistant, providing users with actionable insights, spending analysis, and savings suggestions—all accessible via a web dashboard and, for convenience, as Google Wallet passes.

### How Web & Wallet Work Together
- **Web App (React + Python):**
  - The main platform for uploading receipts, viewing full AI insights, querying spending, and exploring recommendations.
  - Offers rich, interactive dashboards, charts, and query capabilities.
- **Google Wallet Passes:**
  - Serve as "portable summaries" of key insights, shopping lists, or alerts.
  - Passes are accessible on the user's phone (Google Wallet app), even offline.
  - Each pass can contain:
    - A summary of recent spending, tips, or a shopping list.
    - A deep link back to the web app for full details or uploading new receipts.
    - Push notifications (optional, via Google Wallet API) for important updates.

### What Can Be Shown in the Wallet Pass?
- A concise summary of the most important insights (e.g., "Groceries: ₹2,000 this month. Top tip: Try Dmart.").
- A list of recent items or a shopping list (as text in the pass details).
- A deep link to your web app for uploading new receipts or viewing the full dashboard.
- **Limitations:** No charts, graphs, or interactive dashboards—just text, numbers, and links.

### Uploading Receipts from Phone
- Users can upload receipts directly from the mobile web version of your app (ensure responsive design).
- You can include a link (in the Wallet pass) that opens the web upload page on their phone.
- No native app is required—mobile web is sufficient for uploads and basic interactions.

### Practical Implementation Notes
- Backend generates passes with the latest insights and upload links after each receipt analysis.
- Frontend displays an "Add to Google Wallet" button after analysis/upload.
- All rich insights and analytics remain in the web app; the Wallet pass is a convenient extension.

---

# Deploying Project Raseed to Google Cloud Run (from GitHub)

## Deployment Options

You can deploy your backend and frontend to Cloud Run using either:
- **Container Image:** Build and push a Docker image, then deploy manually.
- **GitHub Integration:** Connect your GitHub repo for continuous deployment (push-to-deploy).

### Container Image
- Build Docker image locally or in the cloud.
- Push to Google Artifact Registry or Docker Hub.
- Deploy to Cloud Run using the image.
- Manual process: re-build, re-push, and re-deploy after every change.

### GitHub (Recommended for CI/CD)
- Connect your GitHub repo to Cloud Run.
- Every push to the selected branch triggers an automatic build and deployment via Cloud Build.
- No need to manually build or push images after setup.

## What You Need for GitHub Deployment
- **A GitHub repository** with your code and a Dockerfile (in backend/frontend folders as needed).
- **A Google Cloud project** with Cloud Run and Cloud Build APIs enabled.
- **Permissions**: Owner/Editor or Cloud Run Admin + Cloud Build Editor.
- **GitHub ↔ GCP connection**: Set up once via the GCP Console.
- **(Optional) Environment variables/secrets**: Set in Cloud Run or Secret Manager.

## Step-by-Step: Deploy from GitHub
1. Push your code (with Dockerfile) to GitHub.
2. In the GCP Console: Go to Cloud Run > Create Service > Select GitHub option.
3. Authorize Google Cloud to access your GitHub repo.
4. Select the repo and branch to deploy.
5. Configure build settings (Dockerfile path, env vars, etc.).
6. Complete the setup. Cloud Build will build and deploy on every push.
7. Cloud Run will generate a public HTTPS URL for your service, accessible from anywhere.

## Checklist
| Item                       | Required? | Notes                                  |
|----------------------------|-----------|----------------------------------------|
| GitHub repo                | Yes       | Code + Dockerfile                      |
| GCP project                | Yes       | Already created                        |
| Cloud Run & Build enabled  | Yes       | `gcloud services enable ...`           |
| Dockerfile                 | Yes       | In service folder                      |
| GitHub ↔ GCP connection    | Yes       | One-time setup in GCP Console          |
| Env vars/secrets           | Optional  | Set in Cloud Run or Secret Manager     |
| Custom domain              | Optional  | Set after deploy                       |

## FAQ
- **Do I need to use the GCP Console UI?**
  - Only for the initial GitHub connection and setup. After that, deployments happen automatically on git push.
- **How do I update my app after changes?**
  - Just push to GitHub! Cloud Build will rebuild and redeploy.
- **Will I get a public URL?**
  - Yes, every Cloud Run service gets a public HTTPS URL, accessible from any device.

---

# Scraping & API Integration Notes

## Amazon Product Advertising API (PAAPI)
- Requires Amazon Associates account (not AWS IAM keys).
- Keys are available in the Associates dashboard under Tools > Product Advertising API.
- Sometimes requires 3 qualifying sales before API keys are issued.
- Used for official product/price data from Amazon.

## Flipkart Affiliate API
- Affiliate API is deprecated/restricted for new accounts.
- Most new affiliates do not get API access.
- If API keys are not visible in your dashboard, you do not have access.
- Unofficial APIs/scraping are alternatives (use with caution).

## Dmart, Blinkit, Zepto, BigBasket, JioMart
- No official public APIs for product search or price data.
- Data can only be obtained via scraping (not recommended for production).

## ScraperAPI
- [https://docs.scraperapi.com/python/](https://docs.scraperapi.com/python/)
- Proxy service for scraping real-time data from sites like Amazon, Flipkart, Blinkit, Zepto, etc.
- Handles IP rotation, CAPTCHAs, and anti-bot measures.
- Returns raw HTML; you must parse it (e.g., with BeautifulSoup).
- Example usage:

```python
from scraperapi import ScraperAPIClient
from bs4 import BeautifulSoup

client = ScraperAPIClient('YOUR_SCRAPERAPI_KEY')
result = client.get('https://www.amazon.in/s?k=iphone')
soup = BeautifulSoup(result.text, 'html.parser')
# Parse soup for product info
```

## Integration Plan
- After extracting product names from receipts, search each item on relevant sites.
- Use ScraperAPI to fetch search result pages.
- Parse HTML for product title, price, link, etc.
- Compare results across sites and present best deals.
- Keep parsing logic modular for each site (selectors may change).

## Legal & Practical Considerations
- Always check and comply with each site's terms of service.
- Scraping is best for prototyping, not production.
- For commercial use, seek partnerships or official APIs where possible.

---

**To-Do:**
- [ ] Get Amazon PAAPI keys (after qualifying sales if needed)
- [ ] Monitor Flipkart affiliate API status
- [ ] Prototype ScraperAPI-based product search for Amazon
- [ ] Add modular parsers for Flipkart, Blinkit, Zepto, etc.
- [ ] Integrate real-time comparison in backend recommendation logic
