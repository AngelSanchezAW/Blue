// Script para mostrar dinámicamente la vista previa de una publicación en un modal de Bootstrap.
document.addEventListener("DOMContentLoaded", function() {
  const modal = document.getElementById("vistaPreviaModal");

  modal.addEventListener("show.bs.modal", function(event) {
    const button = event.relatedTarget; // Button that triggered the modal
    const publicacionId = button.getAttribute("data-publicacion-id"); // Extract info from data-* attributes
    
    fetch(`/get_publication_details/?publicacion_id=${publicacionId}`)
      .then(response => response.json())
      .then(data => {
        const modalBody = document.getElementById("modalBody");
        modalBody.innerHTML = `
          <div class="container CuerpoVistaPreviaPost">
            <p class="infoPost">Presentado por ${data.nombreSitioWeb}</p>
            <h2>${data.titulo}</h2>
            <p class="infoPost">Publicado originalmente en <a href="${data.urlSitioWeb}">${data.nombreSitioWeb}</a> puedes leer el articulo original aquí: <a href="${data.postUrl}">${data.titulo}</a></p>
            <img src="${data.imagenPortada}">
            <hr>
            <div>${data.extracto}</div>
          </div>
        `;
      })
      .catch(error => {
        console.log("Error fetching publication details", error);
      });
  });
});