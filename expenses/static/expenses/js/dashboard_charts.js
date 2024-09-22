function renderDashboardCharts(incomeData, expenseData, dates, balances) {
    const ctxIncome = document.getElementById('incomeChart').getContext('2d');
    const ctxExpense = document.getElementById('expenseChart').getContext('2d');
    const ctxBalance = document.getElementById('balanceChart').getContext('2d');

    const incomeLabels = incomeData.map(entry => entry.source);
    const incomeValues = incomeData.map(entry => entry.total);

    const expenseLabels = expenseData.map(entry => entry.category);
    const expenseValues = expenseData.map(entry => entry.total);

    const incomeChart = new Chart(ctxIncome, {
        type: 'pie',
        data: {
            labels: incomeLabels,
            datasets: [{
                data: incomeValues,
                backgroundColor: ['#4CAF50', '#FF9800', '#F44336', '#2196F3', '#9C27B0', '#FFC107'],
            }]
        }
    });

    const expenseChart = new Chart(ctxExpense, {
        type: 'pie',
        data: {
            labels: expenseLabels,
            datasets: [{
                data: expenseValues,
                backgroundColor: ['#FF5722', '#03A9F4', '#4CAF50', '#FFC107', '#9C27B0', '#F44336'],
            }]
        }
    });

    const balanceChart = new Chart(ctxBalance, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Balance',
                data: balances,
                borderColor: '#4CAF50',
                fill: false,
                lineTension: 0,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                    },
                },
            },
        }
    });
}
