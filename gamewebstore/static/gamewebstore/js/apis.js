// api clipboard
function copiarEmail() {
    const email = document.getElementById('mail').innerText;
    const iconoCopiar = document.getElementById('iconoCopiar');
    const alerta = document.getElementById('alerta-email-copy');
    const card = document.querySelector('.card'); // Contenedor '.card'

    navigator.clipboard.writeText(email)
        .then(() => {
            const iconoPos = iconoCopiar.getBoundingClientRect();
            const cardPos = card.getBoundingClientRect();

            alerta.style.left = `${iconoPos.left - cardPos.left - 40}px`;
            alerta.style.top = `${iconoPos.top - cardPos.top - alerta.offsetHeight - 50}px`;
            alerta.style.display = 'block';

            console.log('Correo electrónico copiado: ' + email);

            setTimeout(() => {
                alerta.style.display = 'none';
            }, 1000);
        })
        .catch(err => {
            console.error('Error al copiar el correo electrónico:', err);
        });
}

function copiarTelefono() {
    const telefono = document.getElementById('telefono').innerText;
    const iconoCopiar2 = document.getElementById('iconoCopiar2');
    const alerta = document.getElementById('alerta-tel-copy');
    const card = document.querySelector('.card');

    navigator.clipboard.writeText(telefono)
        .then(() => {
            const iconoPos = iconoCopiar2.getBoundingClientRect();
            const cardPos = card.getBoundingClientRect();
            alerta.style.left = `${iconoPos.left - cardPos.left - 40}px`;
            alerta.style.top = `${iconoPos.top - cardPos.top - alerta.offsetHeight - 50}px`;
            alerta.style.display = 'block';

            console.log('Número de teléfono copiado: ' + telefono);

            setTimeout(() => {
                alerta.style.display = 'none';
            }, 1000);
        })
        .catch(err => {
            console.error('Error al copiar el número de teléfono:', err);
        });
}

//api gato random
const url = "https://api.thecatapi.com/v1/images/search";
const section = document.querySelector(".container");
const button = document.querySelector(".btn");

button.addEventListener("click", getRandomCats);

randomCatPhoto = (json) => {
    let photo = json[0].url;
    section.classList.add("cats");

    // Verifica si ya existe una imagen y la elimina
    const existingImage = document.querySelector(".random_cats");
    if (existingImage) {
        section.removeChild(existingImage);
    }

    let image = document.createElement("img");
    image.src = photo;
    image.classList.add("random_cats");
    // Texto alternativo descriptivo para la imagen
    image.alt = "Foto aleatoria de un gato";
    section.appendChild(image);
};

async function getRandomCats() {
    section.innerHTML = "";
    try {
        const response = await fetch(url);
        const json = await response.json();
        console.log("JSON:", json);
        return randomCatPhoto(json);
    } catch (e) {
        // Muestra un mensaje de error en la interfaz de usuario
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Error, el gatito no se puede mostrar en este momento.";
        section.appendChild(errorMessage);
        console.log("Error, el gatito no se puede mostrar");
        console.log(e);
    }
}