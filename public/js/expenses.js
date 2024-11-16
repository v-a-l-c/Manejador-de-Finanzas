let tableData = [];
let isEditing = false;
let editingIndex = null;

// Enviar un nuevo gasto al backend
async function submitExpense(expense) {
    try {
        const response = await fetch('http://172.24.0.3:5000/transactions/expenses/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expense),
        });

        if (response.ok) {
            const result = await response.json();
            showMessage(result.response || "Expense added successfully");
            fetchExpenses(); // Actualiza la tabla con los datos más recientes
        } else {
            const error = await response.json();
            alert("Error: " + (error.message || "Failed to add expense"));
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// Manejar la presentación del formulario para agregar o editar un gasto
function handleFormSubmit(event) {
    event.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value).toFixed(2);
    const date = document.getElementById("date").value;

    const expense = { description, amount, date };

    if (isEditing) {
        tableData[editingIndex] = expense;
        showMessage("Modified Successfully");
        isEditing = false;
        editingIndex = null;
    } else {
        submitExpense(expense); // Enviar el gasto al backend
    }

    renderTable();
    resetForm();
}

// Obtener gastos del backend (diario, mensual o anual)
async function fetchExpenses(period = 'day') {
    const endpoint = `http://172.24.0.3:5000/transactions/expenses/${period}`;
    const date = document.getElementById("date").value; // Usa la fecha seleccionada para obtener datos

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ date: date }),
        });

        if (response.ok) {
            const data = await response.json();
            tableData = data.resource || [];
            renderTable();
        } else {
            const error = await response.json();
            alert("Error: " + (error.message || "Failed to fetch expenses"));
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// Renderizar la tabla con los datos de los gastos
function renderTable() {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    tableData.forEach((data, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${data.description}</td>
            <td>$${parseFloat(data.amount).toFixed(2)}</td>
            <td>${data.date}</td>
            <td><button onclick="editRow(${index})">Modify</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Mostrar un mensaje de éxito
function showMessage(message) {
    const successMessage = document.getElementById("successMessage");
    successMessage.textContent = message;
    successMessage.style.display = "block";
    setTimeout(() => successMessage.style.display = "none", 2000);
}

// Editar una fila en la tabla
function editRow(index) {
    const data = tableData[index];
    document.getElementById("description").value = data.description;
    document.getElementById("amount").value = data.amount;
    document.getElementById("date").value = data.date;

    isEditing = true;
    editingIndex = index;

    document.getElementById("menuTitle").textContent = "Modify";
    document.getElementById("deleteButton").style.display = "inline-block";
}

// Reiniciar el formulario y el estado
function resetForm() {
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("date").value = "";
    isEditing = false;
    editingIndex = null;

    document.getElementById("menuTitle").textContent = "Add";
    document.getElementById("deleteButton").style.display = "none";
}

// Búsqueda en la tabla
function searchTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#dataTable tbody tr");

    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        const match = [...cells].some(cell => cell.textContent.toLowerCase().includes(input));
        row.style.display = match ? "" : "none";
    });
}

// Limpiar el campo de búsqueda
function clearSearch() {
    document.getElementById("searchInput").value = "";
    renderTable();
}

// Función para cargar la tabla al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    fetchExpenses('day'); // Por defecto, obtener gastos diarios
});

