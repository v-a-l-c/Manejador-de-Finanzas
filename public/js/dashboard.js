// Imágenes para el fondo
const images = [
    "FondoDash1.jpg",
    "FondoDash2.jpg",
];

// Función para establecer un fondo aleatorio
function setRandomBackground() {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    const mainContent = document.querySelector('.main-content');
    mainContent.style.backgroundImage = `url('images/${randomImage}')`;
    mainContent.style.backgroundSize = 'cover';
    mainContent.style.backgroundPosition = 'center';
    mainContent.style.backgroundRepeat = 'no-repeat';
}

// Ejecutar la función al cargar la página
window.onload = setRandomBackground;

// Función para obtener los datos de gastos desde la API
async function getExpenseData(timePeriod) {
    const noDataMessage = document.getElementById('no-data-message');
    const chartContainer = document.getElementById('myChart');
    
    noDataMessage.style.display = 'none';
    chartContainer.style.display = 'none';

    try {
        const baseURL = 'http://172.16.238.10:5000/transactions/expenses/aot';
        const timeMap = {
            day: 'day',
            quincena: 'quincena',
            month: 'month',
            year: 'year',
        };

        if (!timeMap[timePeriod]) {
            throw new Error('Periodo no soportado');
        }

        const url = `${baseURL}${timeMap[timePeriod]}`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ date: new Date().toISOString() }),
        });

        if (!response.ok) {
            throw new Error(`Error al cargar los datos: ${response.status}`);
        }

        const data = await response.json();
        renderChart(data.resource, timePeriod); // Pasar timePeriod para personalizar el gráfico
    } catch (error) {
        console.error('Error:', error.message);
        noDataMessage.style.display = 'block';
    } finally {
        chartContainer.style.display = 'block';
    }
}

// Función para renderizar el gráfico con Chart.js
function renderChart(data, timePeriod) {
    const ctx = document.getElementById('myChart').getContext('2d');

    // Si no hay datos, usar valores por defecto
    if (!data || data.length === 0) {
        data = [{ date: '', amount: 0 }];
    }

    const labels = data.map(item => item.date);
    const amounts = data.map(item => item.amount);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [
                {
                    label: `Gastos por ${timePeriod}`,
                    data: amounts,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Fecha: ${context.label} - Monto: $${context.raw}`;
                        },
                    },
                },
            },
            scales: {
                y: { beginAtZero: true },
            },
        },
    });
}