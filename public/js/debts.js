let tableData = [];
let isEditing = false;
let editingIndex = null;

// Buscar en la tabla
function searchTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#dataTable tbody tr");

    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        const match = [...cells].some(cell => cell.textContent.toLowerCase().includes(input));
        row.style.display = match ? "" : "none";
    });
}

// Limpiar la búsqueda y restaurar la tabla
function clearSearch() {
    document.getElementById("searchInput").value = ""; // Limpiar el campo de búsqueda
    renderTable(); // Mostrar todos los datos nuevamente
}

// Añadir nueva categoría
function addNewCategory() {
    const newCategory = document.getElementById("newCategory").value.toUpperCase();
    if (newCategory) {
        const categorySelect = document.getElementById("category");
        const option = document.createElement("option");
        option.textContent = newCategory;
        option.value = newCategory;
        categorySelect.appendChild(option);
        categorySelect.value = newCategory; // Seleccionar la nueva categoría
        document.getElementById("newCategory").value = ""; // Limpiar campo
        document.getElementById("newCategoryContainer").style.display = "none"; // Ocultar el campo de entrada de nuevo rubro
    }
}

// Manejar formulario para añadir o modificar una fila
function handleFormSubmit(event) {
    event.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value).toFixed(2); // Convertir cantidad a formato decimal
    const date = document.getElementById("date").value;
    const category = document.getElementById("category").value;

    if (isEditing) {
        tableData[editingIndex] = { description, amount, date, category };
        showMessage("Modificado Exitosamente");
    } else {
        tableData.push({ description, amount, date, category });
        showMessage("Añadido Exitosamente");
    }

    renderTable();
    resetForm();
}

// Mostrar mensaje de éxito
function showMessage(message) {
    const successMessage = document.getElementById("successMessage");
    successMessage.textContent = message;
    successMessage.style.display = "block";
    setTimeout(() => successMessage.style.display = "none", 2000); // Ocultar mensaje después de 2 segundos
}

// Renderizar la tabla con datos actualizados
function renderTable() {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    tableData.forEach((data, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${data.description}</td>
            <td>$${data.amount}</td> <!-- Mostrar cantidad con símbolo de dólar -->
            <td>${data.date}</td>
            <td>${data.category}</td>
            <td><button onclick="editRow(${index})">Modificar</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Editar una fila existente
function editRow(index) {
    const data = tableData[index];
    document.getElementById("description").value = data.description;
    document.getElementById("amount").value = data.amount;
    document.getElementById("date").value = data.date;
    document.getElementById("category").value = data.category;

    isEditing = true;
    editingIndex = index;

    document.getElementById("menuTitle").textContent = "Modificar";
    document.getElementById("deleteButton").style.display = "inline-block";
}

// Eliminar la fila seleccionada
function deleteRow() {
    if (isEditing && editingIndex !== null) {
        tableData.splice(editingIndex, 1);
        renderTable();
        resetForm();
        showMessage("Borrado Exitosamente");
    }
}

// Resetear formulario y restablecer a modo de añadir
function resetForm() {
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("date").value = "";
    document.getElementById("category").value = "/COMIDA/";
    isEditing = false;
    editingIndex = null;

    document.getElementById("menuTitle").textContent = "Añadir";
    document.getElementById("deleteButton").style.display = "none";
}

// Evento de cambio en el selector de rubro para mostrar el campo de nuevo rubro
document.getElementById("category").addEventListener("change", function () {
    if (this.value === "add-new") {
        document.getElementById("newCategoryContainer").style.display = "block";
    } else {
        document.getElementById("newCategoryContainer").style.display = "none";
    }
});
