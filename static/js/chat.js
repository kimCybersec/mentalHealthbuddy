document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");
    const clearBtn = document.getElementById("clear-session");

    let session_id = localStorage.getItem("session_id");
    if (!session_id) {
        session_id = crypto.randomUUID();
        localStorage.setItem("session_id", session_id);
    }

    function renderMessage(role, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", role);
        msgDiv.innerText = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function loadHistory() {
        try {
            const res = await fetch(`/history/${session_id}`);
            const data = await res.json();
            if (data.history) {
                data.history.forEach(entry => {
                    renderMessage("user", entry.user);
                    renderMessage("assistant", entry.bot);
                });
            }
        } catch (err) {
            console.error("Failed to load chat history", err);
        }
    }

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userMsg = chatInput.value.trim();
        if (!userMsg) return;

        renderMessage("user", userMsg);
        chatInput.value = "";

        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    session_id,
                    messages: [{ role: "user", content: userMsg }]
                })
            });
            const data = await res.json();

            if (data.reply) {
                renderMessage("assistant", data.reply);
            }
            if (data.crisis_resources) {
                renderMessage("assistant", `Crisis Support: ${data.crisis_resources}`);
            }
        } catch (err) {
            renderMessage("assistant", "Sorry, there was an error processing your request.");
            console.error(err);
        }
    });

    clearBtn.addEventListener("click", async () => {
        if (confirm("Are you sure you want to clear this session?")) {
            try {
                await fetch(`/clear/${session_id}`, {
                    method: "DELETE"
                });
                chatBox.innerHTML = "";
                localStorage.removeItem("session_id");
                location.reload();
            } catch (err) {
                console.error("Failed to clear session", err);
            }
        }
    });

    loadHistory();
});
