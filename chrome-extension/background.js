// Background script for Veritas Fact Checker Extension
// Handles context menu, API calls, and extension state management

const API_BASE_URL = 'http://localhost:8000/api/v1/verify';

// Create context menu when extension is installed
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "veritas-fact-check",
    title: "🔍 Fact-check with Veritas",
    contexts: ["selection"]
  });
  
  console.log("Veritas Fact Checker extension installed");
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "veritas-fact-check" && info.selectionText) {
    console.log("Fact-checking selected text:", info.selectionText);
    
    // Show loading state
    chrome.tabs.sendMessage(tab.id, {
      action: "showLoading",
      text: info.selectionText
    });
    
    try {
      // Call Veritas API
      const result = await factCheckText(info.selectionText);
      
      // Send result to content script
      chrome.tabs.sendMessage(tab.id, {
        action: "showResult",
        result: result,
        originalText: info.selectionText
      });
      
    } catch (error) {
      console.error("Fact-check failed:", error);
      
      // Send error to content script
      chrome.tabs.sendMessage(tab.id, {
        action: "showError",
        error: error.message,
        originalText: info.selectionText
      });
    }
  }
});

// Function to call Veritas API
async function factCheckText(text) {
  const response = await fetch(`${API_BASE_URL}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      claim_type: 'sentence',
      language: 'en'
    })
  });
  
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }
  
  const data = await response.json();
  return data;
}

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "factCheck") {
    factCheckText(request.text)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    
    return true; // Keep message channel open for async response
  }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, {
    action: "togglePanel"
  });
});
