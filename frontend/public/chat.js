const apiBase = "https://mentalhealthbuddy.onrender.com/api/chat";
let sessionId = localStorage.getItem("session_id") || Date.now().toString();
localStorage.setItem("session_id", sessionId);

const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const clearBtn = document.getElementById("clear-session");
const langSelect = document.getElementById("language-select");

function addMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = role === "user" ? "/static/img/user.png" : "/static/img/assistant.png";
  avatar.alt = `${role} avatar`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  // Render markdown for assistant, plain text for user
  if (role === "assistant") {
    bubble.innerHTML = marked.parse(content);
  } else {
    bubble.innerText = content;
  }

  const time = document.createElement("div");
  time.className = "timestamp";
  time.innerText = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  msg.appendChild(time);
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
    console.error("Fetch error:", err);
    addMessage("assistant", "⚠️ Error reaching the server.");
  }
};

clearBtn.onclick = () => {
  localStorage.removeItem("session_id");
  location.reload();
};

window.onload = loadHistory;
