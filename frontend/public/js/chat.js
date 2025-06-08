const apiBase = "https://mentalhealthbuddy.onrender.com"; 
let sessionId = localStorage.getItem("session_id") || Date.now().toString(); 
localStorage.setItem("session_id", sessionId);

const chatBox = document.getElementById("chat-box"); 
const form = document.getElementById("chat-form"); 
const clearBtn = document.getElementById("clear-session"); 
const langSelect = document.getElementById("lang-select");

function addMessage(role, content) { 
  const msg = document.createElement("div"); 
  msg.className = role; 
  msg.innerText = content; 
  chatBox.appendChild(msg); 
}

async function loadHistory() 
{ 
  const res = await fetch(`${apiBase}/history/${sessionId}`); 
  const data = await res.json(); 
  data.history.forEach(m => { 
    addMessage("user", m.user); 
    addMessage("assistant", m.bot); 
  }); 
}

form.onsubmit = async (e) => { e.preventDefault(); 
  const input = document.getElementById("message"); 
  const msg = input.value; 
  addMessage("user", msg); 
  input.value = "";

const res = await fetch(apiBase, {
    method: "POST", 
    headers: { "Content-Type": "application/json" }, 
    body: JSON.stringify({ 
      messages: [{ role: "user", content: msg }], 
      lang: langSelect.value, session_id: sessionId 
    }) 
  }); 
  const data = await res.json(); 
  addMessage("assistant", data.reply); 
};

clearBtn.onclick = () => { 
  localStorage.removeItem("session_id"); 
  location.reload(); 
};

window.onload = loadHistory;