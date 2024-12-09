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
        day: (date) => date.toISOString().split('T')[0], 
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
    document.getElementById('graphIncomesButton').disabled = false; 
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

document.getElementById('graphIncomesButton').addEventListener('click', graphIncomes);

async function graphIncomes() {
    if (!selectedTimespan) {
        alert('Selecciona un periodo antes de graficar');
        return;
    }

    const noDataMessage = document.getElementById('no-incomes-data-message');
    const chartContainer = document.getElementById('incomesChart');

    noDataMessage.style.display = 'none';
    chartContainer.style.display = 'none';

    try {
        const baseURL = 'http://172.16.238.10:5000/transactions/incomes/allincomes';
        const response = await fetch(baseURL, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`Error al cargar los datos: ${response.status}`);
        }

        const data = await response.json();
        const processedData = processIncomes(data.data, selectedTimespan);
        renderIncomeChart(processedData, selectedTimespan);
    } catch (error) {
        console.error('Error:', error.message);
        noDataMessage.style.display = 'block';
    } finally {
        chartContainer.style.display = 'block';
    }
}

function processIncomes(incomes, timePeriod) {
    const groupBy = {
        day: (date) => date.toISOString().split('T')[0], // YYYY-MM-DD
        month: (date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        year: (date) => date.getFullYear().toString(),
    };

    const groupFunc = groupBy[timePeriod];
    if (!groupFunc) throw new Error('Periodo no soportado');

    const groupedIncomes = {};
    incomes.forEach((income) => {
        const date = new Date(income.date);
        const key = groupFunc(date);
        groupedIncomes[key] = (groupedIncomes[key] || 0) + income.amount;
    });

    return Object.entries(groupedIncomes)
        .map(([key, total]) => ({ period: key, total }))
        .sort((a, b) => new Date(a.period) - new Date(b.period));
}

function renderIncomeChart(data, timePeriod) {
    const ctx = document.getElementById('incomesChart').getContext('2d');

    if (window.incomesChart instanceof Chart) {
        window.incomesChart.destroy();
    }

    const labels = data.map(item => item.period);
    const amounts = data.map(item => item.total);

    window.incomesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: `Ingresos por ${timePeriod}`,
                    data: amounts,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
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


async function loadExpenseChart() {
    const chartContainer = document.getElementById('expensePieChart');
    const noDataMessage = document.getElementById('noDataMessageExpenses');

    if (!chartContainer || !noDataMessage) {
        console.error('No se encontraron los elementos del gráfico');
        return;
    }

    noDataMessage.style.display = 'none';
    chartContainer.style.display = 'none';

    try {
        const apiURL = 'http://172.16.238.10:5000/transactions/expenses/allexpenses';
        const response = await fetch(apiURL, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`Error al cargar los datos: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Datos recibidos:', responseData);

        if (responseData.status === 'success' && Array.isArray(responseData.data) && responseData.data.length > 0) {
            const tagData = groupExpensesByTags(responseData.data);
            renderPieChart(tagData);
        } else {
            noDataMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error.message);
        noDataMessage.style.display = 'block';
    } finally {
        chartContainer.style.display = 'block';
    }
}

async function loadIncomePieChart() {
    const chartContainer = document.getElementById('incomePieChart');
    const noDataMessage = document.getElementById('noDataMessageIncomes');

    if (!chartContainer || !noDataMessage) {
        console.error('No se encontraron los elementos del gráfico');
        return;
    }

    noDataMessage.style.display = 'none';
    chartContainer.style.display = 'none';

    try {
        const apiURL = 'http://172.16.238.10:5000/transactions/incomes/allincomes';
        const response = await fetch(apiURL, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`Error al cargar los datos: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Datos recibidos:', responseData);

        if (responseData.status === 'success' && Array.isArray(responseData.data) && responseData.data.length > 0) {
            const tagData = groupExpensesByTags(responseData.data);
            renderPieChartincome(tagData);
        } else {
            noDataMessage.style.display = 'block'; 
        }
    } catch (error) {
        console.error('Error:', error.message);
        noDataMessage.style.display = 'block';
    } finally {
        chartContainer.style.display = 'block';
    }
}


function groupExpensesByTags(expenses) {
    const totalsByCategory = {};

    expenses.forEach(({ category, amount }) => {
        totalsByCategory[category] = (totalsByCategory[category] || 0) + parseFloat(amount);
    });

    const totalAmount = Object.values(totalsByCategory).reduce((sum, value) => sum + value, 0);

    return Object.entries(totalsByCategory).map(([category, total]) => ({
        tag: category || "Sin categoría", 
        percentage: ((total / totalAmount) * 100).toFixed(2),
    }));
}


function renderPieChart(data) {
    const ctx = document.getElementById('expensePieChart').getContext('2d');

    if (window.expenseChartInstance instanceof Chart) {
        window.expenseChartInstance.destroy();
    }

    const labels = data.map(item => item.tag);
    const percentages = data.map(item => item.percentage);
    const colors = generateColorPalette(labels.length);

    window.expenseChartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels,
            datasets: [
                {
                    label: 'Distribución de Gastos por Tags',
                    data: percentages,
                    backgroundColor: colors,
                    borderColor: colors.map(color => darkenColor(color, 0.8)),
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
                        label: (context) =>
                            `${context.label}: ${context.raw}%`,
                    },
                },
            },
        },
    });
}

function renderPieChartincome(data) {
    const ctx = document.getElementById('incomePieChart').getContext('2d');

    if (window.expenseChartInstance instanceof Chart) {
        window.expenseChartInstance.destroy();
    }

    const labels = data.map(item => item.tag);
    const percentages = data.map(item => item.percentage);
    const colors = generateColorPalette(labels.length);

    window.expenseChartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels,
            datasets: [
                {
                    label: 'Distribución de Gastos por Tags',
                    data: percentages,
                    backgroundColor: colors,
                    borderColor: colors.map(color => darkenColor(color, 0.8)),
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
                        label: (context) =>
                            `${context.label}: ${context.raw}%`,
                    },
                },
            },
        },
    });
}


function generateColorPalette(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(`hsl(${(i * 360) / count}, 70%, 50%)`);
    }
    return colors;
}

function darkenColor(color, amount) {
    const [h, s, l] = color.match(/\d+/g).map(Number);
    return `hsl(${h}, ${s}%, ${Math.max(0, l - amount * 100)}%)`;
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM completamente cargado');
    
    selectedTimespan = 'day'; 
    document.getElementById('timeSelectButton').innerText = `Periodo seleccionado: ${selectedTimespan}`;
    
    graphData();
    graphIncomes();

    document.getElementById('timeSelectButton').addEventListener('click', toggleMenu);
    document.querySelectorAll('#timeMenu li').forEach((item) => {
        item.addEventListener('click', (e) => {
            const timespan = e.target.dataset.timespan;
            setTimespan(timespan);
        });
    });
    document.getElementById('graphButton').addEventListener('click', graphData);
    document.getElementById('graphIncomesButton').addEventListener('click', graphIncomes);

    loadExpenseChart();
    loadIncomePieChart();
});




document.getElementById('graphButton').addEventListener('click', graphData);
