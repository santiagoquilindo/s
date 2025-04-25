document.addEventListener("DOMContentLoaded", function () {
  const today = new Date().toISOString().split("T")[0];
  const fechaInput = document.getElementById("fecha");
  fechaInput.value=today;
  fechaInput.readOnly=true;
});


document
  .getElementById("formGuia")
  .addEventListener("submit", function (event) {
    event.preventDefault();




    const form = document.getElementById("formGuia");
    const formData = new FormData(form);

    fetch("/agregarguia", {
      method: "POST",
      body: formData,
    });
    alert("guardado guia")
      .then((response) => response.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        const alertContainer = doc.querySelector("#alert-container");
      });
  });


  