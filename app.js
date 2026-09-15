/*
 * SOC Triage Demo - Interactive Dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("🚀 SOC Triage Dashboard Loaded");
    updateMetrics();
});

function updateMetrics() {
    // Update metric cards
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
    console.log("📊 Metrics updated");
}
