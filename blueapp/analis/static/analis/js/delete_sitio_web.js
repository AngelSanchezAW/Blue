document.addEventListener("DOMContentLoaded", function() {
  const deleteButtons = document.querySelectorAll(".borrar-sitio-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function() {
      const sitioWebId = this.id.split("-")[4];
      console.log(sitioWebId)
      if (confirm("¿Estás seguro de que deseas eliminar este sitio web?")) {
        // Realiza una solicitud fetch para eliminar el sitio web
        fetch(`/borrar_sitio_web/${sitioWebId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            // Elimina visualmente el elemento del DOM si la eliminación es exitosa
            if ("mensaje" in data) {
              const sitioWebElement = document.getElementById(`sitio-web-${sitioWebId}`);
              sitioWebElement.parentNode.removeChild(sitioWebElement);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    });
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
});
