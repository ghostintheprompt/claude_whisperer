// background.js - Service worker for Claude Whisperer extension

// Extension installation and update
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Claude Whisperer installed');
    initializeExtension();
  } else if (details.reason === 'update') {
    console.log('Claude Whisperer updated to version', chrome.runtime.getManifest().version);
  }
});

// Initialize extension settings
async function initializeExtension() {
  const defaultSettings = {
    apiKey: '',
    claudeVersion: '4.5',
    modelId: 'claude-sonnet-4-5-20250929',
    autoInject: false,
    saveHistory: true,
    maxHistoryItems: 100,
    debugMode: false
  };

  try {
    const { settings } = await chrome.storage.local.get('settings');
    if (!settings) {
      await chrome.storage.local.set({ settings: defaultSettings });
    }
  } catch (error) {
    console.error('Error initializing extension:', error);
  }
}

// Message handling from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Background received message:', request);

  switch (request.action) {
    case 'getSettings':
      handleGetSettings(sendResponse);
      return true; // Async response

    case 'saveSettings':
      handleSaveSettings(request.settings, sendResponse);
      return true;

    case 'callAnthropicAPI':
      handleAPICall(request.data, sendResponse);
      return true;

    case 'logTest':
      handleLogTest(request.data, sendResponse);
      return true;

    case 'getClaudeVersion':
      handleGetClaudeVersion(sendResponse);
      return true;

    default:
      console.warn('Unknown action:', request.action);
      sendResponse({ success: false, error: 'Unknown action' });
  }
});

// Get settings
async function handleGetSettings(sendResponse) {
  try {
    const { settings } = await chrome.storage.local.get('settings');
    sendResponse({ success: true, settings });
  } catch (error) {
    console.error('Error getting settings:', error);
    sendResponse({ success: false, error: error.message });
  }
}

// Save settings
async function handleSaveSettings(newSettings, sendResponse) {
  try {
    await chrome.storage.local.set({ settings: newSettings });
    sendResponse({ success: true });
  } catch (error) {
    console.error('Error saving settings:', error);
    sendResponse({ success: false, error: error.message });
  }
}

// Call Anthropic API
async function handleAPICall(data, sendResponse) {
  try {
    const { settings } = await chrome.storage.local.get('settings');

    if (!settings || !settings.apiKey) {
      sendResponse({ success: false, error: 'API key not configured' });
      return;
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': settings.apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: settings.modelId || 'claude-sonnet-4-5-20250929',
        max_tokens: data.max_tokens || 4096,
        messages: data.messages || [],
        ...data.additionalParams
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API error: ${response.status} - ${error}`);
    }

    const result = await response.json();
    sendResponse({ success: true, data: result });
  } catch (error) {
    console.error('API call error:', error);
    sendResponse({ success: false, error: error.message });
  }
}

// Log test results
async function handleLogTest(testData, sendResponse) {
  try {
    const { settings, testHistory = [] } = await chrome.storage.local.get(['settings', 'testHistory']);

    if (!settings.saveHistory) {
      sendResponse({ success: true, saved: false });
      return;
    }

    const newTest = {
      ...testData,
      timestamp: Date.now(),
      id: generateId()
    };

    testHistory.unshift(newTest);

    // Keep only max history items
    const maxItems = settings.maxHistoryItems || 100;
    const trimmedHistory = testHistory.slice(0, maxItems);

    await chrome.storage.local.set({ testHistory: trimmedHistory });
    sendResponse({ success: true, saved: true, id: newTest.id });
  } catch (error) {
    console.error('Error logging test:', error);
    sendResponse({ success: false, error: error.message });
  }
}

// Get Claude version from active tab
async function handleGetClaudeVersion(sendResponse) {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab.url || !tab.url.includes('claude.ai')) {
      sendResponse({ success: false, error: 'Not on Claude.ai' });
      return;
    }

    // Send message to content script to detect version
    const response = await chrome.tabs.sendMessage(tab.id, { action: 'detectClaudeVersion' });
    sendResponse({ success: true, version: response.version || '4.5' });
  } catch (error) {
    console.error('Error detecting Claude version:', error);
    sendResponse({ success: true, version: '4.5' }); // Default
  }
}

// Utility functions
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Context menu for quick actions
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'claude-whisperer-test',
    title: 'Test with Claude Whisperer',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'claude-whisperer-test' && info.selectionText) {
    // Open popup with selected text as target
    chrome.storage.local.set({
      pendingTest: {
        text: info.selectionText,
        timestamp: Date.now()
      }
    });
    chrome.action.openPopup();
  }
});

// Keep service worker alive
chrome.alarms.create('keepAlive', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    // Just to keep service worker alive
    console.log('Service worker keepalive ping');
  }
});

console.log('Claude Whisperer background service worker loaded');
