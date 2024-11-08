document.addEventListener("DOMContentLoaded", () => {
    const updateUserForm = document.getElementById("update-user-form");
    const updateEmailForm = document.getElementById("update-email-form");
    const updatePasswordForm = document.getElementById("update-password-form");

    // Nombre de usuario
    updateUserForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const newUsername = document.getElementById("new-username").value;
        const confirmUsername = document.getElementById("confirm-username").value;

        if (newUsername === confirmUsername) {
            try {
                const response = await fetch("http://172.19.0.3:5000/auth/update_username", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: newUsername }),
                });

                if (response.ok) alert("Nombre de usuario actualizado");
                else alert("Error al actualizar nombre de usuario.");
            } catch (error) {
                console.error(error);
                alert("Error en el servidor.");
            }
        } else {
            alert("Los nombres de usuario no coinciden.");
        }
    });

    // Correo 
    updateEmailForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const newEmail = document.getElementById("new-email").value;
        const confirmEmail = document.getElementById("confirm-email").value;

        if (newEmail === confirmEmail) {
            try {
                const response = await fetch("/auth/update_email", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email: newEmail }),
                });

                if (response.ok) alert("Correo actualizado");
                else alert("Error al actualizar correo.");
            } catch (error) {
                console.error(error);
                alert("Error en el servidor.");
            }
        } else {
            alert("Los correos no coinciden.");
        }
    });

    // Contraseña
    updatePasswordForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const newPassword = document.getElementById("new-password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (newPassword === confirmPassword) {
            try {
                const response = await fetch("/auth/update_password", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ password: newPassword }),
                });

                if (response.ok) alert("Contraseña actualizada");
                else alert("Error al actualizar contraseña.");
            } catch (error) {
                console.error(error);
                alert("Error en el servidor.");
            }
        } else {
            alert("Las contraseñas no coinciden.");
        }
    });
});
