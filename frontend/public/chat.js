const apiBase = "https://mentalhealthbuddy.onrender.com/api/chat";
let sessionId = localStorage.getItem("session_id") || Date.now().toString();
localStorage.setItem("session_id", sessionId);

const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const clearBtn = document.getElementById("clear-session");
const langSelect = document.getElementById("language-select");

function addMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = role;
  msg.innerText = content;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadHistory() {
  try {
    const res = await fetch(`${apiBase}/history/${sessionId}`);
    const data = await res.json();
    data.history.forEach(m => {
      addMessage("user", m.user);
      addMessage("assistant", m.bot);
    });
  } catch (err) {
    console.error("Failed to load chat history:", err);
  }
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById("message");
  const msg = input.value;
  addMessage("user", msg);
  input.value = "";

  try {
    const res = await fetch(apiBase, {
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
    addMessage("assistant", "⚠️ Error reaching the server.");
    console.error("Fetch error:", err);
  }
};

clearBtn.onclick = () => {
  localStorage.removeItem("session_id");
  location.reload();
};

window.onload = loadHistory;
