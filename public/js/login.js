document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        username: formData.get("username"),
        password: formData.get("password")
    };

    try {
        const response = await fetch("http://172.16.238.10:5000/auth/login", {  // URL actualizada
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        const responseMessage = document.getElementById("login-response");
        if (response.ok && result.response === "success") {
            responseMessage.textContent = "Inicio de sesión exitoso";
            responseMessage.style.color = "green";
            // Redirecciona al dashboard, anteriormente solo daba el mensaje
            window.location.href = "/dashboard.html";
        } else if (result.response === "no_user_found") {
            responseMessage.textContent = "Usuario no encontrado";
            responseMessage.style.color = "red";
        } else if (result.response === "no_access") {
            responseMessage.textContent = "Contraseña incorrecta";
            responseMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Error:", error);
    }
});
