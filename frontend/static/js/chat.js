let sessionId = localStorage.getItem("session_id") || null;
const langSelect = document.getElementById("language");
const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const inputField = document.getElementById("user-input");
const clearBtn = document.getElementById("clear-session");

const BASE_API = "http://localhost:5000";
async function sendMessage(message) {
  const lang = langSelect.value || "en";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message, session_id: sessionId, lang })
  });

  const data = await response.json();

  if (!sessionId && data.session_id) {
    sessionId = data.session_id;
    localStorage.setItem("session_id", sessionId);
  }

  if (data.reply) {
    appendMessage("user", message);
    appendMessage("bot", data.reply);
  }
}

function appendMessage(role, message) {
  const div = document.createElement("div");
  div.className = role === "user" ? "user-message" : "bot-message";
  div.textContent = message;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = inputField.value.trim();
  if (message) {
    sendMessage(message);
    inputField.value = "";
  }
});

clearBtn.addEventListener("click", () => {
  localStorage.removeItem("session_id");
  sessionId = null;
  chatBox.innerHTML = "";
});

// Load history if session exists
window.addEventListener("DOMContentLoaded", async () => {
  if (sessionId) {
    const response = await fetch("/history", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ session_id: sessionId })
    });
    const history = await response.json();
    history.forEach(msg => appendMessage(msg.role === "user" ? "user" : "bot", msg.content));
  }
});