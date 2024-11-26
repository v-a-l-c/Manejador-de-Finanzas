document.getElementById("signup-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        username: formData.get("username"),
        password: formData.get("password"),
        mail: formData.get("mail"),
        firstName: formData.get("firstName") || undefined, 
        secondNames: formData.get("secondNames") || undefined,  
        curp: formData.get("curp") || undefined,  
        rfc: formData.get("rfc") || undefined  
    };

    try {
        const response = await fetch("http://172.16.238.10:5000/auth/", {  
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        
        const responseMessage = document.getElementById("signup-response");


        let result;
        try {
            result = await response.json();
        } catch (error) {
            console.error("Error al analizar la respuesta JSON:", error);
            result = { message: "Error en el servidor" };
        }

        if (response.ok) {
            responseMessage.textContent = "Usuario registrado exitosamente";
            responseMessage.style.color = "green";

            window.location.href = "/dashboard.html";
        } else {
            responseMessage.textContent = result.message || "Error en el registro";
            responseMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Error en la solicitud de registro:", error);
    }
});