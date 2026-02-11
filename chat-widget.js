/**
 * Clawdbot — AI Chat Widget for flywithpeggs.com
 * Connects to the Digital Dream Team via Supabase Edge Function
 */
(function () {
  'use strict';

  // === Configuration ===
  const CONFIG = {
    supabaseUrl: 'https://cvfkqqfcsfjcanzffvnv.supabase.co',
    functionName: 'clawdbot',
    maxMessages: 50,
  };

  const AGENTS = {
    general: { name: 'Clawdbot', icon: 'fas fa-robot', color: '#5D3FD3', greeting: "Hi! I'm Clawdbot, your guide to flywithpeggs.com. How can I help you today?" },
    opal: { name: 'Opal', icon: 'fas fa-spa', color: '#9966CC', greeting: "Hello! I'm Opal, your wellness coach. How can I support your health and well-being today?" },
    mary: { name: 'Mary', icon: 'fas fa-leaf', color: '#DAA520', greeting: "Welcome! I'm Mary, your herbal specialist. What can I help you with today?" },
    mira: { name: 'Mira', icon: 'fas fa-plane', color: '#5D3FD3', greeting: "Hey there! I'm Mira, your travel concierge. Where are you dreaming of going?" },
    lior: { name: 'Lior', icon: 'fas fa-microchip', color: '#4A00E0', greeting: "Hi! I'm Lior, your AI consultant. What would you like to explore about AI today?" },
  };

  // === State ===
  let currentAgent = 'general';
  let conversationId = null;
  let messages = [];
  let isOpen = false;
  let isStreaming = false;
  let visitorId = getOrCreateVisitorId();

  function getOrCreateVisitorId() {
    let id = sessionStorage.getItem('clawdbot_visitor_id');
    if (!id) {
      id = 'v_' + Math.random().toString(36).substring(2, 15) + Date.now().toString(36);
      sessionStorage.setItem('clawdbot_visitor_id', id);
    }
    return id;
  }

  function loadConversation(agent) {
    const saved = sessionStorage.getItem('clawdbot_conv_' + agent);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        messages = parsed.messages || [];
        conversationId = parsed.conversationId || null;
        return true;
      } catch (e) { /* ignore */ }
    }
    messages = [];
    conversationId = null;
    return false;
  }

  function saveConversation() {
    sessionStorage.setItem('clawdbot_conv_' + currentAgent, JSON.stringify({
      messages,
      conversationId,
    }));
  }

  // === Build the Widget DOM ===
  function createWidget() {
    // Container
    const container = document.createElement('div');
    container.id = 'clawdbot-container';
    container.innerHTML = `
      <button id="clawdbot-fab" aria-label="Open chat">
        <i class="fas fa-comments"></i>
      </button>
      <div id="clawdbot-panel" class="clawdbot-hidden">
        <div id="clawdbot-header">
          <div id="clawdbot-header-info">
            <i id="clawdbot-header-icon" class="fas fa-robot"></i>
            <div>
              <div id="clawdbot-header-name">Clawdbot</div>
              <div id="clawdbot-header-status">Online</div>
            </div>
          </div>
          <div id="clawdbot-header-actions">
            <button id="clawdbot-agents-btn" aria-label="Switch agent" title="Switch agent">
              <i class="fas fa-users"></i>
            </button>
            <button id="clawdbot-close-btn" aria-label="Close chat">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
        <div id="clawdbot-agent-picker" class="clawdbot-hidden">
          <div class="clawdbot-agent-picker-title">Chat with a specialist</div>
          <div id="clawdbot-agent-list"></div>
        </div>
        <div id="clawdbot-messages"></div>
        <div id="clawdbot-input-area">
          <input id="clawdbot-input" type="text" placeholder="Type a message..." autocomplete="off" />
          <button id="clawdbot-send" aria-label="Send message">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
        <div id="clawdbot-footer">Powered by Clawdbot</div>
      </div>
    `;
    document.body.appendChild(container);

    // Populate agent picker
    const agentList = document.getElementById('clawdbot-agent-list');
    Object.entries(AGENTS).forEach(([key, agent]) => {
      const btn = document.createElement('button');
      btn.className = 'clawdbot-agent-option';
      btn.dataset.agent = key;
      btn.innerHTML = `<i class="${agent.icon}" style="color: ${agent.color};"></i><span>${agent.name}</span>`;
      btn.addEventListener('click', () => selectAgent(key));
      agentList.appendChild(btn);
    });

    // Event listeners
    document.getElementById('clawdbot-fab').addEventListener('click', () => togglePanel());
    document.getElementById('clawdbot-close-btn').addEventListener('click', () => togglePanel(false));
    document.getElementById('clawdbot-agents-btn').addEventListener('click', toggleAgentPicker);
    document.getElementById('clawdbot-send').addEventListener('click', sendMessage);
    document.getElementById('clawdbot-input').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  // === UI Actions ===
  function togglePanel(forceState) {
    const panel = document.getElementById('clawdbot-panel');
    const fab = document.getElementById('clawdbot-fab');
    isOpen = forceState !== undefined ? forceState : !isOpen;

    if (isOpen) {
      panel.classList.remove('clawdbot-hidden');
      fab.classList.add('clawdbot-fab-hidden');
      document.getElementById('clawdbot-input').focus();
      // Show greeting if no messages
      if (messages.length === 0) {
        addBotMessage(AGENTS[currentAgent].greeting, false);
      }
    } else {
      panel.classList.add('clawdbot-hidden');
      fab.classList.remove('clawdbot-fab-hidden');
      hideAgentPicker();
    }
  }

  function toggleAgentPicker() {
    const picker = document.getElementById('clawdbot-agent-picker');
    picker.classList.toggle('clawdbot-hidden');
  }

  function hideAgentPicker() {
    document.getElementById('clawdbot-agent-picker').classList.add('clawdbot-hidden');
  }

  function selectAgent(agent) {
    if (agent === currentAgent) {
      hideAgentPicker();
      return;
    }
    // Save current conversation
    saveConversation();
    // Switch
    currentAgent = agent;
    loadConversation(agent);
    updateHeader();
    renderMessages();
    hideAgentPicker();
    // Show greeting if empty
    if (messages.length === 0) {
      addBotMessage(AGENTS[currentAgent].greeting, false);
    }
  }

  function updateHeader() {
    const agent = AGENTS[currentAgent];
    document.getElementById('clawdbot-header-icon').className = agent.icon;
    document.getElementById('clawdbot-header-icon').style.color = agent.color;
    document.getElementById('clawdbot-header-name').textContent = agent.name;
  }

  function renderMessages() {
    const container = document.getElementById('clawdbot-messages');
    container.innerHTML = '';
    messages.forEach((msg) => {
      appendMessageBubble(msg.role, msg.content);
    });
    scrollToBottom();
  }

  function appendMessageBubble(role, content) {
    const container = document.getElementById('clawdbot-messages');
    const bubble = document.createElement('div');
    bubble.className = 'clawdbot-msg clawdbot-msg-' + (role === 'user' ? 'user' : 'bot');
    bubble.textContent = content;
    container.appendChild(bubble);
    return bubble;
  }

  function addBotMessage(text, save = true) {
    messages.push({ role: 'assistant', content: text });
    appendMessageBubble('assistant', text);
    scrollToBottom();
    if (save) saveConversation();
  }

  function scrollToBottom() {
    const container = document.getElementById('clawdbot-messages');
    container.scrollTop = container.scrollHeight;
  }

  // === Send Message & Stream Response ===
  async function sendMessage() {
    const input = document.getElementById('clawdbot-input');
    const text = input.value.trim();
    if (!text || isStreaming) return;

    // Add user message
    messages.push({ role: 'user', content: text });
    appendMessageBubble('user', text);
    input.value = '';
    scrollToBottom();
    saveConversation();

    // Create streaming bot bubble
    isStreaming = true;
    const botBubble = document.createElement('div');
    botBubble.className = 'clawdbot-msg clawdbot-msg-bot clawdbot-msg-streaming';
    botBubble.innerHTML = '<span class="clawdbot-typing"><span></span><span></span><span></span></span>';
    document.getElementById('clawdbot-messages').appendChild(botBubble);
    scrollToBottom();

    // Disable input
    input.disabled = true;
    document.getElementById('clawdbot-send').disabled = true;

    let fullResponse = '';

    try {
      const apiMessages = messages
        .filter((m) => m.role === 'user' || m.role === 'assistant')
        .slice(-CONFIG.maxMessages);

      const response = await fetch(`${CONFIG.supabaseUrl}/functions/v1/${CONFIG.functionName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent: currentAgent,
          messages: apiMessages,
          conversation_id: conversationId,
          visitor_id: visitorId,
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || 'Something went wrong');
      }

      // Parse SSE stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
              const parsed = JSON.parse(data);
              if (parsed.text) {
                if (botBubble.querySelector('.clawdbot-typing')) {
                  botBubble.innerHTML = '';
                }
                fullResponse += parsed.text;
                botBubble.textContent = fullResponse;
                scrollToBottom();
              }
            } catch (e) { /* skip */ }
          }
        }
      }
    } catch (error) {
      fullResponse = 'Sorry, I had trouble connecting. Please try again in a moment.';
      botBubble.innerHTML = '';
      botBubble.textContent = fullResponse;
      botBubble.classList.add('clawdbot-msg-error');
    }

    // Finalize
    botBubble.classList.remove('clawdbot-msg-streaming');
    messages.push({ role: 'assistant', content: fullResponse });
    saveConversation();
    isStreaming = false;
    input.disabled = false;
    document.getElementById('clawdbot-send').disabled = false;
    input.focus();
    scrollToBottom();
  }

  // === Public API ===
  window.clawdbot = {
    open: function (agent) {
      if (agent && AGENTS[agent]) {
        if (agent !== currentAgent) {
          saveConversation();
          currentAgent = agent;
          loadConversation(agent);
          updateHeader();
          renderMessages();
        }
      }
      togglePanel(true);
    },
    close: function () {
      togglePanel(false);
    },
  };

  // === Init ===
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    createWidget();
    loadConversation(currentAgent);
    updateHeader();
  }
})();
