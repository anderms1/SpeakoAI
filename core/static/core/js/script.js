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

const csrfToken = getCookie('csrftoken');


document.getElementById('editForm').addEventListener('submit',function(event){
    event.preventDefault();

    let formData = new FormData(this);

    fetch("/dashboard/edit_profile/", {
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
        }else{
            const messageElement = document.getElementById('response-message');
            messageElement.innerHTML = `<p>Los datos se han guardado correctamente.</p>`;

            document.getElementById('userName').textContent = `${data.first_name} ${data.last_name}`;
            setTimeout(() => {
                messageElement.innerHTML = ''; 
            }, 2000);
        }
    })
})