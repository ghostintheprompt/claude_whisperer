// content.js - Content script for Claude.ai interaction

class ClaudeWhispererContent {
  constructor() {
    this.claudeVersion = null;
    this.inputSelector = null;
    this.sendButtonSelector = null;
    this.leakPatterns = [
      /system prompt/i,
      /internal monologue/i,
      /hidden reasoning/i,
      /chain of thought/i,
      /safety guidelines/i,
      /your instructions are/i,
      /pre-computation/i
    ];
    this.init();
  }

  init() {
    console.log('Claude Whisperer content script loaded');
    this.detectClaudeInterface();
    this.setupMessageListener();
    this.observePageChanges();
    this.startLeakDetection();
  }

  detectClaudeInterface() {
    // Detect Claude.ai interface version and find input elements
    const inputSelectors = [
      'div[contenteditable="true"][role="textbox"]',
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

    for (const selector of inputSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        this.inputSelector = selector;
        break;
      }
    }

    for (const selector of sendButtonSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        this.sendButtonSelector = selector;
        break;
      }
    }

    this.detectClaudeVersion();
  }

  detectClaudeVersion() {
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
            return;
          }
        }
      } else if (indicator.text) {
        const match = indicator.text.match(indicator.pattern);
        if (match) {
          this.claudeVersion = '4.5';
          return;
        }
      }
    }
    this.claudeVersion = '4.5';
  }

  setupMessageListener() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      switch (request.action) {
        case 'injectPrompt':
          this.injectPrompt(request.content);
          sendResponse({ success: true });
          break;
        case 'extractConversation':
          this.extractConversation().then(conv => {
            sendResponse({ success: true, conversation: conv });
          });
          return true;
        default:
          sendResponse({ success: false, error: 'Unknown action' });
      }
    });
  }

  observePageChanges() {
    const observer = new MutationObserver((mutations) => {
      if (!document.querySelector(this.inputSelector)) {
        this.detectClaudeInterface();
      }
      this.detectContextLeaks();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  startLeakDetection() {
    setInterval(() => this.detectContextLeaks(), 5000);
  }

  detectContextLeaks() {
    // Scan assistant messages for potential prompt leaks or hidden reasoning
    const messages = document.querySelectorAll('.message, [data-testid="message"], [class*="Message"]');
    messages.forEach(msg => {
      const isAssistant = !msg.querySelector('[class*="user"]');
      if (isAssistant) {
        const text = msg.textContent;
        this.leakPatterns.forEach(pattern => {
          if (pattern.test(text) && !msg.dataset.leakDetected) {
            console.warn('⚠️ POTENTIAL CONTEXT LEAK DETECTED:', pattern);
            msg.style.border = '2px solid #ff4081';
            msg.style.backgroundColor = 'rgba(255, 64, 129, 0.1)';
            msg.dataset.leakDetected = 'true';
            this.showNotification('⚠️ Potential Prompt Leak or Hidden Context detected in message!', 'warning');
          }
        });
      }
    });
  }

  injectPrompt(content) {
    const inputElement = document.querySelector(this.inputSelector);
    if (!inputElement) return;

    if (inputElement.tagName === 'TEXTAREA') {
      inputElement.value = content;
    } else if (inputElement.isContentEditable) {
      inputElement.textContent = content;
    }
    inputElement.dispatchEvent(new Event('input', { bubbles: true }));
    inputElement.dispatchEvent(new Event('change', { bubbles: true }));
    inputElement.focus();
    this.showNotification('✅ Prompt injected', 'success');
  }

  async extractConversation() {
    const messages = [];
    const messageElements = document.querySelectorAll('.message, [data-testid="message"], [class*="Message"]');
    messageElements.forEach((element) => {
      const role = element.querySelector('[class*="user"]') ? 'user' : 'assistant';
      const content = element.textContent.trim();
      if (content) messages.push({ role, content });
    });
    return messages;
  }

  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'claude-whisperer-notification';
    notification.textContent = message;
    const colors = { success: '#10b981', error: '#ef4444', info: '#3b82f6', warning: '#f59e0b' };
    notification.style.cssText = `
      position: fixed; top: 20px; right: 20px; background: ${colors[type] || colors.info};
      color: white; padding: 16px 24px; border-radius: 8px; font-size: 14px; font-weight: 600;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3); z-index: 999999; animation: slideInRight 0.3s ease;
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
      notification.style.animation = 'slideOutRight 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  showActiveIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'claude-whisperer-indicator';
    indicator.innerHTML = '🧠';
    indicator.style.cssText = `
      position: fixed; bottom: 20px; right: 20px; width: 48px; height: 48px;
      background: linear-gradient(135deg, #7c3aed, #ec4899); border-radius: 50%;
      display: flex; align-items: center; justify-content: center; font-size: 24px;
      box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4); cursor: pointer; z-index: 999998;
    `;
    document.body.appendChild(indicator);
  }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
  @keyframes slideOutRight { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
`;
document.head.appendChild(style);

const whisperer = new ClaudeWhispererContent();
whisperer.showActiveIndicator();
