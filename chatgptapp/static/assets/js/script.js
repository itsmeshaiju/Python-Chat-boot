const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");

const createChatElement = (content, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv;
}

const getChatResponse = async () => {
    const API_URL = "/generate_content/";
    const pElement = document.createElement("p");

    const formData = new FormData();
    formData.append('question', chatInput.value.trim());

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (response.ok) {
            pElement.textContent = data.answer;
            displayQuestionAnswer(chatInput.value.trim(), data.answer);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
    }

    chatInput.value = "";
    chatInput.style.height = "40px";
}

const displayQuestionAnswer = (question, answer) => {
    const questionHtml = `<div class="chat-content">
                            <div class="chat-details">
                              <div class="chat-response">
                                <p><strong>Question:</strong> ${question}</p>
                              </div>
                            </div>
                          </div>`;

    const answerHtml = `<div class="chat-content">
                            <div class="chat-details">
                              <div class="chat-response">
                                <p><strong>Answer:</strong> ${answer}</p>
                              </div>
                            </div>
                          </div>`;

    const outgoingChatDiv = createChatElement(questionHtml, "outgoing");
    chatContainer.appendChild(outgoingChatDiv);

    setTimeout(() => {
        const answerChatDiv = createChatElement(answerHtml, "outgoing");
        chatContainer.appendChild(answerChatDiv);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    }, 1000);
}

themeButton.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

sendButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (chatInput.value.trim()) {
        getChatResponse();
    }
});

chatInput.addEventListener("input", () => {
    chatInput.style.height = "40px";
    chatInput.style.height = `${Math.min(chatInput.scrollHeight, 150)}px`;
});
