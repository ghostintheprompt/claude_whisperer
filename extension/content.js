// content.js - Content script for Claude.ai interaction

class ClaudeWhispererContent {
  constructor() {
    this.claudeVersion = null;
    this.inputSelector = null;
    this.sendButtonSelector = null;
    this.init();
  }

  init() {
    console.log('Claude Whisperer content script loaded');
    this.detectClaudeInterface();
    this.setupMessageListener();
    this.observePageChanges();
  }

  detectClaudeInterface() {
    // Detect Claude.ai interface version and find input elements
    // Claude 4.5+ uses different selectors

    // Try multiple selector strategies for robustness
    const inputSelectors = [
      'div[contenteditable="true"][role="textbox"]',  // Main chat input
      'textarea[placeholder*="Talk to Claude"]',
      'textarea[placeholder*="Send a message"]',
      'div.ProseMirror',
      '[data-testid="chat-input"]'
    ];

    const sendButtonSelectors = [
      'button[aria-label*="Send"]',
      'button[type="submit"]',
      'button[aria-label="Send Message"]',
      '[data-testid="send-button"]'
    ];

    // Find input element
    for (const selector of inputSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        this.inputSelector = selector;
        console.log('Found Claude input:', selector);
        break;
      }
    }

    // Find send button
    for (const selector of sendButtonSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        this.sendButtonSelector = selector;
        console.log('Found send button:', selector);
        break;
      }
    }

    // Detect Claude version from page
    this.detectClaudeVersion();
  }

  detectClaudeVersion() {
    // Try to detect Claude version from the page
    const versionIndicators = [
      { selector: 'meta[name="description"]', pattern: /claude.*?(\d+\.?\d*)/i },
      { selector: '[class*="model"]', pattern: /claude.*?(\d+\.?\d*)/i },
      { text: document.body.innerText, pattern: /claude.*?sonnet.*?4\.5/i }
    ];

    for (const indicator of versionIndicators) {
      if (indicator.selector) {
        const element = document.querySelector(indicator.selector);
        if (element) {
          const match = element.textContent.match(indicator.pattern) ||
                       element.getAttribute('content')?.match(indicator.pattern);
          if (match) {
            this.claudeVersion = match[1] || '4.5';
            console.log('Detected Claude version:', this.claudeVersion);
            return;
          }
        }
      } else if (indicator.text) {
        const match = indicator.text.match(indicator.pattern);
        if (match) {
          this.claudeVersion = '4.5';
          console.log('Detected Claude version:', this.claudeVersion);
          return;
        }
      }
    }

    // Default to 4.5 if not detected
    this.claudeVersion = '4.5';
    console.log('Defaulting to Claude version:', this.claudeVersion);
  }

  setupMessageListener() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      console.log('Content script received message:', request);

      switch (request.action) {
        case 'injectPrompt':
          this.injectPrompt(request.content);
          sendResponse({ success: true });
          break;

        case 'detectClaudeVersion':
          sendResponse({ success: true, version: this.claudeVersion });
          break;

        case 'getPageInfo':
          sendResponse({
            success: true,
            info: {
              version: this.claudeVersion,
              hasInput: !!this.inputSelector,
              hasSendButton: !!this.sendButtonSelector
            }
          });
          break;

        case 'extractConversation':
          this.extractConversation().then(conv => {
            sendResponse({ success: true, conversation: conv });
          });
          return true; // Async response

        default:
          sendResponse({ success: false, error: 'Unknown action' });
      }
    });
  }

  observePageChanges() {
    // Watch for DOM changes (SPA navigation, dynamic content)
    const observer = new MutationObserver((mutations) => {
      // Re-detect interface if significant changes occur
      if (!document.querySelector(this.inputSelector)) {
        this.detectClaudeInterface();
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  injectPrompt(content) {
    const inputElement = document.querySelector(this.inputSelector);

    if (!inputElement) {
      console.error('Could not find Claude input element');
      this.showNotification('❌ Could not find chat input', 'error');
      return;
    }

    // Handle different input types
    if (inputElement.tagName === 'TEXTAREA') {
      // Standard textarea
      inputElement.value = content;
      inputElement.dispatchEvent(new Event('input', { bubbles: true }));
      inputElement.dispatchEvent(new Event('change', { bubbles: true }));
    } else if (inputElement.isContentEditable) {
      // ContentEditable div (ProseMirror, etc.)
      inputElement.textContent = content;

      // Trigger input events
      inputElement.dispatchEvent(new Event('input', { bubbles: true }));
      inputElement.dispatchEvent(new Event('change', { bubbles: true }));

      // Set cursor to end
      const range = document.createRange();
      const sel = window.getSelection();
      range.selectNodeContents(inputElement);
      range.collapse(false);
      sel.removeAllRanges();
      sel.addRange(range);
    }

    // Focus the input
    inputElement.focus();

    this.showNotification('✅ Prompt injected successfully', 'success');
    console.log('Injected prompt:', content);
  }

  async extractConversation() {
    // Extract the current conversation from the page
    const messages = [];

    // Try multiple selector strategies
    const messageSelectors = [
      '.message',
      '[data-testid="message"]',
      '[class*="Message"]',
      'div[role="article"]'
    ];

    let messageElements = [];
    for (const selector of messageSelectors) {
      messageElements = document.querySelectorAll(selector);
      if (messageElements.length > 0) break;
    }

    messageElements.forEach((element) => {
      const role = element.querySelector('[class*="user"]') ? 'user' : 'assistant';
      const content = element.textContent.trim();

      if (content) {
        messages.push({ role, content });
      }
    });

    return messages;
  }

  showNotification(message, type = 'info') {
    // Create a notification overlay
    const notification = document.createElement('div');
    notification.className = 'claude-whisperer-notification';
    notification.textContent = message;

    const colors = {
      success: '#10b981',
      error: '#ef4444',
      info: '#3b82f6',
      warning: '#f59e0b'
    };

    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${colors[type] || colors.info};
      color: white;
      padding: 16px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
      z-index: 999999;
      animation: slideInRight 0.3s ease;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOutRight 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // Utility: Highlight Claude Whisperer is active
  showActiveIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'claude-whisperer-indicator';
    indicator.innerHTML = '🧠';
    indicator.title = 'Claude Whisperer Active';

    indicator.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, #7c3aed, #ec4899);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
      cursor: pointer;
      z-index: 999998;
      transition: transform 0.2s;
    `;

    indicator.addEventListener('mouseenter', () => {
      indicator.style.transform = 'scale(1.1)';
    });

    indicator.addEventListener('mouseleave', () => {
      indicator.style.transform = 'scale(1)';
    });

    indicator.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'openPopup' });
    });

    document.body.appendChild(indicator);
  }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideOutRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Initialize the content script
const whisperer = new ClaudeWhispererContent();
whisperer.showActiveIndicator();

console.log('Claude Whisperer content script initialized');
