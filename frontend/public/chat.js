document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.chat-container')) {
    initChat();
  }
});

function initChat() {
  const apiBase = "/api";
  let sessionId = localStorage.getItem("session_id") || Date.now().toString();
  localStorage.setItem("session_id", sessionId);

  const chatBox = document.getElementById("chat-box");
  const form = document.getElementById("chat-form");
  const clearBtn = document.getElementById("clear-session");
  const langSelect = document.getElementById("language-select");

  loadHistory();

  form.onsubmit = async (e) => {
    e.preventDefault();
    const input = document.getElementById("user-input");
    const msg = input.value.trim();
    if (!msg) return;

    addMessage("user", msg);
    input.value = "";

    try {
      const res = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [{ role: "user", content: msg }],
          lang: langSelect.value,
          session_id: sessionId
        })
      });
      const data = await res.json();
      addMessage("assistant", data.reply);
    } catch (err) {
      addMessage("assistant", "⚠️ Failed to get response. Please try again.");
    }
  };

  clearBtn.onclick = () => {
    localStorage.removeItem("session_id");
    chatBox.innerHTML = "";
    sessionId = Date.now().toString();
    localStorage.setItem("session_id", sessionId);
  };
}

function addMessage(role, content) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = `message ${role}`;
  msg.innerText = content;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadHistory() {
  const chatBox = document.getElementById("chat-box");
  if (!chatBox) return;

  const sessionId = localStorage.getItem("session_id");
  if (!sessionId) return;

  try {
    const res = await fetch(`/api/history/${sessionId}`);
    const data = await res.json();
    data.history.forEach(m => {
      addMessage("user", m.user);
      addMessage("assistant", m.bot);
    });
  } catch (err) {
    console.error("Failed to load history:", err);
  }
}