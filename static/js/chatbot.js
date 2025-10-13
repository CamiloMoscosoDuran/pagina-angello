document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.getElementById('chatbot-toggle');
  const chatbotBox = document.getElementById('chatbot-box');
  const closeBtn = document.getElementById('chatbot-close');
  const chatForm = document.getElementById('chatbot-form');
  const chatMessages = document.getElementById('chatbot-messages');
  const stepName = document.getElementById('chatbot-step-name');
  const stepMessage = document.getElementById('chatbot-step-message');
  const inputName = document.getElementById('chatbot-input-name');
  const nextBtn = document.getElementById('chatbot-next');
  const inputMsg = document.getElementById('chatbot-input');

  let userName = "";

  // Mostrar/ocultar ventana
  toggleBtn.addEventListener('click', () => {
    chatbotBox.classList.toggle('hidden');
  });
  closeBtn.addEventListener('click', () => {
    chatbotBox.classList.add('hidden');
  });

  // Paso 1: Nombre
  nextBtn.addEventListener('click', function() {
    const name = inputName.value.trim();
    if (!name) return;
    userName = name;
    appendMessage(`Nombre: ${userName}`, 'user-message');
    appendMessage(`¡Hola ${userName}! ¿Cómo te podemos ayudar?`, 'bot-message');
    stepName.classList.add('hidden');
    stepMessage.classList.remove('hidden');
    inputMsg.focus();
  });

  // Paso 2: Mensaje
  chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const text = inputMsg.value.trim();
    if (!text) return;

    appendMessage(text, 'user-message');
    setTimeout(() => {
      appendMessage(botReply(text), 'bot-message');
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 600);
    inputMsg.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
  });

  function appendMessage(text, cls) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + cls;
    msgDiv.textContent = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function botReply(message) {
    if (/hola|buenas/i.test(message)) {
      return `¡Hola ${userName}! Bienvenido a nuestro restaurante ¿En qué puedo ayudarte?`;
    } else if (/adiós|bye/i.test(message)) {
      return "¡Hasta luego! 😊";
    } else if (/en donde se ubican/i.test(message)) {
      return "¡Nos ubicamos en  Miguel Grau, San Vicente de Cañete 15701!";
    } else {
      return "No entendí tu mensaje. ¿Puedes reformularlo?";
    }
  }
});