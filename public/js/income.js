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

const addNewCategory = () => {
    const newCategoryValue = newCategoryInput.value.trim();
    if (newCategoryValue) {
        const newOption = document.createElement("option");
        newOption.value = newCategoryValue;
        newOption.textContent = newCategoryValue.toUpperCase();

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

function searchTable() {
    let inputField = document.getElementById("searchInput");
    let consulta = inputField.value;
    console.log("Entrada del usuario: " + consulta);
    searchTableAsync(consulta);
}


async function searchTableAsync(user_input) {
    let date = null, tag = null, fe_type = null;
    if (user_input.includes('date')|| user_input.includes('tag')){
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
    const response = await fetch("http://172.16.238.10:5000/transactions/incomes/search", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            date: date,
            type_of_date: fe_type,
            tag: tag
        }),
    });
    console.log(response);
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
          populateTable(resourceArray);
        } else {
            console.error("No se encontraron ingresos o hubo un error:", jsonResponse.message);
        }

    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

function generarpdf(){
  generarAsync();
}

async function generarAsync(){
  const response = await fetch("http://172.16.238.10:5000/transactions/incomes/pdf", {
      method: "GET",
      credentials: "include",
      /*headers: {
          "Content-Type": "application/json"
      }*/
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

document.addEventListener("DOMContentLoaded", loadIncomes);
