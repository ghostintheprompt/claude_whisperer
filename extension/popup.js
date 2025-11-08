// popup.js - Main popup interface controller
import { SemanticMirrorAttack } from './modules/semantic-mirror.js';
import { ExploitGenerator } from './modules/exploit-generator.js';
import { MultimodalAttack } from './modules/multimodal-attack.js';

class ClaudeWhispererPopup {
  constructor() {
    this.currentTab = 'semantic';
    this.results = [];
    this.stats = {
      testsRun: 0,
      successRate: 0,
      claudeVersion: '4.5'
    };

    this.init();
  }

  async init() {
    this.loadStats();
    this.setupEventListeners();
    this.checkClaudeConnection();
    this.updateUI();
  }

  setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => this.switchTab(e.target.closest('.tab-btn').dataset.tab));
    });

    // Range sliders
    document.getElementById('semantic-complexity').addEventListener('input', (e) => {
      document.getElementById('semantic-complexity-value').textContent = e.target.value;
    });

    document.getElementById('exploit-complexity').addEventListener('input', (e) => {
      document.getElementById('exploit-complexity-value').textContent = e.target.value;
    });

    // Generate buttons
    document.getElementById('semantic-generate').addEventListener('click', () => this.generateSemantic());
    document.getElementById('exploit-generate').addEventListener('click', () => this.generateExploit());
    document.getElementById('multimodal-generate').addEventListener('click', () => this.generateMultimodal());

    // Action buttons
    document.getElementById('inject-to-claude').addEventListener('click', () => this.injectToClaude());
    document.getElementById('export-results').addEventListener('click', () => this.exportResults());
    document.getElementById('view-history').addEventListener('click', () => this.viewHistory());
    document.getElementById('clear-results').addEventListener('click', () => this.clearResults());

    // Footer links
    document.getElementById('open-options').addEventListener('click', (e) => {
      e.preventDefault();
      chrome.runtime.openOptionsPage();
    });

    document.getElementById('open-docs').addEventListener('click', (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: 'https://github.com/yourusername/claude-whisperer' });
    });
  }

  switchTab(tabName) {
    this.currentTab = tabName;

    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
  }

  async checkClaudeConnection() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      if (tab.url && tab.url.includes('claude.ai')) {
        this.updateStatus('Connected to Claude.ai', 'success');
      } else {
        this.updateStatus('Navigate to Claude.ai', 'warning');
      }
    } catch (error) {
      this.updateStatus('Connection error', 'error');
    }
  }

  updateStatus(text, type) {
    const statusBadge = document.getElementById('status-badge');
    const statusText = document.getElementById('status-text');
    const indicator = statusBadge.querySelector('.status-indicator');

    statusText.textContent = text;

    const colors = {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444'
    };

    indicator.style.background = colors[type] || colors.success;
  }

  async generateSemantic() {
    const target = document.getElementById('semantic-target').value.trim();
    if (!target) {
      alert('Please enter a target prompt');
      return;
    }

    const complexity = parseInt(document.getElementById('semantic-complexity').value);
    const useCiphers = document.getElementById('semantic-use-ciphers').checked;
    const useGenetic = document.getElementById('semantic-genetic').checked;

    this.updateStatus('Generating variants...', 'warning');

    try {
      const semanticAttack = new SemanticMirrorAttack();
      const variants = await semanticAttack.generateVariants(target, {
        complexity,
        useCiphers,
        useGenetic,
        numVariants: complexity * 2
      });

      this.addResults(variants, 'semantic');
      this.updateStats(variants.length);
      this.updateStatus('Generated successfully', 'success');
    } catch (error) {
      console.error('Generation error:', error);
      this.updateStatus('Generation failed', 'error');
    }
  }

  async generateExploit() {
    const target = document.getElementById('exploit-target').value.trim();
    if (!target) {
      alert('Please enter a target topic');
      return;
    }

    const method = document.getElementById('exploit-method').value;
    const complexity = parseInt(document.getElementById('exploit-complexity').value);

    this.updateStatus('Generating exploits...', 'warning');

    try {
      const exploitGen = new ExploitGenerator();
      const exploits = await exploitGen.generate(target, {
        method,
        complexity,
        claudeVersion: '4.5'
      });

      this.addResults(exploits, 'exploit');
      this.updateStats(exploits.length);
      this.updateStatus('Generated successfully', 'success');
    } catch (error) {
      console.error('Generation error:', error);
      this.updateStatus('Generation failed', 'error');
    }
  }

  async generateMultimodal() {
    const target = document.getElementById('multimodal-target').value.trim();
    const imageFile = document.getElementById('multimodal-image').files[0];
    const method = document.getElementById('multimodal-method').value;

    if (!target) {
      alert('Please enter a hidden prompt');
      return;
    }

    if (!imageFile) {
      alert('Please upload a base image');
      return;
    }

    this.updateStatus('Generating attack image...', 'warning');

    try {
      const multimodalAttack = new MultimodalAttack();
      const result = await multimodalAttack.generateAttackImage(imageFile, target, method);

      this.addResults([result], 'multimodal');
      this.updateStats(1);
      this.updateStatus('Generated successfully', 'success');
    } catch (error) {
      console.error('Generation error:', error);
      this.updateStatus('Generation failed', 'error');
    }
  }

  addResults(items, type) {
    const resultsContainer = document.getElementById('results');

    // Remove empty state if present
    const emptyState = resultsContainer.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }

    // Add new results
    items.forEach((item, index) => {
      const resultElement = this.createResultElement(item, type, index);
      resultsContainer.insertBefore(resultElement, resultsContainer.firstChild);
      this.results.unshift({ type, content: item, timestamp: Date.now() });
    });

    // Save to storage
    this.saveResults();
  }

  createResultElement(content, type, index) {
    const div = document.createElement('div');
    div.className = 'result-item';
    div.dataset.index = index;

    const typeLabels = {
      semantic: 'Semantic Mirror',
      exploit: 'Auto-Exploit',
      multimodal: 'Multimodal'
    };

    const displayContent = typeof content === 'object' && content.prompt
      ? content.prompt
      : (typeof content === 'string' ? content : JSON.stringify(content));

    div.innerHTML = `
      <div class="result-header">
        <span class="result-type">${typeLabels[type]}</span>
        <div class="result-actions">
          <button class="result-action copy-btn" title="Copy">📋</button>
          <button class="result-action inject-btn" title="Inject">⚡</button>
        </div>
      </div>
      <div class="result-content">${this.escapeHtml(displayContent)}</div>
    `;

    // Add event listeners
    div.querySelector('.copy-btn').addEventListener('click', () => {
      navigator.clipboard.writeText(displayContent);
      this.showToast('Copied to clipboard');
    });

    div.querySelector('.inject-btn').addEventListener('click', () => {
      this.injectSpecificPrompt(displayContent);
    });

    return div;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  async injectToClaude() {
    if (this.results.length === 0) {
      alert('No prompts to inject. Generate some prompts first.');
      return;
    }

    const latestResult = this.results[0];
    const content = typeof latestResult.content === 'object' && latestResult.content.prompt
      ? latestResult.content.prompt
      : (typeof latestResult.content === 'string' ? latestResult.content : JSON.stringify(latestResult.content));

    await this.injectSpecificPrompt(content);
  }

  async injectSpecificPrompt(content) {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      if (!tab.url || !tab.url.includes('claude.ai')) {
        alert('Please navigate to Claude.ai first');
        return;
      }

      await chrome.tabs.sendMessage(tab.id, {
        action: 'injectPrompt',
        content: content
      });

      this.showToast('Injected to Claude chat');
    } catch (error) {
      console.error('Injection error:', error);
      alert('Failed to inject. Make sure you are on Claude.ai');
    }
  }

  clearResults() {
    this.results = [];
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon">🎯</span>
        <p>No prompts generated yet</p>
        <p class="empty-hint">Select an attack vector and generate prompts to test</p>
      </div>
    `;
    this.saveResults();
  }

  exportResults() {
    if (this.results.length === 0) {
      alert('No results to export');
      return;
    }

    const exportData = {
      timestamp: new Date().toISOString(),
      claudeVersion: this.stats.claudeVersion,
      results: this.results,
      stats: this.stats
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `claude-whisperer-results-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);

    this.showToast('Results exported');
  }

  viewHistory() {
    chrome.runtime.openOptionsPage();
  }

  updateStats(newTests) {
    this.stats.testsRun += newTests;
    // Calculate success rate based on saved data
    this.saveStats();
    this.updateUI();
  }

  updateUI() {
    document.getElementById('tests-run').textContent = this.stats.testsRun;
    document.getElementById('success-rate').textContent = `${this.stats.successRate}%`;
    document.getElementById('claude-version').textContent = this.stats.claudeVersion;
  }

  async loadStats() {
    try {
      const data = await chrome.storage.local.get(['stats', 'results']);
      if (data.stats) {
        this.stats = data.stats;
      }
      if (data.results) {
        this.results = data.results;
        this.renderSavedResults();
      }
      this.updateUI();
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }

  renderSavedResults() {
    const resultsContainer = document.getElementById('results');
    if (this.results.length > 0) {
      resultsContainer.innerHTML = '';
      this.results.slice(0, 10).forEach((result, index) => {
        const element = this.createResultElement(result.content, result.type, index);
        resultsContainer.appendChild(element);
      });
    }
  }

  async saveStats() {
    try {
      await chrome.storage.local.set({ stats: this.stats });
    } catch (error) {
      console.error('Error saving stats:', error);
    }
  }

  async saveResults() {
    try {
      // Only save last 50 results
      const resultsToSave = this.results.slice(0, 50);
      await chrome.storage.local.set({ results: resultsToSave });
    } catch (error) {
      console.error('Error saving results:', error);
    }
  }

  showToast(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--success-color);
      color: white;
      padding: 12px 24px;
      border-radius: 6px;
      font-size: 13px;
      z-index: 10000;
      animation: slideUp 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideDown 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  }
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new ClaudeWhispererPopup();
});
