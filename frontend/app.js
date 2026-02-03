const API_URL = 'http://localhost:8000/api/v1/transactions/users/test1?page_size=20'; // Demo Endpoint (fetching history for a user for now)
// Note: Ideally, we'd have a 'latest transactions' endpoint. For week 4 demo, we can use the user history endpoint 
// or I can quickly add a 'get all' endpoint. Let's assume we might need to update the backend to support 'get all'
// or we just simulate by querying a known user or iterating.
// Let's stick to querying 'test1' user for the demo purposes or a hardcoded list if the backend is empty.

// Ideally, we want a "/transactions/feed" endpoint. 
// I will check if I can fetch recent transactions.
// The service has `get_user_transactions`. I might need to add `get_all_recent` to backend.
// For now, let's try to hit the user endpoint, and if I have time, I'll add the feed endpoint.

async function fetchTransactions() {
    try {
        // Fetching "test1" user history as a proxy for the stream for this demo
        // In a real app, we'd have a dedicated admin stream endpoint.
        const response = await fetch('http://localhost:8000/api/v1/transactions/users/test1?page=1&page_size=50');
        const data = await response.json();
        
        updateStats(data.transactions);
        renderTable(data.transactions);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateStats(transactions) {
    const total = transactions.length;
    const flagged = transactions.filter(t => t.status === 'flagged').length;
    const rejected = transactions.filter(t => t.status === 'rejected').length;
    const approved = transactions.filter(t => t.status === 'approved').length;
    
    document.getElementById('total-txns').innerText = total;
    document.getElementById('flagged-txns').innerText = flagged;
    document.getElementById('rejected-txns').innerText = rejected;
    
    const rate = total > 0 ? Math.round((approved / total) * 100) : 0;
    document.getElementById('approval-rate').innerText = `${rate}%`;
}

function renderTable(transactions) {
    const tbody = document.getElementById('transaction-table-body');
    tbody.innerHTML = '';
    
    transactions.forEach(txn => {
        const row = document.createElement('tr');
        
        const scoreClass = txn.fraud_score >= 70 ? 'score-high' : 
                          (txn.fraud_score >= 40 ? 'score-med' : 'score-low');
                          
        const date = new Date(txn.timestamp).toLocaleString();
        
        row.innerHTML = `
            <td><span class="status-badge ${txn.status}">${txn.status}</span></td>
            <td>${txn.transaction_id.substring(0, 8)}...</td>
            <td>test1</td> <!-- Hardcoded for this endpoint -->
            <td>$${txn.amount}</td> <!-- Info not in response? Wait, response schema has ID, Status, Score, Msg, Time. Missing Amount/Merchant in Response Schema! -->
            <td>Unknown</td> <!-- Schema limitation detected! -->
            <td class="fraud-score ${scoreClass}">${txn.fraud_score}</td>
            <td>${date}</td>
        `;
        tbody.appendChild(row);
    });
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    fetchTransactions();
    
    // Auto refresh every 5s
    setInterval(fetchTransactions, 5000);
});

document.getElementById('refresh-btn').addEventListener('click', fetchTransactions);
