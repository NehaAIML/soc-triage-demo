"""
AI Triage Engine
Processes raw SIEM alerts using different methodologies (Rule-based, ML, LLM).
Outputs enriched alerts for human review and frontend visualization.

Author: Neha Purohit
"""

import json
import os
import time
import random
from datetime import datetime

class TriageEngine:
    def __init__(self, method='llm'):
        """
        Initialize the engine. 
        method can be 'rule', 'ml', or 'llm'
        """
        self.method = method
        self.results = []
        
    def load_alerts(self, filepath):
        """Load raw alerts from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)

    def rule_based_triage(self, alert):
        """Simple keyword matching (Baseline approach)"""
        score = 0
        if alert['severity'] == 'critical': score += 40
        if alert['user_privilege'] == 'privileged': score += 30
        if 'brute' in alert['event_type'].lower() or 'malware' in alert['event_type'].lower(): 
            score += 30
            
        return self._format_result(alert, score, "Rule-Based")

    def ml_simulated_triage(self, alert):
        """Simulates a Random Forest / XGBoost prediction"""
        # In a real production environment, this would load a .pkl model
        # Here we simulate the model's logic with weighted randomness
        base_score = 50 if alert['severity'] in ['critical', 'high'] else 20
        noise = random.randint(-10, 15) 
        score = min(100, max(0, base_score + noise))
        
        return self._format_result(alert, score, "ML-Simulated")

    def llm_simulated_triage(self, alert):
        """Simulates an LLM (GPT-4) reasoning process"""
        # Simulates the LLM's superior context awareness and few-shot learning
        score = 0
        if alert['severity'] == 'critical': score += 50
        if alert['user_privilege'] == 'privileged': score += 20
        
        # LLM recognizes external threat IPs better than basic rules
        if alert['source_ip'].startswith('203.') or alert['source_ip'].startswith('185.'): 
            score += 30 
            
        reasoning = "High confidence due to external IP and privileged account usage." if score > 70 else "Standard activity, requires manual review."
        
        return self._format_result(alert, score, "LLM-Simulated", reasoning)

    def _format_result(self, alert, score, method, reasoning=""):
        """Standardize the output format"""
        priority = "LOW"
        if score >= 80: priority = "CRITICAL"
        elif score >= 60: priority = "HIGH"
        elif score >= 40: priority = "MEDIUM"

        return {
            "alert_id": alert['alert_id'],
            "original_severity": alert['severity'],
            "ai_priority": priority,
            "risk_score": score,
            "method": method,
            "reasoning": reasoning,
            "timestamp_processed": datetime.now().isoformat()
        }

    def run_batch(self, alerts):
        """Process a batch of alerts and measure performance"""
        print(f"Starting {self.method} triage on {len(alerts)} alerts...")
        start_time = time.time()
        
        for alert in alerts:
            if self.method == 'rule':
                res = self.rule_based_triage(alert)
            elif self.method == 'ml':
                res = self.ml_simulated_triage(alert)
            elif self.method == 'llm':
                res = self.llm_simulated_triage(alert)
            self.results.append(res)
            
        duration = time.time() - start_time
        print(f"Completed in {duration:.4f} seconds.")
        return self.results, duration

def main():
    # Dynamically find paths so it works anywhere
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'siem_alerts_raw.json')
    output_file = os.path.join(base_dir, 'demo', 'triage_results.json')
    
    # Initialize and run
    engine = TriageEngine(method='llm')
    alerts = engine.load_alerts(input_file)
    results, duration = engine.run_batch(alerts)
    
    # Save results for the frontend demo
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump({"processing_time": duration, "results": results}, f, indent=2)
        
    print(f"✅ Results saved to {output_file}")

if __name__ == "__main__":
    main()
