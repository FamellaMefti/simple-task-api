const listEl = document.getElementById('ticket-list');
const emptyEl = document.getElementById('empty-state');
const errorEl = document.getElementById('error-state');
const formEl = document.getElementById('add-form');
const inputEl = document.getElementById('add-input');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

const CHECK_ICON = `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M5 13l4 4L19 7" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;

function setStatus(state) {
  statusDot.classList.remove('is-ok', 'is-error');
  if (state === 'ok') {
    statusDot.classList.add('is-ok');
    statusText.textContent = 'Terhubung ke API';
  } else if (state === 'error') {
    statusDot.classList.add('is-error');
    statusText.textContent = 'Tidak bisa menghubungi API';
  } else {
    statusText.textContent = 'Menghubungkan ke API…';
  }
}

function renderTasks(tasks) {
  listEl.innerHTML = '';
  emptyEl.hidden = tasks.length > 0;

  tasks.forEach((task) => {
    const li = document.createElement('li');
    li.className = 'ticket' + (task.done ? ' is-done' : '');
    li.dataset.id = task.id;

    li.innerHTML = `
      <button class="ticket__stamp" title="Tandai selesai">${CHECK_ICON}</button>
      <span class="ticket__id">#${String(task.id).padStart(3, '0')}</span>
      <span class="ticket__title"></span>
      <button class="ticket__delete" title="Hapus task">&times;</button>
    `;
    li.querySelector('.ticket__title').textContent = task.title;

    li.querySelector('.ticket__stamp').addEventListener('click', () => toggleDone(task));
    li.querySelector('.ticket__delete').addEventListener('click', () => deleteTask(task.id));

    listEl.appendChild(li);
  });
}

async function loadTasks() {
  try {
    const res = await fetch('/tasks');
    if (!res.ok) throw new Error('bad response');
    const tasks = await res.json();
    renderTasks(tasks);
    errorEl.hidden = true;
    setStatus('ok');
  } catch (err) {
    errorEl.hidden = false;
    listEl.innerHTML = '';
    emptyEl.hidden = true;
    setStatus('error');
  }
}

async function addTask(title) {
  await fetch('/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  loadTasks();
}

async function toggleDone(task) {
  await fetch(`/tasks/${task.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done: !task.done }),
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`/tasks/${id}`, { method: 'DELETE' });
  loadTasks();
}

formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const title = inputEl.value.trim();
  if (!title) return;
  inputEl.value = '';
  addTask(title);
});

loadTasks();
setInterval(loadTasks, 15000);
