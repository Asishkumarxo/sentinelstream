// --- State ---
const state = {
    transactions: [],
    view: 'dashboard',
    autoRefresh: true,
    refreshInterval: null
};

// --- API ---
async function fetchTransactions() {
    try {
        // Fetch global feed from the new endpoint
        const response = await fetch('http://localhost:8000/api/v1/transactions/feed?limit=50');
        const data = await response.json();

        // Data is now a list, not { transactions: [...] }
        state.transactions = data;
        updateUI();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// --- UI Logic ---
function updateUI() {
    // 1. Update Stats (Always needed for Dashboard view)
    updateStats(state.transactions);

    // 2. Render active view content
    if (state.view === 'dashboard') {
        renderDashboardTable(state.transactions.slice(0, 10)); // Show last 10
    } else if (state.view === 'transactions') {
        renderFullTransactionTable(state.transactions);
    } else if (state.view === 'alerts') {
        const alerts = state.transactions.filter(t => t.fraud_score >= 40);
        renderAlertsTable(alerts);
    }
}

function updateStats(transactions) {
    const total = transactions.length;
    const flagged = transactions.filter(t => t.status === 'flagged').length;
    const rejected = transactions.filter(t => t.status === 'rejected').length;
    const approved = transactions.filter(t => t.status === 'approved').length;

    // Check if elements exist (in case we are not on dashboard view, but stats are global? No, stats are in dashboard view)
    // Actually, stats are only in dashboard view HTML. So we check existence.
    const elTotal = document.getElementById('total-txns');
    if (elTotal) {
        elTotal.innerText = total;
        document.getElementById('flagged-txns').innerText = flagged;
        document.getElementById('rejected-txns').innerText = rejected;
        const rate = total > 0 ? Math.round((approved / total) * 100) : 0;
        document.getElementById('approval-rate').innerText = `${rate}%`;
    }
}

// Helper to create rows
function createRow(txn, fullDetails = false) {
    const scoreClass = txn.fraud_score >= 70 ? 'score-high' : (txn.fraud_score >= 40 ? 'score-med' : 'score-low');
    const date = new Date(txn.timestamp).toLocaleString();

    if (fullDetails) {
        return `
            <tr>
                <td><span class="status-badge ${txn.status}">${txn.status}</span></td>
                <td>${txn.transaction_id.substring(0, 8)}...</td>
                <td>test1</td>
                <td>$${txn.amount}</td>
                <td>${txn.merchant}</td>
                <td class="fraud-score ${scoreClass}">${txn.fraud_score}</td>
                <td>${date}</td>
            </tr>
        `;
    } else {
        // Dashboard mini row
        return `
            <tr>
                <td><span class="status-badge ${txn.status}">${txn.status}</span></td>
                <td>${txn.transaction_id.substring(0, 8)}...</td>
                <td>test1</td>
                <td>$${txn.amount}</td>
                <td class="fraud-score ${scoreClass}">${txn.fraud_score}</td>
            </tr>
        `;
    }
}

function renderDashboardTable(transactions) {
    const tbody = document.getElementById('dashboard-table-body');
    if (!tbody) return;
    tbody.innerHTML = transactions.map(t => createRow(t, false)).join('');
}

function renderFullTransactionTable(transactions) {
    const tbody = document.getElementById('full-transaction-table-body');
    if (!tbody) return;
    tbody.innerHTML = transactions.map(t => createRow(t, true)).join('');
}

function renderAlertsTable(transactions) {
    const tbody = document.getElementById('alerts-table-body');
    if (!tbody) return;

    tbody.innerHTML = transactions.map(t => {
        const scoreClass = t.fraud_score >= 70 ? 'score-high' : 'score-med';
        const severity = t.fraud_score >= 70 ? 'CRITICAL' : 'WARNING';

        return `
            <tr>
                <td><span class="status-badge ${t.status}" style="font-weight:900">${severity}</span></td>
                <td>${t.transaction_id.substring(0, 8)}...</td>
                <td>test1</td>
                <td>$${t.amount}</td>
                <td>${t.merchant}</td>
                <td class="fraud-score ${scoreClass}">${t.fraud_score}</td>
                <td>
                    <button style="padding:4px 8px; cursor:pointer;" onclick="alert('Action taken on ${t.transaction_id}')">Resolve</button>
                </td>
            </tr>
        `;
    }).join('');
}

// --- Navigation ---
function switchView(viewName) {
    state.view = viewName;

    // Update Sidebar
    document.querySelectorAll('.sidebar li').forEach(li => li.classList.remove('active'));
    document.querySelector(`.sidebar li[data-view="${viewName}"]`).classList.add('active');

    // Update Header Title
    const titles = {
        'dashboard': 'Dashboard',
        'transactions': 'Transaction History',
        'alerts': 'Fraud Alerts',
        'settings': 'Settings'
    };
    document.getElementById('page-title').innerText = titles[viewName];

    // Show/Hide Sections
    document.querySelectorAll('.view-section').forEach(el => el.classList.add('hidden'));
    document.getElementById(`${viewName}-view`).classList.remove('hidden');

    updateUI();
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    // Add data-view attributes to sidebar links
    const sidebarItems = document.querySelectorAll('.sidebar nav li');
    const views = ['dashboard', 'transactions', 'alerts', 'settings'];

    sidebarItems.forEach((li, index) => {
        const view = views[index];
        li.setAttribute('data-view', view);
        li.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            switchView(view);
        });
    });

    // Refresh Buttons
    document.getElementById('refresh-dashboard')?.addEventListener('click', fetchTransactions);
    document.getElementById('refresh-tx')?.addEventListener('click', fetchTransactions);

    // Search Filter (Simple Client Side)
    document.getElementById('search-tx-input')?.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = state.transactions.filter(t =>
            t.transaction_id.toLowerCase().includes(term) ||
            String(t.amount).includes(term)
        );
        renderFullTransactionTable(filtered);
    });

    // Toggle Auto Refresh
    document.getElementById('auto-refresh-toggle')?.addEventListener('change', (e) => {
        state.autoRefresh = e.target.checked;
        if (state.autoRefresh) {
            state.refreshInterval = setInterval(fetchTransactions, 5000);
        } else {
            clearInterval(state.refreshInterval);
        }
    });

    // Start
    fetchTransactions();
    state.refreshInterval = setInterval(fetchTransactions, 5000);
});
