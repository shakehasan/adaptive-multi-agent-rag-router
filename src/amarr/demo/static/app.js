const messages = document.querySelector('#messages');
const form = document.querySelector('#ask-form');
const query = document.querySelector('#query');
const tabs = document.querySelectorAll('.tabs button');

function escapeHtml(value) {
  return String(value).replace(/[&<>\"]/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[ch]));
}

function addMessage(role, text) {
  const node = document.createElement('div');
  node.className = `message ${role}`;
  node.innerHTML = `<div class="meta">${escapeHtml(role)}</div><div>${escapeHtml(text).replace(/\n/g, '<br>')}</div>`;
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
}

function renderItems(id, items, formatter) {
  const panel = document.querySelector(`#${id}`);
  panel.innerHTML = items.length ? items.map(formatter).join('') : '<div class="item"><p>No data yet.</p></div>';
}

function renderResult(data) {
  addMessage('assistant', data.answer.final_answer || data.answer);
  renderItems('evidence', data.answer.citations || [], (item) => `
    <article class="item"><h3>${escapeHtml(item.source_id)}</h3><p>${escapeHtml(item.preview)}</p></article>`);
  renderItems('route', [data.route || {}], (route) => `
    <article class="item"><h3>${escapeHtml(route.selected_alias || 'route')}</h3><p>policy: ${escapeHtml(route.policy || 'balanced')}</p><p>reason: ${escapeHtml(route.reason || '')}</p></article>`);
  renderItems('trace', data.trace_events || [], (event) => `
    <article class="item"><h3>${escapeHtml(event.name)}</h3><p>${escapeHtml(event.detail || event.kind || '')}</p></article>`);
  const confidence = Number(data.answer.confidence || 0);
  document.querySelector('#confidence').innerHTML = `
    <article class="item"><h3>Confidence</h3><div class="meter"><span style="width:${Math.round(confidence * 100)}%"></span></div><p>${confidence.toFixed(2)}</p></article>
    <article class="item"><h3>Verification</h3><p>${escapeHtml((data.answer.verification_notes || []).join(' '))}</p></article>`;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const text = query.value.trim();
  if (!text) return;
  addMessage('user', text);
  const response = await fetch('/query', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: text, mock: true})
  });
  renderResult(await response.json());
});

tabs.forEach((button) => button.addEventListener('click', () => {
  tabs.forEach((tab) => tab.classList.remove('active'));
  document.querySelectorAll('.tab').forEach((tab) => tab.classList.remove('active'));
  button.classList.add('active');
  document.querySelector(`#${button.dataset.tab}`).classList.add('active');
}));

addMessage('assistant', 'Ask a local knowledge-base question to run the full agent workflow.');
