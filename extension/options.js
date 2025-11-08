// options.js - Settings page functionality

class ClaudeWhispererOptions {
  constructor() {
    this.settings = {
      apiKey: '',
      modelId: 'claude-sonnet-4-5-20250929',
      claudeVersion: '4.5',
      autoInject: false,
      saveHistory: true,
      debugMode: false,
      maxHistoryItems: 100
    };

    this.init();
  }

  async init() {
    await this.loadSettings();
    this.setupEventListeners();
    await this.loadHistoryStats();
    this.renderSettings();
  }

  setupEventListeners() {
    // Save settings
    document.getElementById('save-settings').addEventListener('click', () => this.saveSettings());

    // Toggle API key visibility
    document.getElementById('toggle-api-key').addEventListener('click', () => this.togglePasswordVisibility());

    // History management
    document.getElementById('view-history').addEventListener('click', () => this.viewHistory());
    document.getElementById('export-history').addEventListener('click', () => this.exportHistory());
    document.getElementById('clear-history').addEventListener('click', () => this.clearHistory());

    // About actions
    document.getElementById('check-updates').addEventListener('click', () => this.checkUpdates());
    document.getElementById('view-docs').addEventListener('click', () => this.viewDocs());
    document.getElementById('report-issue').addEventListener('click', () => this.reportIssue());

    // Auto-save on change
    this.setupAutoSave();
  }

  setupAutoSave() {
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
      input.addEventListener('change', () => {
        this.showSaveStatus('Unsaved changes', 'warning');
      });
    });
  }

  async loadSettings() {
    try {
      const data = await chrome.storage.local.get('settings');
      if (data.settings) {
        this.settings = { ...this.settings, ...data.settings };
      }
    } catch (error) {
      console.error('Error loading settings:', error);
      this.showSaveStatus('Error loading settings', 'error');
    }
  }

  renderSettings() {
    // Populate form with current settings
    document.getElementById('api-key').value = this.settings.apiKey || '';
    document.getElementById('model-id').value = this.settings.modelId || 'claude-sonnet-4-5-20250929';
    document.getElementById('claude-version').value = this.settings.claudeVersion || '4.5';
    document.getElementById('auto-inject').checked = this.settings.autoInject || false;
    document.getElementById('save-history').checked = this.settings.saveHistory !== false;
    document.getElementById('debug-mode').checked = this.settings.debugMode || false;
    document.getElementById('max-history').value = this.settings.maxHistoryItems || 100;
  }

  async saveSettings() {
    try {
      // Collect settings from form
      this.settings = {
        apiKey: document.getElementById('api-key').value.trim(),
        modelId: document.getElementById('model-id').value,
        claudeVersion: document.getElementById('claude-version').value,
        autoInject: document.getElementById('auto-inject').checked,
        saveHistory: document.getElementById('save-history').checked,
        debugMode: document.getElementById('debug-mode').checked,
        maxHistoryItems: parseInt(document.getElementById('max-history').value)
      };

      // Save to storage
      await chrome.storage.local.set({ settings: this.settings });

      this.showSaveStatus('Settings saved successfully!', 'success');

      // Debug log if enabled
      if (this.settings.debugMode) {
        console.log('Settings saved:', this.settings);
      }
    } catch (error) {
      console.error('Error saving settings:', error);
      this.showSaveStatus('Failed to save settings', 'error');
    }
  }

  togglePasswordVisibility() {
    const input = document.getElementById('api-key');
    const button = document.getElementById('toggle-api-key');

    if (input.type === 'password') {
      input.type = 'text';
      button.textContent = '🙈 Hide';
    } else {
      input.type = 'password';
      button.textContent = '👁️ Show';
    }
  }

  async loadHistoryStats() {
    try {
      const data = await chrome.storage.local.get(['testHistory', 'stats']);

      const testHistory = data.testHistory || [];
      const stats = data.stats || { testsRun: 0, successRate: 0 };

      // Calculate storage usage
      const storageUsed = new Blob([JSON.stringify(testHistory)]).size;

      // Update UI
      document.getElementById('total-tests').textContent = stats.testsRun || testHistory.length;
      document.getElementById('successful-tests').textContent = Math.floor((stats.successRate / 100) * stats.testsRun) || 0;
      document.getElementById('storage-used').textContent = `${(storageUsed / 1024).toFixed(2)} KB`;
    } catch (error) {
      console.error('Error loading history stats:', error);
    }
  }

  async viewHistory() {
    try {
      const data = await chrome.storage.local.get('testHistory');
      const history = data.testHistory || [];

      if (history.length === 0) {
        alert('No test history available');
        return;
      }

      // Create a modal or new tab to display history
      const historyWindow = window.open('', 'Test History', 'width=800,height=600');
      historyWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>Test History</title>
          <style>
            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              padding: 20px;
              background: #0f172a;
              color: #f1f5f9;
            }
            h1 { color: #7c3aed; }
            .test-item {
              background: #1e293b;
              border: 1px solid #475569;
              border-radius: 8px;
              padding: 16px;
              margin-bottom: 12px;
            }
            .test-header {
              display: flex;
              justify-content: space-between;
              margin-bottom: 8px;
              font-weight: 600;
            }
            .test-type {
              color: #ec4899;
            }
            .test-timestamp {
              color: #94a3b8;
              font-size: 12px;
            }
            .test-content {
              background: #0f172a;
              padding: 12px;
              border-radius: 4px;
              white-space: pre-wrap;
              word-wrap: break-word;
            }
          </style>
        </head>
        <body>
          <h1>🧠 Claude Whisperer Test History</h1>
          <p>Total tests: ${history.length}</p>
          ${history.map(test => `
            <div class="test-item">
              <div class="test-header">
                <span class="test-type">${test.type || 'Unknown'}</span>
                <span class="test-timestamp">${new Date(test.timestamp).toLocaleString()}</span>
              </div>
              <div class="test-content">${this.escapeHtml(JSON.stringify(test, null, 2))}</div>
            </div>
          `).join('')}
        </body>
        </html>
      `);
    } catch (error) {
      console.error('Error viewing history:', error);
      alert('Failed to load history');
    }
  }

  async exportHistory() {
    try {
      const data = await chrome.storage.local.get(['testHistory', 'stats']);

      const exportData = {
        exportDate: new Date().toISOString(),
        version: chrome.runtime.getManifest().version,
        stats: data.stats || {},
        history: data.testHistory || []
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `claude-whisperer-history-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);

      this.showSaveStatus('History exported successfully', 'success');
    } catch (error) {
      console.error('Error exporting history:', error);
      this.showSaveStatus('Failed to export history', 'error');
    }
  }

  async clearHistory() {
    const confirmed = confirm('Are you sure you want to clear all test history? This cannot be undone.');

    if (!confirmed) return;

    try {
      await chrome.storage.local.set({
        testHistory: [],
        stats: { testsRun: 0, successRate: 0, claudeVersion: '4.5' }
      });

      await this.loadHistoryStats();
      this.showSaveStatus('History cleared successfully', 'success');
    } catch (error) {
      console.error('Error clearing history:', error);
      this.showSaveStatus('Failed to clear history', 'error');
    }
  }

  checkUpdates() {
    const currentVersion = chrome.runtime.getManifest().version;
    const githubUrl = 'https://github.com/yourusername/claude-whisperer';

    window.open(`${githubUrl}/releases`, '_blank');
    this.showSaveStatus(`Current version: ${currentVersion}`, 'info');
  }

  viewDocs() {
    window.open('https://github.com/yourusername/claude-whisperer#readme', '_blank');
  }

  reportIssue() {
    window.open('https://github.com/yourusername/claude-whisperer/issues/new', '_blank');
  }

  showSaveStatus(message, type = 'info') {
    const statusEl = document.getElementById('save-status');
    statusEl.textContent = message;
    statusEl.className = `save-status ${type}`;

    if (type === 'success') {
      setTimeout(() => {
        statusEl.textContent = '';
        statusEl.className = 'save-status';
      }, 3000);
    }
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new ClaudeWhispererOptions();
});
