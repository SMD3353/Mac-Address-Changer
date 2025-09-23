const menuContainer = document.getElementById("menu-container");
const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const voiceButton = document.getElementById("voice-button");
const voiceLabel = document.getElementById("voice-label");
const voicePlayback = document.getElementById("voice-playback");

const conversationHistory = [];
let mediaRecorder;
let recordedChunks = [];
let activeStream;
let isRecording = false;

const formatCurrency = (value) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);

async function fetchMenu() {
  try {
    const response = await fetch("/api/menu");
    if (!response.ok) throw new Error("Unable to load menu");
    const menu = await response.json();
    renderMenu(menu);
  } catch (error) {
    menuContainer.innerHTML = `<p class="menu__error">${error.message}</p>`;
  }
}

function renderMenu(menu) {
  menuContainer.innerHTML = Object.entries(menu)
    .map(([category, items]) => {
      const itemsHtml = items
        .map(
          (item) => `
            <article class="menu__item">
              <div>
                <div class="menu__item-name">${item.name}</div>
                <div class="menu__item-description">${item.description}</div>
              </div>
              <div class="menu__item-price">${formatCurrency(item.price)}</div>
            </article>
          `
        )
        .join("");

      return `
        <section class="menu__category">
          <h3>${category}</h3>
          ${itemsHtml}
        </section>
      `;
    })
    .join("");
}

function addMessage(role, text) {
  const message = document.createElement("div");
  message.className = `chat__message chat__message--${role}`;
  message.textContent = text;
  chatLog.appendChild(message);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendChatMessage(message) {
  addMessage("user", message);
  conversationHistory.push({ role: "user", content: message });
  userInput.value = "";
  userInput.focus();

  const loadingMessage = document.createElement("div");
  loadingMessage.className = "chat__message chat__message--assistant";
  loadingMessage.textContent = "Harmony is thinking...";
  chatLog.appendChild(loadingMessage);
  chatLog.scrollTop = chatLog.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: conversationHistory }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Unable to contact Harmony");
    }

    const data = await response.json();
    loadingMessage.remove();
    addMessage("assistant", data.reply);
    conversationHistory.push({ role: "assistant", content: data.reply });
  } catch (error) {
    loadingMessage.remove();
    addMessage("assistant", error.message);
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;
  sendChatMessage(message);
});

async function toggleRecording() {
  if (isRecording) {
    mediaRecorder.stop();
    voiceButton.disabled = true;
    voiceLabel.textContent = "Processing voice order...";
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    activeStream = stream;
    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = handleRecordingStop;

    mediaRecorder.start();
    isRecording = true;
    voiceButton.classList.add("is-recording");
    voiceLabel.textContent = "Listening... Tap to finish";
  } catch (error) {
    addMessage("assistant", "Microphone access is required for voice ordering.");
    voiceButton.disabled = false;
    voiceButton.classList.remove("is-recording");
    voiceLabel.textContent = "Start voice order";
  }
}

async function handleRecordingStop() {
  isRecording = false;
  voiceButton.classList.remove("is-recording");

  if (activeStream) {
    activeStream.getTracks().forEach((track) => track.stop());
    activeStream = undefined;
  }

  const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
  const formData = new FormData();
  formData.append("audio", audioBlob, "voice.webm");
  formData.append("history", JSON.stringify(conversationHistory));

  try {
    const response = await fetch("/api/voice", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Voice request failed");
    }

    addMessage("user", payload.transcript);
    conversationHistory.push({ role: "user", content: payload.transcript });
    addMessage("assistant", payload.reply);
    conversationHistory.push({ role: "assistant", content: payload.reply });

    if (payload.audio) {
      voicePlayback.src = payload.audio;
      voicePlayback.classList.add("is-visible");
      voicePlayback.play().catch(() => {
        /* Autoplay might be blocked; leave the controls for manual playback */
      });
    }
  } catch (error) {
    addMessage("assistant", error.message);
  } finally {
    voiceButton.disabled = false;
    voiceLabel.textContent = "Start voice order";
  }
}

voiceButton.addEventListener("click", () => {
  if (!isRecording) {
    toggleRecording();
  } else {
    mediaRecorder.stop();
  }
});

if (typeof MediaRecorder === "undefined") {
  voiceButton.disabled = true;
  voiceLabel.textContent = "Voice ordering requires a modern browser.";
}

fetchMenu();
const welcomeMessage = "Hi there! I’m Harmony. Feel free to ask about the menu or start an order when you’re ready.";
addMessage("assistant", welcomeMessage);
conversationHistory.push({ role: "assistant", content: welcomeMessage });
