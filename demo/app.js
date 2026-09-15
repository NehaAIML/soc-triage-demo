/*
 * SOC Triage Demo - Interactive Dashboard
 * Loads triage results and displays comparison metrics
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("🚀 SOC Triage Dashboard Loaded");
    loadTriageResults();
    updateMetrics();
});

function loadTriageResults() {
    // In a real deployment, this would fetch from the JSON file
    // For GitHub Pages demo, we'll use embedded sample data
    
    const sampleData = {
        "processing_time": 2.45,
        "total_alerts": 150,
        "summary": {
            "critical_count": 23,
            "high_count": 31,
            "medium_count": 45,
            "low_count": 51
        }
    };
    
    displayAlerts(sampleData);
    updateStats(sampleData);
}

function displayAlerts(data) {
    const alertList = document.getElementById('alertList');
    if (!alertList) return;
    
    // Sample alerts for demo
    const alerts = [
        { id: "a1b2c3d4", type: "Brute Force Attempt", severity: "critical", ai_priority: "CRITICAL", score: 95 },
        { id: "e5f6g7h8", type: "Failed Login", severity: "low", ai_priority: "LOW", score: 15 },
        { id: "i9j0k1l2", type: "DNS Tunneling", severity: "critical", ai_priority: "CRITICAL", score: 92 },
        { id: "m3n4o5p6", type: "PowerShell Execution", severity: "high", ai_priority: "HIGH", score: 78 },
        { id: "q7r8s9t0", type: "Port Scan", severity: "medium", ai_priority: "MEDIUM", score: 45 }
    ];
    
    alertList.innerHTML = alerts.map(alert => `
        <div class="alert-item">
            <div>
                <strong>${alert.type}</strong><br>
                <small class="text-muted">ID: ${alert.id}</small>
            </div>
            <div>
                <span class="badge badge-${alert.ai_priority.toLowerCase()}">${alert.ai_priority}</span>
                <span class="metric-value text-blue">${alert.score}</span>
            </div>
        </div>
    `).join('');
}

function updateStats() {
    // Update metric cards if they exist
    const elements = {
        'totalAlerts': '150',
        'processingTime': '2.45s',
        'accuracy': '84%',
        'speedup': '134x'
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }
}

function updateMetrics() {
    // Simulate real-time metric updates
    console.log("📊 Metrics updated");
}

// Export for use in other scripts
window.SOCDashboard = {
    loadTriageResults,
    displayAlerts,
    updateMetrics
};
