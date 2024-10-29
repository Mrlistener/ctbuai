// 监听回车键的事件，触发 sendMessage
document.getElementById("user-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();  // 防止默认的回车行为（如换行）
        sendMessage();  // 调用 sendMessage 函数发送消息
    }
});

async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const modelType = document.getElementById("model-selector").value;
    if (!userInput) return;

    const chatOutput = document.getElementById("chat-output");
    chatOutput.innerHTML += `<p class="user-message">${userInput}</p>`;
    document.getElementById("user-input").value = '';  // 清空输入框

    try {
        const response = await axios.post('/api/generate', {
            message: userInput,
            model_type: modelType
        });
        const botResponse = response.data.response;
        chatOutput.innerHTML += `<p class="bot-message">${botResponse}</p>`;
        chatOutput.scrollTop = chatOutput.scrollHeight;  // 自动滚动到底部
    } catch (error) {
        console.error("Error generating response:", error);
    }
}
