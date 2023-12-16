// Función para llenar campos cuando se selecciona un sitio web
function llenarCampos() {
    const sitioSeleccionado = document.getElementById('sitiosDataList').value;
    const sitiosOptions = document.getElementById('datalistOptions').getElementsByTagName('option');
  
    for (const option of sitiosOptions) {
      if (option.value === sitioSeleccionado) {
        // Llena los campos del formulario con la información del sitio web seleccionado
        document.getElementById('actualizarSitioNombre').value = option.value;
        document.getElementById('actualizarSitioUrl').value = option.getAttribute('data-url');
        document.getElementById('actualizarSitioRSS').value = option.getAttribute('data-rss');
        const sitioSeleccionadoId = option.getAttribute('data-id');
        actualizarSitioForm.action = '/actualizar_sitio_web/' + sitioSeleccionadoId + '/';
        break;
      } 
    }
  }
  
  // Asociar la función al evento onchange del input de la lista desplegable
  document.getElementById('sitiosDataList').onchange = llenarCampos;
  