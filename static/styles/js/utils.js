function showMessage(text, type = "success") {
  const container = document.getElementById("message-container");

  if (!container) {
    console.warn("message-container not found");
    return;
  }

  const message = document.createElement("div");
  message.className = `message ${type}`;
  message.innerText = text;

  container.appendChild(message);

  setTimeout(() => {
    message.remove();
  }, 3000);
}

window.showMessage = showMessage;