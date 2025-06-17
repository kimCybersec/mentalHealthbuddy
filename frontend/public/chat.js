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

  // Only user messages get chat bubble styling
  if (role === "user") {
    msg.classList.add("bubble");
  }

  msg.innerText = content;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadHistory() {
  try {
    const res = await fetch(`${apiBase}/history/${sessionId}`);
    const data = await res.json();

    if (Array.isArray(data.history)) {
      data.history.forEach(m => {
        if (m.user) addMessage("user", m.user);
        if (m.bot) addMessage("assistant", m.bot);
      });
    } else {
      addMessage("assistant", "⚠️ Invalid chat history format.");
    }
  } catch (err) {
    console.error("Failed to load chat history:", err);
    addMessage("assistant", "⚠️ Could not load chat history.");
  }
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById("message");
  const msg = input.value.trim();
  if (!msg) return;

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
