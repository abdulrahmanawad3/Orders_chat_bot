const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const emptyState = document.getElementById('empty-state');
const evalBtn = document.getElementById('eval-btn');
const evalPanel = document.getElementById('eval-panel');
const evalBody = document.getElementById('eval-body');
const evalClose = document.getElementById('eval-close');

let busy = false;

// ── Textarea auto-resize ──────────────────────────────────────────────────────
inputEl.addEventListener('input', () => {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
});
inputEl.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
sendBtn.addEventListener('click', send);

// ── Clear ─────────────────────────────────────────────────────────────────────
document.getElementById('clear-btn').addEventListener('click', () => {
    messagesEl.innerHTML = '';
    messagesEl.appendChild(emptyState);
    emptyState.style.display = 'flex';
    closeEvalPanel();
});

// ── Eval panel open/close ─────────────────────────────────────────────────────
evalBtn.addEventListener('click', runEval);
evalClose.addEventListener('click', closeEvalPanel);

function closeEvalPanel() {
    evalPanel.classList.remove('open');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function fillInput(text) {
    inputEl.value = text;
    inputEl.focus();
    inputEl.dispatchEvent(new Event('input'));
}

function now() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}


function addMessage(text, role) {
    emptyState.style.display = 'none';
    const row = document.createElement('div');
    row.className = `msg-row ${role}`;

    const av = document.createElement('div');
    av.className = 'msg-avatar';
    av.textContent = role === 'bot' ? '🍗' : 'Me';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    // Convert \n to <br> and escape HTML special chars to prevent injection
    bubble.innerHTML = escHtml(text).replace(/\n/g, '<br>');

    const ts = document.createElement('span');
    ts.className = 'timestamp';
    ts.textContent = now();

    if (role === 'user') row.append(ts, bubble, av);
    else row.append(av, bubble, ts);

    messagesEl.appendChild(row);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showTyping() {
    const row = document.createElement('div');
    row.className = 'typing-row';
    row.id = 'typing';
    const av = document.createElement('div');
    av.className = 'msg-avatar';
    av.style.cssText = 'background:linear-gradient(135deg,#c0392b,#e8540a);box-shadow:0 3px 10px rgba(232,84,10,.4);font-size:16px;';
    av.textContent = '🍗';
    const b = document.createElement('div');
    b.className = 'typing-bubble';
    b.innerHTML = '<span></span><span></span><span></span>';
    row.append(av, b);
    messagesEl.appendChild(row);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}
function hideTyping() { document.getElementById('typing')?.remove(); }

// ── Send ──────────────────────────────────────────────────────────────────────
async function send() {
    const text = inputEl.value.trim();
    if (!text || busy) return;

    addMessage(text, 'user');
    inputEl.value = '';
    inputEl.style.height = 'auto';
    sendBtn.disabled = true;
    busy = true;
    showTyping();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        hideTyping();
        addMessage(data.reply || '…', 'bot');
    } catch {
        hideTyping();
        addMessage("Uh oh! Something went wrong in the kitchen. Please try again!", 'bot');
    } finally {
        sendBtn.disabled = false;
        busy = false;
        inputEl.focus();
    }
}

// ── Evaluate ──────────────────────────────────────────────────────────────────
async function runEval() {
    if (busy) return;

    evalBtn.disabled = true;
    evalPanel.classList.add('open');

    // Show loading state inside panel
    evalBody.innerHTML = `
        <div class="eval-idle">
            <div class="eval-idle-icon">⏳</div>
            <div class="eval-idle-text">Judging the last response…</div>
        </div>`;

    try {
        const res = await fetch('/evaluate', { method: 'POST' });
        const data = await res.json();

        if (data.error) {
            evalBody.innerHTML = `
                <div class="eval-idle">
                    <div class="eval-idle-icon">⚠️</div>
                    <div class="eval-idle-text">${data.error}</div>
                </div>`;
            return;
        }

        // Score colour: green ≥0.7, amber 0.4–0.69, red <0.4
        const s = data.score ?? 0;
        const pct = Math.round(s * 100);
        const ringBg = s >= 0.7
            ? 'linear-gradient(135deg,#1a7a3a,#27ae60)'
            : s >= 0.4
                ? 'linear-gradient(135deg,#7a4e00,#e8940a)'
                : 'linear-gradient(135deg,#7a1010,#c0392b)';

        evalBody.innerHTML = `
            <div class="eval-score-wrap">
                <div class="score-ring" style="background:${ringBg}">${pct}%</div>
                <div class="score-label">CORRECTNESS SCORE</div>
            </div>

            <div class="eval-qa">
                <div class="eval-qa-row">
                    <div class="eval-qa-label">Question</div>
                    <div class="eval-qa-text">${escHtml(data.question)}</div>
                </div>
                <div class="eval-qa-row">
                    <div class="eval-qa-label">Answer</div>
                    <div class="eval-qa-text">${escHtml(data.answer)}</div>
                </div>
            </div>

            <div class="eval-reasoning">
                <div class="eval-reasoning-label">🧠 Judge's Reasoning</div>
                <div class="eval-reasoning-text">${escHtml(data.reasoning)}</div>
            </div>`;

    } catch {
        evalBody.innerHTML = `
            <div class="eval-idle">
                <div class="eval-idle-icon">💥</div>
                <div class="eval-idle-text">Evaluation failed.<br>Check your server logs.</div>
            </div>`;
    } finally {
        evalBtn.disabled = false;
    }
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}