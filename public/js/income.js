incomeForm = document.getElementById("actionForm");


const categorySelect = document.getElementById("category");
const newCategoryContainer = document.getElementById("newCategoryContainer");
const newCategoryInput = document.getElementById("newCategory");

categorySelect.addEventListener("change", () => {
    if (categorySelect.value === "add-new") {
        newCategoryContainer.style.display = "block";
        newCategoryInput.focus();
    } else {
        newCategoryContainer.style.display = "none";
        newCategoryInput.value = "";
    }
});

function addNewCategory() {
    const newCategoryValue = newCategoryInput.value.trim();
    if (newCategoryValue) {
        const newOption = document.createElement("option");
        newOption.value = newCategoryValue.toUpperCase();
        newOption.textContent = newCategoryValue;

        categorySelect.appendChild(newOption);
        categorySelect.value = newCategoryValue.toUpperCase();

        newCategoryContainer.style.display = "none";
        newCategoryInput.value = "";
    } else {
        alert("Por favor, ingresa un nombre para el nuevo rubro.");
    }
}

incomeForm.addEventListener("submit", async (event) =>{

    event.preventDefault();

    const current_amount = document.getElementById("amount").value;
    const current_description = document.getElementById("description").value;
    const current_date = document.getElementById("date").value;
    const  current_tag = document.getElementById("category").value;
    try {
        const response = await fetch("http://172.16.238.10:5000/transactions/incomes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                amount: current_amount,
                description: current_description,
                date: current_date,
                tag: current_tag
            }),
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
            incomeForm.reset();
            loadIncomes();
            showMessage("Nuevo ingreso añadido") 
        }
    } catch(error){
        console.log(error);
    }
});
// Mostrar mensaje de éxito
function showMessage(message) {
    const successMessage = document.getElementById("successMessage");
    successMessage.textContent = message;
    successMessage.style.display = "block";
    setTimeout(() => successMessage.style.display = "none", 2000); // Ocultar mensaje después de 2 segundos
}





async function loadIncomes() {
    const response = await fetch("http://172.16.238.10:5000/transactions/incomes/allincomes", {
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
            const incomes = jsonResponse.data;
            populateTable(incomes);
        }else {
            console.error("No se encontraron ingresos o hubo un error:", jsonResponse.message);
        }

    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

function populateTable(incomes) {
    const dataTableBody = document.getElementById("data-table-body");
    if (!dataTableBody) {
        console.error("El elemento de la tabla no se encuentra.");
        return;
    }

    dataTableBody.innerHTML = "";

    incomes.forEach((income) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${income.id}</td>
            <td>${income.description}</td>
            <td>${income.amount}</td>
            <td>${income.date}</td>
            <td>${income.category || "Sin rubro"}</td>
            <td>
                <button onclick="editIncome(${income.id})">Editar</button>
                <button onclick="deleteIncome(${income.id})">Eliminar</button>
            </td>
        `;

        dataTableBody.appendChild(row);
    });
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const incomeId = event.target.getAttribute("data-id");
            console.log("se llamará a delete");
            deleteIncome(incomeId);
        });
    });
}

function deleteIncome(incomeId) {
  console.log("se llamó a delete");
  deleteIncomeAsync(incomeId);
}

async function deleteIncomeAsync(income_id) {
  const response = await fetch("http://172.16.238.10:5000/transactions/incomes/delete", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
          id: income_id,
      }),
  });

  if (!response.ok) {
      alert("Ocurrió un problema al eliminar el ingreso");
      return;
  }

  try {
      const jsonResponse = await response.json();

      if (jsonResponse.response === "success") {
          loadIncomes();
      } else {
          console.error("Hubo un error:", jsonResponse.message);
      }

  } catch (error) {
      console.error("Error en la solicitud:", error);
  }
}

document.addEventListener("DOMContentLoaded", loadIncomes);
