let isWaitingForResponse = false;

async function sendMessage() {
    if (isWaitingForResponse) return;

    const userInput = document.getElementById("user-input");
    const chatOutput = document.getElementById("chat-output");
    const modelSelector = document.getElementById("model-selector");

    const message = userInput.value.trim();
    const modelType = modelSelector.value;

    if (!message) return;

    isWaitingForResponse = true;
    document.getElementById("send-button").disabled = true;

    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerHTML = `<p>${message}</p>`;
    chatOutput.appendChild(userMessage);
    userInput.value = "";

    try {
        const response = await axios.post("/api/generate", {
            message: message,
            model_type: modelType
        });

        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerHTML = `<p>${response.data.response}</p>`;
        chatOutput.appendChild(botMessage);
    } catch (error) {
        console.error("Error sending message:", error);
        const errorMessage = document.createElement("div");
        errorMessage.className = "bot-message";
        errorMessage.innerHTML = `<p>无法生成响应，请稍后再试。</p>`;
        chatOutput.appendChild(errorMessage);
    } finally {
        isWaitingForResponse = false;
        document.getElementById("send-button").disabled = false;
    }

    chatOutput.scrollTop = chatOutput.scrollHeight;
}

document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
