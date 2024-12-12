let tableData = [];
let isEditing = false;
let editingIndex = null;

// Buscar en la tabla
/*function searchTable() {
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
}*/

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
async function handleFormSubmit(event) {
    event.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value).toFixed(2); // Convertir cantidad a formato decimal
    const date = document.getElementById("date").value;
    const category = document.getElementById("category").value;

    if (isEditing) {
        tableData[editingIndex] = { description, amount, date, category };
        showMessage("Modificado exitosamente");
        renderTable();
        resetForm();
    } else {
        const expenseData = { description, amount, date, category };

        try {
            const response = await fetch("http://172.16.238.10:5000/transactions/expenses/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(expenseData),
            });

            const data = await response.json();

            if (response.ok) {
                console.log("Gasto añadido:", data);
                showMessage("Añadido exitosamente");
                loadExpenses();
                resetForm();
            }else {
                console.error("Error al añadir gasto:", data.message);
                showMessage("Error al añadir gasto");
            }
        } catch (error) {
            console.error("Error al enviar el gasto:", error);
            showMessage("Error al enviar el gasto");
        }
    }
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


async function loadExpenses() {
    const response = await fetch("http://172.16.238.10:5000/transactions/expenses/allexpenses", {
        method: "GET",
        credentials: "include"
    });

    if (!response.ok) {
        alert("No estás autenticado. Por favor, inicia sesión.");
        window.location.href = "/login.html";
        return;
    }

    try {
        const jsonResponse = await response.json();

        if (jsonResponse.status === "success" && Array.isArray(jsonResponse.data)) {
            const expenses = jsonResponse.data;
            populateExpensesTable(expenses);
        } else {
            console.error("No se encontraron gastos o hubo un error:", jsonResponse.message);
        }
    } catch (error) {
        console.error("Error al cargar los gastos:", error);
    }
}

function populateExpensesTable(expenses) {
    const dataTableBody = document.getElementById("expense-table-body");
    if (!dataTableBody) {
        console.error("El elemento de la tabla no se encuentra.");
        return;
    }

    dataTableBody.innerHTML = "";

    expenses.forEach((expense) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${expense.id}</td>
            <td>${expense.description}</td>
            <td>${expense.amount}</td>
            <td>${expense.date}</td>
            <td>${expense.category || "Sin rubro"}</td>
            <td>
                <button onclick="editExpense(${expense.id})">Editar</button>
                <button onclick="deleteExpense(${expense.id})">Eliminar</button>
            </td>
        `;

        dataTableBody.appendChild(row);
    });
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const expenseId = event.target.getAttribute("data-id");
            console.log("se llamará a delete");
            deleteExpense(expenseId);
        });
    });
}

function deleteExpense(expenseId) {
  console.log("se llamó a delete");
  deleteIncomeAsync(expenseId);
}

async function deleteIncomeAsync(expenseId) {
  const response = await fetch("http://172.16.238.10:5000/transactions/expenses/delete", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
          id: expenseId,
      }),
  });

  if (!response.ok) {
      alert("Ocurrió un problema al eliminar el egreso");
      return;
  }

  try {
      const jsonResponse = await response.json();

      if (jsonResponse.response === "success") {
          loadExpenses();
      } else {
          console.error("Hubo un error:", jsonResponse.message);
      }

  } catch (error) {
      console.error("Error en la solicitud:", error);
  }
}

function searchTable() {
    let inputField = document.getElementById("searchInput");
    let consulta = inputField.value;
    console.log("Entrada del usuario: " + consulta);
    searchTableAsync(consulta);
}

async function searchTableAsync(user_input) {
    let date = null, tag = null, fe_type = null;
    if (user_input.includes('date')||user_input.includes('tag')){
      const parts = user_input.split(',').map(part => part.trim());
      parts.forEach(part => {
          if (part.startsWith('date:')) {
              const feValue = part.split(':')[1].trim();
              if (feValue.includes('&')) {
                  const feParts = feValue.split('&');
                  date = feParts[0].trim();
                  fe_type = feParts[1].trim();
              } else {
                  fe = feValue;
                  fe_type = null;
              }
          } else if (part.startsWith('tag:')) {
              tag = part.split(':')[1].trim();
          } else {
            alert("Error en la búsqueda. Formato: date: xx-xx-xx (&d, &m, &y), tag:xxxx");
            return;
          }
        });
    } else {
      alert("Error en la búsqueda. Formato: date: xx-xx-xx (&d, &m, &y), tag:xxxx");
      return;
    }
    const response = await fetch("http://172.16.238.10:5000/transactions/expenses/search", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            date: date,
            type_of_date: fe_type,
            tag: tag
        }),
    });
    if (!response.ok) {
        alert("Error en la búsqueda.");
        return;
    }

    try {
        const jsonResponse = await response.json();

        if (jsonResponse.message === "transaction_search_returned") {
          const resourceArray = Object.values(jsonResponse.resource).map(item => {
            return {
                total: item.total || null,
                amount: item.amount || null,
                category: item.category || null,
                date: item.date || null,
                description: item.description || null
            };
          });
          resourceArray.shift();
          console.log(resourceArray);
          populateExpensesTable(resourceArray);
        } else {
            console.error("No se encontraron egresos o hubo un error:", jsonResponse.message);
        }

    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

function generarpdf(){
  generarAsync();
}

async function generarAsync(){
  const response = await fetch("http://172.16.238.10:5000/transactions/expenses/pdf", {
      method: "GET",
      credentials: "include",
  });

  if (!response.ok) {
      alert("Error");
      return;
  }

  try {
      const jsonResponse = await response.json();

      if (jsonResponse.response === "success") {
          console.log("Success");
      } else {
          console.error("Hubo un error:", jsonResponse.response);
      }

  } catch (error) {
      console.error("Error en la solicitud:", error);
  }
}

document.addEventListener("DOMContentLoaded", loadExpenses);
