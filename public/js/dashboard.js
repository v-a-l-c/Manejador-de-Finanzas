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
let selectedTimespan = '';




document.querySelectorAll('#timeMenu li').forEach((item) => {
    item.addEventListener('click', (e) => {
        const timespan = e.target.dataset.timespan;
        setTimespan(timespan);
    });
});

async function graphData() {
    if (!selectedTimespan) {
        alert('Selecciona un periodo antes de graficar');
        return;
    }

    const noDataMessage = document.getElementById('no-data-message');
    const chartContainer = document.getElementById('myChart');
    
    noDataMessage.style.display = 'none';
    chartContainer.style.display = 'none';

    try {
        const baseURL = 'http://172.16.238.10:5000/transactions/expenses/allexpenses';
        const response = await fetch(baseURL, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`Error al cargar los datos: ${response.status}`);
        }

        const data = await response.json();
        const processedData = processExpenses(data.data, selectedTimespan);
        renderChart(processedData, selectedTimespan);
    } catch (error) {
        console.error('Error:', error.message);
        noDataMessage.style.display = 'block';
    } finally {
        chartContainer.style.display = 'block';
    }
}

function processExpenses(expenses, timePeriod) {
    const groupBy = {
        day: (date) => date.toISOString().split('T')[0], // YYYY-MM-DD
        month: (date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        year: (date) => date.getFullYear().toString(),
    };

    const groupFunc = groupBy[timePeriod];
    if (!groupFunc) throw new Error('Periodo no soportado');

    const groupedExpenses = {};
    expenses.forEach((expense) => {
        const date = new Date(expense.date);
        const key = groupFunc(date);
        groupedExpenses[key] = (groupedExpenses[key] || 0) + expense.amount;
    });

    return Object.entries(groupedExpenses)
        .map(([key, total]) => ({ period: key, total }))
        .sort((a, b) => new Date(a.period) - new Date(b.period));
}

function renderChart(data, timePeriod) {
    const ctx = document.getElementById('myChart').getContext('2d');

    if (window.myChart instanceof Chart) {
        window.myChart.destroy();
    }

    const labels = data.map(item => item.period);
    const amounts = data.map(item => item.total);

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: `Gastos por ${timePeriod}`,
                    data: amounts,
                    fill: true,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: (context) => `Periodo: ${context.label} - Monto: $${context.raw}`,
                    },
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: (value) => `$${value}` },
                },
            },
        },
    });
}

function toggleMenu() {
    const menu = document.getElementById('timeMenu');
    const isVisible = window.getComputedStyle(menu).display !== 'none';
    menu.style.display = isVisible ? 'none' : 'block';
}

function setTimespan(timespan) {
    selectedTimespan = timespan;
    document.getElementById('timeSelectButton').innerText = `Periodo seleccionado: ${timespan}`;
    document.getElementById('graphButton').disabled = false; 
    toggleMenu(); 
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('timeSelectButton').addEventListener('click', toggleMenu);
    document.querySelectorAll('#timeMenu li').forEach((item) => {
        item.addEventListener('click', (e) => {
            const timespan = e.target.dataset.timespan;
            setTimespan(timespan);
        });
    });
    document.getElementById('graphButton').addEventListener('click', graphData);
});


document.getElementById('graphButton').addEventListener('click', graphData);
