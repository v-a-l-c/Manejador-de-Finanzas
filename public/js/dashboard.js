const images = [
    "FondoDash1.jpg",
    "FondoDash2.jpg",
];

function setRandomBackground() {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    
    const mainContent = document.querySelector('.main-content');
    mainContent.style.backgroundImage = `url('images/${randomImage}')`;
    mainContent.style.backgroundSize = 'cover';        
    mainContent.style.backgroundPosition = 'center';   
    mainContent.style.backgroundRepeat = 'no-repeat';  
}

window.onload = setRandomBackground;

async function getExpenseData(timePeriod) {
    try {
        let url = '';

        if (timePeriod === 'day') {
            url = '172.16.238.10:5000/transactions/expenses/aotday';
        } else if (timePeriod === 'month') {
            url = '172.16.238.10:50000/transactions/expenses/aotmonth';
        } else if (timePeriod === 'year') {
            url = '172.16.238.10:5000transactions/expenses/aotyear';
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ date: new Date().toISOString() })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        console.log(data);

        renderChart(data.resource);
    } catch (error) {
        console.error("Error loading chart data:", error.message);
    }
}



function renderChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    if (!data || data.length === 0) {
        data = [{ date: '', amount: 0 }]; 
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.date), 
            datasets: [{
                label: 'Gasto Total',
                data: data.map(item => item.amount),  
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItem) {

                            return tooltipItem[0].raw ? tooltipItem[0].label : 'No disponible';
                        }
                    }
                }
            }
        }
    });
}

