document.addEventListener("DOMContentLoaded", function() {

    console.log('JavaScript cargado correctamente');

    const csrfToken = getCookie('csrftoken');

    const editForm = document.getElementById('editForm');
    if(editForm){
        // Event listener para el formulario de edición de perfil
        editForm.addEventListener('submit', function(event){
            event.preventDefault();

            let formData = new FormData(this);

            fetch("/core/edit_profile/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.error){
                    document.getElementById('response-message').innerHTML = `<h2>${data.error}</h2>`;
                } else {
                    const messageElement = document.getElementById('response-message');
                    messageElement.innerHTML = `<p>Los datos se han guardado correctamente.</p>`;

                    document.getElementById('userName').textContent = `${data.first_name} ${data.last_name}`;
                    setTimeout(() => {
                        messageElement.innerHTML = ''; 
                    }, 2000);
                }
            });
        });
    }
    
});



document.addEventListener("DOMContentLoaded", function() {
    const changeButton = document.getElementById('cambiarBoton');

    if (changeButton) {
        changeButton.addEventListener('click', function(event){
            event.preventDefault();
            const traducirDe = document.getElementById('source');
            const traducirA = document.getElementById('target');
            const sourceText = document.getElementById('text');
            const targetText = document.getElementById('translation');


            if (traducirA.value !== "empty" && traducirDe.value !== "empty") {
                if(traducirA.value === "EN-US" && traducirDe.value === "EN"){
                    traducirA.value = "EN-US";
                    traducirDe.value = "EN";
                }else if(traducirA.value === "EN-US"){
                    const temp = "EN";
                    traducirA.value = traducirDe.value;
                    traducirDe.value = temp;
                }else{
                    const temp = traducirA.value
                    traducirA.value = traducirDe.value;
                    traducirDe.value = temp;
                }
                

                const tempText = sourceText.value;
                sourceText.value = targetText.value;
                targetText.value = tempText;
                realizarTraduccion();
            }
        });
    } else {
        console.error('changeButton not found');
    }

    const textArea = document.getElementById('text');
    const source = document.getElementById('source');
    const target = document.getElementById('target');

    if(textArea){
        textArea.addEventListener('input', realizarTraduccion);
    }

    if(source){
        source.addEventListener('change', realizarTraduccion);
    }
    
    if(target){
        target.addEventListener('change', realizarTraduccion);
    }
    
});


document.addEventListener("DOMContentLoaded", function() {
    const chatWindow = document.getElementById('chatWindow');
    const userMessage = document.getElementById("userMessage");
    const chatForm = document.getElementById("chatForm");
    

    chatForm.addEventListener('submit', function(event){
        event.preventDefault();

        const message = userMessage.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userMessage.value = "";

        fetch("/core/chat-api/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ message: message }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.response) {
                appendMessage("assistant", data.response);
            } else {
                console.error("Error:", data.error);
            }
        })
        .catch((error) => console.error("Error:", error));
    });

    function appendMessage(role, content) {
        const messageDiv = document.createElement("div");
        if (role === "user") {
            messageDiv.className = "message-user";
            messageDiv.innerHTML = `<span>${content}</span>`;
        } else {
            messageDiv.className = "message-assistant";
            messageDiv.innerHTML = `<span>${content}</span>`;
        }
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});




function realizarTraduccion(){
    const csrfToken = getCookie('csrftoken');
    const text = document.getElementById('text').value;
    const source = document.getElementById('source').value;
    const target = document.getElementById('target').value;

    if (text && source !== "empty" && target !== "empty") {
        fetch("/core/translate-api/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ text: text, source: source, target: target })
        })
        .then(response => response.json())
        .then(data => {
            if(data.translated_text){
                document.getElementById('translation').value = data.translated_text;
            }else{
                document.getElementById('translation').value = data.error;
                console.error('Error al traducir:', data.error);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    }
}


// Función para obtener el valor de la cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
