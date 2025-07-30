function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";

  // Temporary bot response
  setTimeout(() => {
    addMessage("This is a dummy response. Backend will handle real answers!", "bot");
  }, 500);
}

// Handle file upload
function handleFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  addMessage(`Uploaded file: ${file.name}`, "user");

  // For now just show file name, later we will send file to backend
  setTimeout(() => {
    addMessage("Resume received! I will analyze it once backend is connected.", "bot");
  }, 500);
}
