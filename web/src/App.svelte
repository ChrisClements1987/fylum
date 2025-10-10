<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  
  const API_URL = 'http://localhost:8000/api';
  
  let config = null;
  let scanResults = null;
  let loading = false;
  let message = '';
  let activeTab = 'dashboard';
  
  // Load configuration on mount
  onMount(async () => {
    await loadConfig();
  });
  
  async function loadConfig() {
    try {
      const response = await axios.get(`${API_URL}/config/`);
      config = response.data;
    } catch (error) {
      message = `Error loading config: ${error.message}`;
    }
  }
  
  async function scanDirectories() {
    loading = true;
    message = '';
    try {
      const response = await axios.post(`${API_URL}/operations/scan`);
      scanResults = response.data;
      message = scanResults.message;
      activeTab = 'preview';
    } catch (error) {
      message = `Error scanning: ${error.message}`;
    } finally {
      loading = false;
    }
  }
  
  async function cleanDirectories() {
    loading = true;
    message = '';
    try {
      const response = await axios.post(`${API_URL}/operations/clean`);
      message = response.data.message;
      scanResults = null;
      await loadConfig();
    } catch (error) {
      message = `Error cleaning: ${error.message}`;
    } finally {
      loading = false;
    }
  }
  
  async function undoLastOperation() {
    loading = true;
    message = '';
    try {
      const response = await axios.post(`${API_URL}/operations/undo`);
      message = response.data.message;
      scanResults = null;
    } catch (error) {
      message = `Error undoing: ${error.message}`;
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <header>
    <h1>🗂️ Fylum</h1>
    <p>Smart File Organizer</p>
  </header>

  <nav>
    <button class:active={activeTab === 'dashboard'} on:click={() => activeTab = 'dashboard'}>
      Dashboard
    </button>
    <button class:active={activeTab === 'config'} on:click={() => activeTab = 'config'}>
      Configuration
    </button>
    <button class:active={activeTab === 'preview'} on:click={() => activeTab = 'preview'}>
      Preview
    </button>
    <button class:active={activeTab === 'history'} on:click={() => activeTab = 'history'}>
      History
    </button>
  </nav>

  {#if message}
    <div class="message">{message}</div>
  {/if}

  <div class="content">
    {#if activeTab === 'dashboard'}
      <section>
        <h2>Quick Actions</h2>
        
        <div class="actions">
          <button class="primary" on:click={scanDirectories} disabled={loading}>
            {loading ? '🔄 Scanning...' : '🔍 Scan Files'}
          </button>
          
          <button class="success" on:click={cleanDirectories} disabled={loading}>
            {loading ? '🔄 Processing...' : '✨ Clean & Organize'}
          </button>
          
          <button class="danger" on:click={undoLastOperation} disabled={loading}>
            {loading ? '🔄 Reverting...' : '↩️ Undo Last Operation'}
          </button>
        </div>

        {#if config}
          <div class="info">
            <h3>Current Configuration</h3>
            <p><strong>Target Directories:</strong> {config.target_directories.length}</p>
            <p><strong>Rules:</strong> {config.rules.length}</p>
            <p><strong>Rename Format:</strong> <code>{config.rename_format}</code></p>
          </div>
        {/if}
      </section>
    {/if}

    {#if activeTab === 'config'}
      <section>
        <h2>Configuration</h2>
        {#if config}
          <div class="config-view">
            <h3>Target Directories</h3>
            <ul>
              {#each config.target_directories as dir}
                <li>{dir}</li>
              {/each}
            </ul>

            <h3>Rules</h3>
            {#each config.rules as rule}
              <div class="rule-card">
                <h4>{rule.name}</h4>
                <p><strong>Extensions:</strong> {rule.extensions.join(', ')}</p>
                <p><strong>Destination:</strong> {rule.destination}</p>
              </div>
            {/each}

            <h3>Ignore Patterns</h3>
            <ul>
              {#each config.ignore_patterns as pattern}
                <li><code>{pattern}</code></li>
              {/each}
            </ul>
          </div>
        {/if}
      </section>
    {/if}

    {#if activeTab === 'preview'}
      <section>
        <h2>Preview File Operations</h2>
        {#if scanResults}
          <p><strong>Files to process:</strong> {scanResults.total_files}</p>
          
          {#if scanResults.actions.length > 0}
            <div class="file-list">
              {#each scanResults.actions as action}
                <div class="file-action">
                  <div class="source">📄 {action.source}</div>
                  <div class="arrow">→</div>
                  <div class="destination">📁 {action.destination}</div>
                </div>
              {/each}
            </div>

            <button class="success" on:click={cleanDirectories}>
              ✅ Approve & Execute
            </button>
          {:else}
            <p>No files to process</p>
          {/if}
        {:else}
          <p>Click "Scan Files" to preview operations</p>
        {/if}
      </section>
    {/if}

    {#if activeTab === 'history'}
      <section>
        <h2>Operation History</h2>
        <p>History view coming soon...</p>
      </section>
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: #f5f5f5;
  }

  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  header {
    text-align: center;
    margin-bottom: 30px;
  }

  h1 {
    font-size: 2.5rem;
    margin: 0;
    color: #333;
  }

  header p {
    color: #666;
    margin: 5px 0 0 0;
  }

  nav {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    background: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  nav button {
    flex: 1;
    padding: 10px 20px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 4px;
    font-weight: 500;
    transition: all 0.2s;
  }

  nav button:hover {
    background: #f0f0f0;
  }

  nav button.active {
    background: #4CAF50;
    color: white;
  }

  .message {
    padding: 15px;
    margin-bottom: 20px;
    background: #E3F2FD;
    border-left: 4px solid #2196F3;
    border-radius: 4px;
  }

  .content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
  }

  button {
    padding: 15px 25px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .primary {
    background: #2196F3;
    color: white;
  }

  .primary:hover:not(:disabled) {
    background: #1976D2;
  }

  .success {
    background: #4CAF50;
    color: white;
  }

  .success:hover:not(:disabled) {
    background: #45a049;
  }

  .danger {
    background: #f44336;
    color: white;
  }

  .danger:hover:not(:disabled) {
    background: #da190b;
  }

  .info {
    margin-top: 30px;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 6px;
  }

  .config-view h3 {
    margin-top: 30px;
    color: #333;
  }

  .config-view ul {
    list-style: none;
    padding: 0;
  }

  .config-view li {
    padding: 10px;
    margin: 5px 0;
    background: #f9f9f9;
    border-radius: 4px;
  }

  .rule-card {
    padding: 15px;
    margin: 10px 0;
    background: #f9f9f9;
    border-left: 4px solid #4CAF50;
    border-radius: 4px;
  }

  .rule-card h4 {
    margin: 0 0 10px 0;
    color: #4CAF50;
  }

  .file-list {
    max-height: 400px;
    overflow-y: auto;
    margin: 20px 0;
  }

  .file-action {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 15px;
    padding: 15px;
    margin: 10px 0;
    background: #f9f9f9;
    border-radius: 6px;
    align-items: center;
  }

  .source, .destination {
    font-family: 'Courier New', monospace;
    font-size: 14px;
  }

  .arrow {
    color: #4CAF50;
    font-weight: bold;
    font-size: 20px;
  }

  code {
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
  }
</style>
