async function renderChart() {
    const response = await fetch('http://localhost:5000/api/transactions/summary');
    const data = await response.json();

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.tag),      
            datasets: [{
                label: 'Total por Categoría',
                data: data.map(item => item.total),  
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', renderChart);
