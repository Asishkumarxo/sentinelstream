// --- State ---
const state = {
    transactions: [],
    view: 'dashboard', // Initial view after landing
    autoRefresh: true,
    refreshInterval: null,
    showLanding: true
};

// --- API ---
async function fetchTransactions() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/transactions/feed?limit=50');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        state.transactions = data;
        updateUI();
    } catch (error) {
        console.error('Error fetching data:', error);
        // Fallback for demo if API is offline
        if (state.transactions.length === 0) {
            // Optional: Generate dummy data or show error state
            document.getElementById('dashboard-table-body').innerHTML = '<tr><td colspan="5" class="loading-row">System Offline - Check Backend</td></tr>';
        }
    }
}

// --- UI Logic ---
function updateUI() {
    updateStats(state.transactions);

    if (state.view === 'dashboard') {
        renderDashboardTable(state.transactions.slice(0, 10));
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

    const elTotal = document.getElementById('total-txns');
    if (elTotal) {
        animateValue(elTotal, parseInt(elTotal.innerText) || 0, total, 500);
        document.getElementById('flagged-txns').innerText = flagged;
        document.getElementById('rejected-txns').innerText = rejected;
        const rate = total > 0 ? Math.round((approved / total) * 100) : 0;
        document.getElementById('approval-rate').innerText = `${rate}%`;
    }
}

// Polish: Number animation
function animateValue(obj, start, end, duration) {
    if (start === end) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
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
                <td>${txn.user_id || 'user'}</td>
                <td>$${txn.amount}</td>
                <td>${txn.merchant}</td>
                <td class="fraud-score ${scoreClass}">${txn.fraud_score}</td>
                <td>${date}</td>
            </tr>
        `;
    } else {
        return `
            <tr>
                <td><span class="status-badge ${txn.status}">${txn.status}</span></td>
                <td>${txn.transaction_id.substring(0, 8)}...</td>
                <td>${txn.user_id || 'user'}</td>
                <td>$${txn.amount}</td>
                <td class="fraud-score ${scoreClass}">${txn.fraud_score}</td>
            </tr>
        `;
    }
}

function renderDashboardTable(transactions) {
    const tbody = document.getElementById('dashboard-table-body');
    if (!tbody) return;
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="loading-row">No recent transactions</td></tr>';
        return;
    }
    tbody.innerHTML = transactions.map(t => createRow(t, false)).join('');
}

function renderFullTransactionTable(transactions) {
    const tbody = document.getElementById('full-transaction-table-body');
    if (!tbody) return;
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-row">No transactions found</td></tr>';
        return;
    }
    tbody.innerHTML = transactions.map(t => createRow(t, true)).join('');
}

function renderAlertsTable(transactions) {
    const tbody = document.getElementById('alerts-table-body');
    if (!tbody) return;

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-row">No active alerts. System secure.</td></tr>';
        return;
    }

    tbody.innerHTML = transactions.map(t => {
        const scoreClass = t.fraud_score >= 70 ? 'score-high' : 'score-med';
        const severity = t.fraud_score >= 70 ? 'CRITICAL' : 'WARNING';

        return `
            <tr id="alert-${t.transaction_id}">
                <td><span class="status-badge ${t.status}" style="font-weight:900">${severity}</span></td>
                <td>${t.transaction_id.substring(0, 8)}...</td>
                <td>${t.user_id || 'user'}</td>
                <td>$${t.amount}</td>
                <td>${t.merchant}</td>
                <td class="fraud-score ${scoreClass}">${t.fraud_score}</td>
                <td>
                    <button class="btn-refresh" style="font-size:0.8rem; padding: 4px 12px;" onclick="resolveAlert('${t.transaction_id}')">Resolve</button>
                </td>
            </tr>
        `;
    }).join('');
}

function resolveAlert(txId) {
    // Optimistic UI update
    const row = document.getElementById(`alert-${txId}`);
    if (row) {
        row.style.opacity = '0';
        setTimeout(() => row.remove(), 300);
        // In a real app, send API request to resolve
        console.log(`Resolved alert for ${txId}`);

        // Remove from local state to prevent reappearance on next poll (until fetch overrides)
        // Ideally backend would mark it handled.
    }
}

// --- Navigation ---
function switchView(viewName) {
    state.view = viewName;

    // Update Sidebar
    document.querySelectorAll('.sidebar li').forEach(li => li.classList.remove('active'));
    const activeLink = document.querySelector(`.sidebar li[data-view="${viewName}"]`);
    if (activeLink) activeLink.classList.add('active');

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
    const viewEl = document.getElementById(`${viewName}-view`);
    if (viewEl) viewEl.classList.remove('hidden');

    updateUI();
}

// --- Landing Page Logic ---
function enterApp(targetView = 'dashboard') {
    console.log('enterApp called with target:', targetView);
    try {
        const landing = document.getElementById('landing-page');
        const appContainer = document.querySelector('.app-container');

        if (!landing || !appContainer) {
            console.error('Landing or App Container not found!');
            return;
        }

        landing.classList.add('fade-out');

        // Ensure transition effects play out
        setTimeout(() => {
            landing.style.display = 'none';
            appContainer.classList.remove('hidden');
            switchView(targetView);

            // Start polling only after entering app
            fetchTransactions();
            if (state.autoRefresh) {
                state.refreshInterval = setInterval(fetchTransactions, 5000);
            }
        }, 500);
    } catch (e) {
        console.error('Error in enterApp:', e);
    }
}
// Ensure global access
window.enterApp = enterApp;

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
    document.getElementById('refresh-dashboard')?.addEventListener('click', () => {
        const btn = document.getElementById('refresh-dashboard');
        const icon = btn.querySelector('i');
        icon.classList.add('fa-spin');
        fetchTransactions().then(() => setTimeout(() => icon.classList.remove('fa-spin'), 500));
    });

    document.getElementById('refresh-tx')?.addEventListener('click', fetchTransactions);

    // Search Filter
    document.getElementById('search-tx-input')?.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = state.transactions.filter(t =>
            t.transaction_id.toLowerCase().includes(term) ||
            String(t.amount).includes(term) ||
            (t.user_id && t.user_id.toLowerCase().includes(term))
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

    // Initial State is Landing Page (handled by HTML/CSS visibility)
    // We do NOT fetch transactions yet.
});

