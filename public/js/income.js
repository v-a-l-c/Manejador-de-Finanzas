incomeForm = document.getElementById("actionForm");
incomeForm.addEventListener("submit", async (event) =>{  

    event.preventDefault();

    const current_amount = document.getElementById("amount").value;
    const current_description = document.getElementById("description").value;
    const current_date = document.getElementById("date").value;
    try {
        const response = await fetch("http://172.16.238.10:5000/transactions/incomes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({amount: current_amount, description: current_description, date: current_date}),
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
            incomeForm.reset();
        }
    } catch(error){
        console.log(error);
    }
});

