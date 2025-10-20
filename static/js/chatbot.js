document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const chatbotBox = document.getElementById('chatbot-box');
    const closeBtn = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chatbot-form');
    const chatMessages = document.getElementById('chatbot-messages');
    
    // Elementos del paso de nombre (Se mantienen para asegurar que el código no falle si el HTML sigue teniéndolos)
    const stepName = document.getElementById('chatbot-step-name');
    const stepMessage = document.getElementById('chatbot-step-message');
    const inputMsg = document.getElementById('chatbot-input');

    // **Nombre del usuario registrado (Reemplaza "Luna" con tu variable real)**
    let userName = "Luna"; 
    let initialGreetingSent = false; 

    // Función para enviar un mensaje al chat
    function appendMessage(text, cls) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ' + cls;
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // ===================================================================

    function botReply(message) {
        const msg = message.toLowerCase(); // Convertir a minúsculas para facilitar la búsqueda

        // Respuestas de saludo y despedida
        if (/hola|buenas/i.test(msg)) {
            return `¡Hola ${userName}! Bienvenido a El Restaurante Angello . ¿En qué puedo ayudarte?`;
        } else if (/adiós|bye|chau/i.test(msg)) {
            return "¡Hasta luego! Esperamos verte pronto en el Restaurante Angello. 😊";
        } 
        
        // ** 1. MENÚ / COMIDA / PLATOS **
        else if (/menú|carta|platos|comida|que venden|que ofrecen/i.test(msg)) {
            return "Nuestro menú es variado. Tenemos: Pollo a la Leña 🍗 , Pastas en salsa al alfredo, bolognesa y al pesto 🍴 , Pizzas 🍕. ¿Te interesa alguno en particular?";
        } 
        // ** 2. HORARIOS **
        else if (/horario|abren|cierran|a que hora/i.test(msg)) {
            return "Abrimos de Martes a Domingo de 3:00 PM a 11:00 PM."; 
        } 
        // ** 3. RESERVAS **
        else if (/reservar|reserva|mesa/i.test(msg)) {
            return "¡Claro! Puedes reservar una mesa llamando al (01) 555-1234 o directamente en nuestra web (link-de-reservas.com). ¿Para cuántas personas sería?";
        }
        // ** 4. UBICACIÓN / DIRECCIÓN **
        else if (/donde se ubican|dirección|como llego/i.test(msg)) {
            return "¡Nos ubicamos en Miguel Grau, San Vicente de Cañete 15701! Estamos justo al lado del Parque Principal.";
        }
        // ** 5. METODOS DE PAGO **
        else if (/pagar|pago|tarjeta|aceptan/i.test(msg)) {
            return "Aceptamos efectivo, tarjetas de crédito/débito (Visa, Mastercard) y pagos por Yape/Plin.";
        }
        // ** 6. ALERGIAS / DIETAS (NUEVA RESPUESTA) **
        else if (/alergia|gluten|vegetariano|vegano|dieta/i.test(msg)) {
            return "Por el momento, no tenemos opciones estrictamente vegetarianas o veganas en nuestro menú. Por favor, consulta con nuestro personal al momento de ordenar.";
        }
        // ** Fallback (Respuesta por defecto) **
        else {
            return "Gracias por tu mensaje. No entendí tu consulta. ¿Podrías preguntar sobre el menú, horarios, reservas o ubicación? ¡Con gusto te ayudo!";
        }
    }
    // ====================================================================

    // Lógica para mostrar/ocultar y enviar el saludo inicial
    toggleBtn.addEventListener('click', () => {
        chatbotBox.classList.toggle('hidden');
        
        if (!chatbotBox.classList.contains('hidden') && !initialGreetingSent) {
            // Oculta el paso de nombre (si existe)
            if (stepName) {
                stepName.classList.add('hidden');
            }
            // Muestra el paso de mensajes
            stepMessage.classList.remove('hidden'); 

            // Envía el saludo inicial con el nombre
            appendMessage(`¡Hola ${userName}! ¿Cómo te podemos ayudar?`, 'bot-message');
            inputMsg.focus();
            initialGreetingSent = true;
        }
    });
    
    closeBtn.addEventListener('click', () => {
        chatbotBox.classList.add('hidden');
    });

    // Paso 2: Mensaje (Lógica para enviar y recibir mensajes)
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
});