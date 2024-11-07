document.getElementById("signup-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        username: formData.get("username"),
        password: formData.get("password"),
        mail: formData.get("mail")
    };

    try {
        const response = await fetch("http://backend:5000/auth/", {  // URL actualizada
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        const responseMessage = document.getElementById("signup-response");
        if (response.ok) {
            responseMessage.textContent = "Usuario registrado exitosamente";
            responseMessage.style.color = "green";
            // Redirecciona al dashboard, antes solo el mensaje
            window.location.href = "/dashboard.html";
        } else {
            responseMessage.textContent = result.message || "Error en el registro";
            responseMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Error:", error);
    }
});
