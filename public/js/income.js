let incomeTableData = [];
let isEditingIncome = false;
let editingIncomeIndex = null;

// Enviar un nuevo ingreso al backend
async function submitIncome(income) {
    try {
        const response = await fetch('http://172.24.0.3:5000/transactions/incomes/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(income),
        });

        if (response.ok) {
            const result = await response.json();
            showIncomeMessage(result.response || "Income added successfully");
            fetchIncomes(); // Actualiza la tabla con los datos más recientes
        } else {
            const error = await response.json();
            alert("Error: " + (error.message || "Failed to add income"));
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// Manejar la presentación del formulario para agregar o editar un ingreso
function handleIncomeFormSubmit(event) {
    event.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value).toFixed(2);
    const date = document.getElementById("date").value;

    const income = { description, amount, date };

    if (isEditingIncome) {
        incomeTableData[editingIncomeIndex] = income;
        showIncomeMessage("Modified Successfully");
        isEditingIncome = false;
        editingIncomeIndex = null;
    } else {
        submitIncome(income); // Enviar el ingreso al backend
    }

    renderIncomeTable();
    resetIncomeForm();
}

// Obtener ingresos del backend (diario, mensual o anual)
async function fetchIncomes(period = 'per-day') {
    const endpoint = `http://172.24.0.3:5000/transactions/incomes/${period}`;
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
            incomeTableData = data.resource || [];
            renderIncomeTable();
        } else {
            const error = await response.json();
            alert("Error: " + (error.message || "Failed to fetch incomes"));
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// Renderizar la tabla con los datos de los ingresos
function renderIncomeTable() {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    incomeTableData.forEach((data, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${data.description}</td>
            <td>$${parseFloat(data.amount).toFixed(2)}</td>
            <td>${data.date}</td>
            <td><button onclick="editIncomeRow(${index})">Modify</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Mostrar un mensaje de éxito
function showIncomeMessage(message) {
    const successMessage = document.getElementById("successMessage");
    successMessage.textContent = message;
    successMessage.style.display = "block";
    setTimeout(() => successMessage.style.display = "none", 2000);
}

// Editar una fila en la tabla de ingresos
function editIncomeRow(index) {
    const data = incomeTableData[index];
    document.getElementById("description").value = data.description;
    document.getElementById("amount").value = data.amount;
    document.getElementById("date").value = data.date;

    isEditingIncome = true;
    editingIncomeIndex = index;

    document.getElementById("menuTitle").textContent = "Modify";
    document.getElementById("deleteButton").style.display = "inline-block";
}

// Reiniciar el formulario y el estado
function resetIncomeForm() {
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("date").value = "";
    isEditingIncome = false;
    editingIncomeIndex = null;

    document.getElementById("menuTitle").textContent = "Add";
    document.getElementById("deleteButton").style.display = "none";
}

// Búsqueda en la tabla de ingresos
function searchIncomeTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#dataTable tbody tr");

    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        const match = [...cells].some(cell => cell.textContent.toLowerCase().includes(input));
        row.style.display = match ? "" : "none";
    });
}

// Limpiar el campo de búsqueda
function clearIncomeSearch() {
    document.getElementById("searchInput").value = "";
    renderIncomeTable();
}

// Función para cargar la tabla al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    fetchIncomes('per-day'); // Por defecto, obtener ingresos diarios
});
