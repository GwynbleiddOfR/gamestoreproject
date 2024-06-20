// ****************** Registro  ******************

// Validar genero
function validarGender() {
    const opciones = document.getElementsByName("inlineRadioOptions");
    let mensajeGender = document.getElementById("mensajeGender");
    let seleccionado = false;

    for (const opcion of opciones) {
        if (opcion.checked) {
            seleccionado = true;
            mensajeGender.textContent = "";
            break;
        }
    }

    if (!seleccionado) {
        mensajeGender.textContent = "Seleccione una opción";
        return false;
    }

    return true;
}

// Validar contraseña
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.href.match(/register\.html$/)) {
      // Añade los event listeners solo si la página es register.html
      document.getElementById("pass").addEventListener("keyup", validarPass);
      document.getElementById("rePass").addEventListener("keyup", validarPass);
    }
});
  
function validarPass() {
    let pass = document.getElementById("pass").value;
    let rePass = document.getElementById("rePass").value;
    let mensajePass = document.getElementById("mensajePass");

    if (pass.length >= 8) {
        if (pass === rePass) {
            mensajePass.className = "text-success";
            mensajePass.textContent = "Las contraseñas coinciden ✅.";
        } else {
            mensajePass.className = "text-danger";
            mensajePass.textContent = "Las contraseñas no coinciden ❌.";
        }
    }
}  

function mostrarPass(){
    let contra = document.getElementById("pass");
    let reContra = document.getElementById("rePass");

    if (contra.type === "password") {
        contra.type = "text";
        reContra.type = "text";
    } else {
        contra.type = "password";
        reContra.type = "password";
    }
}

document.getElementById('telefono').addEventListener('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

// Primera letra de nombre, apellido, ciudad y comuna siempre en mayuscula
function primeraLetraMayuscula(id) {
    let input = document.getElementById(id);
    input.addEventListener('input', function (e) {
        let valor = e.target.value;
        e.target.value = valor.charAt(0).toUpperCase() + valor.slice(1);
    });
}

// Aplicar las funciones
primeraLetraMayuscula('nombre');
primeraLetraMayuscula('apellido');

// Funcion que permite usar el maxlength en type number
function validarLongitudInput(inputId, maxLength) {
    var inputElement = document.getElementById(inputId);
    var valor = inputElement.value;

    valor = valor.replace(/-/g, '');

    if (valor.length > maxLength) {
        valor = valor.slice(0, maxLength);
    }

    inputElement.value = valor;
}

// ********** CARRITO **********
// Formato fecha
function validarFecha(input) {
    let formatoFecha = /^(0[1-9]|1[0-2])\/\d{4}$/;
    let valor = input.value.replace(/\D/g, '').replace(/(.{2})/, '$1/');
  
    valor = valor.substring(0, 7);
  
    if (valor.length === 2) {
      valor += '/';
    }
  
    input.value = valor;

    if (!formatoFecha.test(valor) && valor.length === 7) {
      console.log('Formato incorrecto, debe ser MM/YYYY');
    }
  }

// Solo numeros
function soloNumeros(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
  }