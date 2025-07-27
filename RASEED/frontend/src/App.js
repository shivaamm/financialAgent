import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import Chatbot from "./Chatbot";

// const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8080";
const BACKEND_URL = "https://agenticai-109221590536.europe-west1.run.app";
const API = `${BACKEND_URL}/api`;


class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  componentDidCatch(error, errorInfo) {
    // log error if needed
  }
  render() {
    if (this.state.hasError) {
      return <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow">Chatbot failed to load.</div>;
    }
    return this.props.children;
  }
}

// Components
const GmailIntegration = ({ gmailStatus, onConnect, onSimulateEmail }) => {
  const [connecting, setConnecting] = useState(false);
  const [simulating, setSimulating] = useState(false);

  const handleConnect = async () => {
    setConnecting(true);
    await onConnect();
    setConnecting(false);
  };

  const handleSimulateEmail = async () => {
    setSimulating(true);
    await onSimulateEmail();
    setSimulating(false);
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          📧 Gmail Integration
        </h2>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          gmailStatus?.connected 
            ? 'bg-green-100 text-green-800' 
            : 'bg-gray-100 text-gray-600'
        }`}>
          {gmailStatus?.connected ? '✅ Connected' : '⚪ Not Connected'}
        </div>
      </div>

      {!gmailStatus?.connected ? (
        <div className="text-center py-6">
          <div className="text-4xl mb-4">📮</div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Connect Your Gmail
          </h3>
          <p className="text-gray-500 mb-4">
            Automatically process email receipts from your inbox
          </p>
          <button
            onClick={handleConnect}
            disabled={connecting}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 transition-colors"
          >
            {connecting ? 'Connecting...' : '🔗 Connect Gmail'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {gmailStatus.total_emails_processed}
              </div>
              <div className="text-sm text-blue-600">Emails Processed</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">Auto</div>
              <div className="text-sm text-green-600">Processing Active</div>
            </div>
          </div>

          <div className="border-t pt-4">
            <h4 className="font-semibold text-gray-700 mb-2">Demo Email Processing</h4>
            <p className="text-sm text-gray-500 mb-3">
              Simulate receiving an email receipt to see automatic processing in action
            </p>
            <button
              onClick={handleSimulateEmail}
              disabled={simulating}
              className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:from-green-600 hover:to-blue-600 disabled:opacity-50 transition-colors"
            >
              {simulating ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Processing Email...</span>
                </div>
              ) : (
                '📨 Simulate Email Receipt'
              )}
            </button>
          </div>

          {gmailStatus.last_sync && (
            <div className="text-xs text-gray-500 text-center">
              Last sync: {new Date(gmailStatus.last_sync).toLocaleString()}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const EmailReceiptsList = ({ emailReceipts }) => {
  // [CASCADE FIX] Log data for debugging
  console.log('[EmailReceiptsList] emailReceipts:', emailReceipts);
  if (!Array.isArray(emailReceipts) || emailReceipts.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
        <div className="text-6xl mb-4">📧</div>
        <div className="text-xl font-semibold text-gray-700">No Email Receipts Yet</div>
        <div className="text-gray-500 mt-2">Connect Gmail to start automatic processing!</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-800">📧 Email Receipts</h2>
      <div className="space-y-3">
        {emailReceipts.map((receipt, index) => (
          <div key={index} className="bg-white rounded-lg p-4 shadow-md border border-gray-100">
            <div className="flex justify-between items-start mb-2">
              <div>
                <div className="font-semibold text-gray-800 flex items-center">
                  <span className="mr-2">📧</span>
                  {receipt.merchant_name}
                </div>
                <div className="text-sm text-gray-500">
                  From: {receipt.sender}
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(receipt.received_date).toLocaleString()}
                </div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-gray-800">
                  ${receipt.total_amount.toFixed(2)}
                </div>
                <div className="text-sm text-gray-500">{receipt.category}</div>
                <div className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full mt-1">
                  Auto-processed
                </div>
              </div>
            </div>
            
            {receipt.items && receipt.items.length > 0 && (
              <div className="border-t pt-2 mt-2">
                <div className="text-xs text-gray-500 mb-1">Items:</div>
                <div className="space-y-1">
                  {/* [CASCADE FIX] Defensive .map check for receipt.items */}
{/* [CASCADE FIX] Defensive .map and .toFixed for receipt.items */}
{Array.isArray(receipt.items)
  ? receipt.items.slice(0, 3).map((item, idx) => (
      <div key={idx} className="flex justify-between text-sm">
        <span>{item && item.name ? item.name : 'N/A'}</span>
        <span>
          {item && typeof item.price === 'number' ? `$${item.price.toFixed(2)}` : 'N/A'}
        </span>
      </div>
    ))
  : null}
                  {receipt.items.length > 3 && (
                    <div className="text-xs text-gray-400">
                      +{receipt.items.length - 3} more items
                    </div>
                  )}
                </div>
              </div>
            )}

            {receipt.insights && receipt.insights.length > 0 && (
              <div className="border-t pt-2 mt-2">
                <div className="text-xs text-gray-500 mb-1">AI Insights:</div>
                <div className="text-sm text-blue-600">
                  💡 {receipt.insights[0]}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

const ReceiptUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API}/receipts/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      if (response.data.success) {
        onUploadSuccess(response.data);
        setFile(null);
        setPreview(null);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        📄 Upload Receipt
      </h2>
      
      <div className="space-y-6">
        {preview && (
          <div className="text-center">
            <img 
              src={preview} 
              alt="Receipt preview" 
              className="max-w-xs mx-auto rounded-lg shadow-md"
            />
          </div>
        )}
        
        <div className="relative">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="receipt-upload"
          />
          <label
            htmlFor="receipt-upload"
            className="block w-full p-6 border-2 border-dashed border-gray-300 rounded-lg text-center hover:border-blue-500 hover:bg-blue-50 cursor-pointer transition-colors"
          >
            <div className="space-y-2">
              <div className="text-4xl">📸</div>
              <div className="text-lg font-medium text-gray-700">
                {file ? file.name : 'Click to select receipt image'}
              </div>
              <div className="text-sm text-gray-500">
                PNG, JPG, or other image formats
              </div>
            </div>
          </label>
        </div>
        
        {file && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Analyzing with AI...</span>
              </div>
            ) : (
              '🚀 Analyze Receipt'
            )}
          </button>
        )}
      </div>
    </div>
  );
};

const Dashboard = ({ dashboardData, storeRecommendations }) => {
  // [CASCADE FIX] Log data for debugging
  console.log('[Dashboard] dashboardData:', dashboardData);
  if (!dashboardData) return null;

  const { 
    total_receipts, 
    manual_receipts = 0,
    email_receipts = 0,
    total_spending, 
    category_breakdown, 
    recent_receipts, 
    insights,
    gmail_integration,
    automation_savings
  } = dashboardData;

  return (
    <div className="space-y-6">
      {/* Enhanced Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-2xl">
          <div className="text-3xl font-bold">{total_receipts}</div>
          <div className="text-blue-100">Total Receipts</div>
          <div className="text-xs text-blue-200 mt-1">
            {manual_receipts} manual + {email_receipts} email
          </div>
        </div>
        <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-2xl">
          <div className="text-3xl font-bold">${total_spending.toFixed(2)}</div>
          <div className="text-green-100">Total Spending</div>
        </div>
        <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-2xl">
          <div className="text-3xl font-bold">{Object.keys(category_breakdown).length}</div>
          <div className="text-purple-100">Categories</div>
        </div>
        <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-6 rounded-2xl">
          <div className="text-3xl font-bold">{automation_savings?.emails_processed || 0}</div>
          <div className="text-orange-100">Auto-Processed</div>
          <div className="text-xs text-orange-200 mt-1">
            {(automation_savings?.time_saved_hours || 0).toFixed(1)}h saved
          </div>
        </div>
      </div>

      {/* Nutrition Section */}
      <div className="space-y-6">
        {dashboardData.nutrition && dashboardData.nutrition.latest && (
          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-lg font-bold mb-2 text-indigo-700">🍎 Nutrition (Latest Receipt)</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-2">
              <div>Calories: <span className="font-semibold">{dashboardData.nutrition.latest.total_calories}</span></div>
              <div>Protein: <span className="font-semibold">{dashboardData.nutrition.latest.total_protein}g</span></div>
              <div>Carbs: <span className="font-semibold">{dashboardData.nutrition.latest.total_carbs}g</span></div>
              <div>Fat: <span className="font-semibold">{dashboardData.nutrition.latest.total_fat}g</span></div>
              <div>Fiber: <span className="font-semibold">{dashboardData.nutrition.latest.total_fiber}g</span></div>
              <div>Item Count: <span className="font-semibold">{dashboardData.nutrition.latest.item_count}</span></div>
            </div>
          </div>
        )}
        {dashboardData.nutrition && dashboardData.nutrition.weekly && (
          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-lg font-bold mb-2 text-indigo-700">🍎 Nutrition (This Week)</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-2">
              <div>Calories: <span className="font-semibold">{dashboardData.nutrition.weekly.total_calories}</span></div>
              <div>Protein: <span className="font-semibold">{dashboardData.nutrition.weekly.total_protein}g</span></div>
              <div>Carbs: <span className="font-semibold">{dashboardData.nutrition.weekly.total_carbs}g</span></div>
              <div>Fat: <span className="font-semibold">{dashboardData.nutrition.weekly.total_fat}g</span></div>
              <div>Fiber: <span className="font-semibold">{dashboardData.nutrition.weekly.total_fiber}g</span></div>
              <div>Item Count: <span className="font-semibold">{dashboardData.nutrition.weekly.item_count}</span></div>
            </div>
          </div>
        )}
        {dashboardData.nutrition && dashboardData.nutrition.monthly && (
          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-lg font-bold mb-2 text-indigo-700">🍎 Nutrition (This Month)</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-2">
              <div>Calories: <span className="font-semibold">{dashboardData.nutrition.monthly.total_calories}</span></div>
              <div>Protein: <span className="font-semibold">{dashboardData.nutrition.monthly.total_protein}g</span></div>
              <div>Carbs: <span className="font-semibold">{dashboardData.nutrition.monthly.total_carbs}g</span></div>
              <div>Fat: <span className="font-semibold">{dashboardData.nutrition.monthly.total_fat}g</span></div>
              <div>Fiber: <span className="font-semibold">{dashboardData.nutrition.monthly.total_fiber}g</span></div>
              <div>Item Count: <span className="font-semibold">{dashboardData.nutrition.monthly.item_count}</span></div>
            </div>
          </div>
        )}
        {dashboardData.dietary_insights && (
          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-lg font-bold mb-2 text-green-700">🥗 Dietary Insights</h3>
            {dashboardData.dietary_insights.current && dashboardData.dietary_insights.current.length > 0 ? (
              <ul className="list-disc pl-5 space-y-1">
                {dashboardData.dietary_insights.current.map((insight, idx) => (
                  <li key={idx} className="text-gray-700">{insight}</li>
                ))}
              </ul>
            ) : (
              <div className="text-gray-500 italic">No current insights available. Please upload more receipts or check back later.</div>
            )}
            {dashboardData.dietary_insights.historical && dashboardData.dietary_insights.historical.length > 0 && (
              <div className="mt-4">
                <h4 className="font-semibold text-green-600 mb-1">Historical Insights</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {dashboardData.dietary_insights.historical.map((insight, idx) => (
                    <li key={idx} className="text-gray-600">{insight}</li>
                  ))}
                </ul>
              </div>
            )}
            {dashboardData.dietary_insights.current === null && (
              <div className="text-red-500 mt-2">Note: Dietary insights are generated based on your purchase history and nutritional data. If you have not uploaded any receipts or if your purchase history is not representative of your typical spending, the insights may not be accurate.</div>
            )}
          </div>
        )}
      </div>
      <div className="space-y-6">
        {/* Gmail Integration Status */}
        {gmail_integration && (
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">📧</div>
                <div>
                  <div className="font-semibold text-gray-800">Gmail Integration</div>
                  <div className="text-sm text-gray-600">
                    {gmail_integration.connected ? 
                      `Auto-processing active • ${gmail_integration.total_emails_processed} emails processed` :
                      'Not connected'
                    }
                  </div>
                </div>
              </div>
              <div className={`px-4 py-2 rounded-full text-sm font-medium ${
                gmail_integration.connected 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {gmail_integration.connected ? '🟢 Active' : '⚪ Inactive'}
              </div>
            </div>
            {automation_savings && automation_savings.emails_processed > 0 && (
              <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-indigo-600">
                    {automation_savings.emails_processed}
                  </div>
                  <div className="text-xs text-gray-500">Emails Processed</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-indigo-600">
                    {automation_savings.time_saved_hours.toFixed(1)}h
                  </div>
                  <div className="text-xs text-gray-500">Time Saved</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-indigo-600">
                    {automation_savings.accuracy_rate}
                  </div>
                  <div className="text-xs text-gray-500">Accuracy</div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Category Breakdown */}
      {Object.keys(category_breakdown).length > 0 && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4">💰 Spending by Category</h3>
          <div className="space-y-3">
            {/* [CASCADE FIX] Defensive .map and .toFixed check for category_breakdown */}
{category_breakdown && typeof category_breakdown === 'object' && Object.entries(category_breakdown).map(([category, amount]) => (
  <div key={category} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
    <span className="font-medium text-gray-700">{category}</span>
    <span className="text-lg font-bold text-gray-800">{typeof amount === 'number' ? amount.toFixed(2) : 'N/A'}</span>
  </div>
))}

          </div>
        </div>
      )}

      {/* Insights */}
      {insights && insights.length > 0 && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4">💡 AI Insights</h3>
          <div className="space-y-4">
            {/* [CASCADE FIX] Defensive .map for insights */}
{Array.isArray(insights) && insights.map((insight, index) => (
              <div key={index} className={`p-4 rounded-lg border-l-4 ${
                insight.type === 'warning' ? 'border-red-500 bg-red-50' :
                insight.type === 'tip' ? 'border-blue-500 bg-blue-50' :
                'border-green-500 bg-green-50'
              }`}>
                <div className="font-semibold text-gray-800">{insight.title}</div>
                <div className="text-gray-600 text-sm mt-1">{insight.description}</div>
                <div className="text-sm text-gray-500 mt-2">💡 {insight.suggestion}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Store Recommendations */}
      {storeRecommendations && storeRecommendations.length > 0 && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4">🏬 Store Recommendations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {storeRecommendations.map((rec, idx) => (
              <div key={idx} className="border p-4 rounded-lg shadow-sm bg-gray-50">
                <div className="font-bold text-blue-700 text-lg mb-1">{rec.store}</div>
                <div className="text-gray-700 mb-1">Item: <span className="font-semibold">{rec.item}</span></div>
                <div className="text-green-700 font-bold mb-1">Price: ₹{rec.price}</div>
                <div className="text-gray-500 text-sm">{rec.store_address}</div>
              </div>
            ))}
          </div>
        </div>
      )}
      {storeRecommendations && storeRecommendations.length === 0 && (
        <div className="bg-white rounded-2xl p-4 shadow text-center text-gray-400 mb-4">
          No store recommendations available yet. Upload a receipt to get suggestions!
        </div>
      )}

      {/* Recent Receipts */}
      {recent_receipts && recent_receipts.length > 0 && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Recent Activity</h3>
          <div className="space-y-3">
            {recent_receipts.map((receipt, index) => (
              <div key={index} className="flex flex-col md:flex-row justify-between items-start md:items-center p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center w-full md:w-auto">
                  <span className="mr-3 text-lg">
                    {receipt.source === 'email' ? '📧' : '📄'}
                  </span>
                  <div>
                    <div className="font-medium text-gray-800">{receipt.merchant_name}</div>
                    <div className="text-sm text-gray-500 flex items-center">
                      <span>{receipt.category}</span>
                      <span className="mx-2">•</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        receipt.source === 'email' 
                          ? 'bg-blue-100 text-blue-800' 
                          : 'bg-green-100 text-green-800'
                      }`}>
                        {receipt.source === 'email' ? 'Auto-processed' : 'Manual upload'}
                      </span>
                    </div>
                    {/* AI Insights */}
                    {Array.isArray(receipt.insights) && receipt.insights.length > 0 && (
                      <ul className="list-disc pl-5 mt-2 text-sm text-blue-700">
                        {receipt.insights.map((insight, idx) => (
                          <li key={idx}>{insight}</li>
                        ))}
                      </ul>
                    )}
                    {/* Savings Suggestions */}
                    {Array.isArray(receipt.savings_suggestions) && receipt.savings_suggestions.length > 0 && (
                      <div className="mt-2 p-2 bg-green-50 border-l-4 border-green-400 rounded">
                        <div className="text-xs font-semibold text-green-700 mb-1">💸 Savings Suggestions:</div>
                        <ul className="list-disc pl-5 text-green-700">
                          {receipt.savings_suggestions.map((suggestion, idx) => (
                            <li key={idx}>{suggestion}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-right mt-4 md:mt-0 md:ml-4">
                  <div className="text-lg font-bold text-gray-800">${receipt.total_amount.toFixed(2)}</div>
                  <div className="text-sm text-gray-500">
                    {new Date(receipt.source === 'email' ? receipt.received_date : receipt.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// [CASCADE FIX] Fully defensive, lint-safe WalletPasses component
const WalletPasses = ({ walletPasses }) => {
  if (!Array.isArray(walletPasses) || walletPasses.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
        <div className="text-6xl mb-4">🎫</div>
        <div className="text-xl font-semibold text-gray-700">No Wallet Passes Yet</div>
        <div className="text-gray-500 mt-2">Upload a receipt to create your first wallet pass!</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">🎫 Your Wallet Passes</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {walletPasses.map((pass, index) => (
          <div
            key={index}
            className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6 rounded-2xl shadow-lg"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <div className="text-xl font-bold">
                  {pass && pass.merchant ? pass.merchant : "N/A"}
                </div>
                <div className="text-indigo-100">
                  {pass && pass.category ? pass.category : "N/A"}
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  {pass && typeof pass.amount === "number"
                    ? `$${pass.amount.toFixed(2)}`
                    : "N/A"}
                </div>
                <div className="text-indigo-100 text-sm">
                  {pass && pass.date
                    ? new Date(pass.date).toLocaleDateString()
                    : "N/A"}
                </div>
              </div>
            </div>
            <div className="text-sm text-indigo-100 mb-3">
              {pass && pass.description ? pass.description : "N/A"}
            </div>
            <div className="flex justify-between items-center">
              <span className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm">
                {pass && pass.status ? pass.status : "N/A"}
              </span>
              <span className="text-sm">Project Raseed</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};


// Main App Component
function App() {
  const [currentView, setCurrentView] = useState('upload');
  const [dashboardData, setDashboardData] = useState(null);
const [storeRecommendations, setStoreRecommendations] = useState([]); // New: for agentic store recs
  const [walletPasses, setWalletPasses] = useState([]);
  const [emailReceipts, setEmailReceipts] = useState([]);
  const [gmailStatus, setGmailStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/dashboard/enhanced`);
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadWalletPasses = async () => {
    try {
      const response = await axios.get(`${API}/wallet-passes`);
      setWalletPasses(response.data);
    } catch (error) {
      console.error('Failed to load wallet passes:', error);
    }
  };

  const loadEmailReceipts = async () => {
    try {
      const response = await axios.get(`${API}/gmail/email-receipts`);
      setEmailReceipts(response.data);
    } catch (error) {
      console.error('Failed to load email receipts:', error);
    }
  };

  const loadGmailStatus = async () => {
    try {
      const response = await axios.get(`${API}/gmail/status`);
      setGmailStatus(response.data);
    } catch (error) {
      console.error('Failed to load Gmail status:', error);
    }
  };

  useEffect(() => {
    loadDashboardData();
    loadWalletPasses();
    loadEmailReceipts();
    loadGmailStatus();
  }, []);

  const handleUploadSuccess = async (data) => {
    alert(`✅ Receipt analyzed! Found ${data.receipt.items.length} items from ${data.receipt.merchant_name}`);
    loadDashboardData();
    loadWalletPasses();

    // Agentic: Call recommend-stores with extracted items and city (default: Mumbai for demo)
    const items = data.receipt.items.map((item) => item.name);
    // TODO: Replace 'Mumbai' with user's actual location if available
    try {
      const recRes = await axios.post(`${API}/recommend-stores`, { items, location: 'Mumbai' });
      setStoreRecommendations(recRes.data);
    } catch (err) {
      setStoreRecommendations([]);
    }
  };

  const handleGmailConnect = async () => {
    try {
      const response = await axios.post(`${API}/gmail/connect`);
      if (response.data.success) {
        alert('✅ Gmail connected successfully! Email receipts will be processed automatically.');
        loadGmailStatus();
        loadDashboardData();
      }
    } catch (error) {
      console.error('Failed to connect Gmail:', error);
      alert('❌ Failed to connect Gmail. Please try again.');
    }
  };

  const handleSimulateEmail = async () => {
    try {
      const response = await axios.post(`${API}/gmail/simulate-email`);
      if (response.data.success) {
        alert(`✅ ${response.data.message}`);
        loadDashboardData();
        loadWalletPasses();
        loadEmailReceipts();
        loadGmailStatus();
      }
    } catch (error) {
      console.error('Failed to simulate email:', error);
      alert('❌ Failed to process email. Please try again.');
    }
  };

  const navigation = [
    { id: 'upload', label: '📄 Upload', icon: '📄' },
    { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
    { id: 'gmail', label: '📧 Gmail', icon: '📧' },
    { id: 'emails', label: '📨 Email Receipts', icon: '📨' },
    { id: 'wallet', label: '🎫 Wallet', icon: '🎫' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="text-2xl">🧾</div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Project Raseed</h1>
                <p className="text-sm text-gray-500">AI-Powered Receipt Intelligence</p>
              </div>
            </div>
            <div className="flex items-center space-x-1">
              {/* [CASCADE FIX] Defensive .map check */}
{/* [CASCADE FIX] Defensive .map check */}
{Array.isArray(navigation) && navigation.length > 0
  ? navigation.map((item) => (
      <button
        key={item.id}
        onClick={() => setCurrentView(item.id)}
        className={`px-3 py-2 rounded-lg font-medium transition-colors text-sm ${
          currentView === item.id
            ? 'bg-blue-100 text-blue-700'
            : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
        }`}
      >
        {item.label}
      </button>
    ))
  : null}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <div className="mt-4 text-gray-600">Loading...</div>
          </div>
        )}

        {!loading && (
          <>
            {currentView === 'upload' && (
              <div className="max-w-2xl mx-auto">
                <ReceiptUpload onUploadSuccess={handleUploadSuccess} />
              </div>
            )}

            {currentView === 'dashboard' && <Dashboard dashboardData={dashboardData} storeRecommendations={storeRecommendations} />}

            {currentView === 'gmail' && (
              <div className="max-w-2xl mx-auto">
                <GmailIntegration 
                  gmailStatus={gmailStatus}
                  onConnect={handleGmailConnect}
                  onSimulateEmail={handleSimulateEmail}
                />
              </div>
            )}

            {currentView === 'emails' && <EmailReceiptsList emailReceipts={emailReceipts} />}

            {currentView === 'wallet' && <WalletPasses walletPasses={walletPasses} />}
          </>
        )}
      </main>

      {/* Chatbot Component with Error Boundary */}
      <div style={{ position: 'fixed', bottom: 40, right: 60, zIndex: 50, marginBottom: '110px' }}>
        <ErrorBoundary>
          <Chatbot />
        </ErrorBoundary>
      </div>

      {/* Auto-processing notification */}
      {gmailStatus?.connected && (
        <div className="fixed bottom-4 right-4 bg-gradient-to-r from-green-500 to-blue-500 text-white px-4 py-2 rounded-full shadow-lg z-40">
          <div className="flex items-center space-x-2">
            <div className="animate-pulse w-2 h-2 bg-white rounded-full"></div>
            <span className="text-sm font-medium">Gmail Auto-Processing Active</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;