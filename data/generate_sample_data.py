"""
SIEM Alert Data Generator
Generates realistic security alerts for triage testing and benchmarking.
Creates both raw alerts and ground truth labels for evaluation.

Author: Neha Purohit
Date: 2024
"""

import json
import random
import csv
from datetime import datetime, timedelta
import uuid

def generate_realistic_alerts(num_alerts=150, seed=42):
    """
    Generate realistic SIEM alerts that mirror real-world SOC data.
    
    Distribution:
    - 15% Critical (actual threats requiring immediate action)
    - 20% High (suspicious activity needing investigation)
    - 30% Medium (anomalous but likely benign)
    - 35% Low (noise, false positives)
    """
    random.seed(seed)
    
    # Define attack patterns with realistic frequencies
    attack_patterns = {
        "brute_force": {
            "event_type": "Brute Force Attempt",
            "severity": "critical",
            "description": "Multiple failed login attempts detected",
            "indicators": ["failed_login_count > 10", "multiple_source_ips", "short_time_window"],
            "frequency": 0.15,
            "is_threat": 0.85  # 85% of these are real threats
        },
        "dns_tunneling": {
            "event_type": "DNS Tunneling Detected",
            "severity": "critical",
            "description": "Unusual DNS query patterns suggesting data exfiltration",
            "indicators": ["long_subdomain_names", "high_query_volume", "txt_record_abuse"],
            "frequency": 0.10,
            "is_threat": 0.90
        },
        "powershell_encoded": {
            "event_type": "Suspicious PowerShell Execution",
            "severity": "high",
            "description": "Encoded or obfuscated PowerShell command detected",
            "indicators": ["base64_encoding", "download_cradle", "bypass_execution_policy"],
            "frequency": 0.20,
            "is_threat": 0.75
        },
        "lateral_movement": {
            "event_type": "Lateral Movement Detected",
            "severity": "high",
            "description": "Unusual internal network connections suggesting lateral movement",
            "indicators": ["smb_admin_share", "remote_psexec", "unusual_internal_rdp"],
            "frequency": 0.10,
            "is_threat": 0.80
        },
        "port_scan": {
            "event_type": "Port Scan Detected",
            "severity": "medium",
            "description": "Sequential port scanning activity detected",
            "indicators": ["sequential_ports", "multiple_destinations", "syn_flood"],
            "frequency": 0.15,
            "is_threat": 0.40
        },
        "failed_login": {
            "event_type": "Failed Login Attempt",
            "severity": "low",
            "description": "Single failed authentication attempt",
            "indicators": ["wrong_password", "account_locked", "expired_credentials"],
            "frequency": 0.25,
            "is_threat": 0.10
        },
        "malware_signature": {
            "event_type": "Malware Signature Detected",
            "severity": "critical",
            "description": "Known malware signature identified in file or process",
            "indicators": ["av_detection", "ioc_match", "behavioral_analysis"],
            "frequency": 0.05,
            "is_threat": 0.95
        }
    }
    
    # Realistic IP ranges
    external_threat_ips = [
        "203.0.113.42", "198.51.100.17", "192.0.2.99", 
        "185.220.101.33", "45.155.205.88"
    ]
    
    internal_ips = [
        "192.168.1.50", "192.168.1.101", "192.168.2.75",
        "10.0.15.23", "10.0.15.88", "172.16.8.99"
    ]
    
    # User accounts with different privilege levels
    users = {
        "jsmith": "standard",
        "mwilson": "standard", 
        "agarcia": "standard",
        "svc_backup": "service_account",
        "svc_sql": "service_account",
        "admin": "privileged",
        "db_admin": "privileged",
        "root": "privileged"
    }
    
    # Hostnames
    hostnames = [
        "WIN-DC01", "WIN-FILE01", "WIN-WEB01", "WIN-APP01",
        "LAPTOP-001", "LAPTOP-042", "SRV-DB01", "SRV-MAIL01"
    ]
    
    alerts = []
    ground_truth = []
    
    base_time = datetime(2024, 4, 12, 8, 0, 0)
    
    print(f"Generating {num_alerts} realistic SIEM alerts...")
    
    for i in range(num_alerts):
        # Select attack type based on frequency weights
        attack_type = random.choices(
            list(attack_patterns.keys()),
            weights=[attack_patterns[p]["frequency"] for p in attack_patterns]
        )[0]
        
        pattern = attack_patterns[attack_type]
        
        # Determine if this is a true threat or false positive
        is_true_positive = random.random() < pattern["is_threat"]
        
        # Select source IP (external for threats, internal for most false positives)
        if is_true_positive and attack_type in ["brute_force", "dns_tunneling", "malware_signature"]:
            source_ip = random.choice(external_threat_ips)
        else:
            source_ip = random.choice(internal_ips)
        
        # Select user and determine risk
        username = random.choice(list(users.keys()))
        user_privilege = users[username]
        
        # Generate alert
        alert = {
            "alert_id": str(uuid.uuid4())[:8],
            "timestamp": (base_time + timedelta(minutes=i*2, seconds=random.randint(0, 59))).isoformat() + "Z",
            "source_ip": source_ip,
            "destination_ip": random.choice(internal_ips),
            "event_type": pattern["event_type"],
            "severity": pattern["severity"],
            "user": username,
            "user_privilege": user_privilege,
            "hostname": random.choice(hostnames),
            "description": pattern["description"],
            "indicators": pattern["indicators"],
            "raw_log": f"Sample log entry for {pattern['event_type']} event at {(base_time + timedelta(minutes=i*2)).strftime('%H:%M:%S')}",
            "event_id": random.randint(1000, 9999)
        }
        
        alerts.append(alert)
        
        # Create ground truth label
        ground_truth.append({
            "alert_id": alert["alert_id"],
            "true_severity": pattern["severity"] if is_true_positive else "low",
            "is_true_positive": is_true_positive,
            "attack_category": attack_type,
            "requires_action": is_true_positive and pattern["severity"] in ["critical", "high"],
            "threat_confidence": round(random.uniform(0.7, 1.0) if is_true_positive else random.uniform(0.1, 0.4), 2),
            "analyst_notes": "Verified threat" if is_true_positive else "False positive - legitimate activity"
        })
    
    return alerts, ground_truth

def save_alerts_to_json(alerts, filename="data/siem_alerts_raw.json"):
    """Save alerts to JSON file"""
    with open(filename, 'w') as f:
        json.dump(alerts, f, indent=2)
    print(f"✓ Saved {len(alerts)} alerts to {filename}")

def save_ground_truth_to_csv(ground_truth, filename="data/ground_truth_labels.csv"):
    """Save ground truth labels to CSV file"""
    if not ground_truth:
        return
    
    fieldnames = list(ground_truth[0].keys())
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ground_truth)
    
    print(f"✓ Saved {len(ground_truth)} ground truth labels to {filename}")

def print_statistics(alerts, ground_truth):
    """Print summary statistics"""
    print("\n" + "="*60)
    print(" DATA GENERATION STATISTICS")
    print("="*60)
    
    # Alert distribution by severity
    severity_counts = {}
    for alert in alerts:
        sev = alert["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    print("\nAlert Distribution by Severity:")
    for sev in ["critical", "high", "medium", "low"]:
        count = severity_counts.get(sev, 0)
        pct = (count / len(alerts)) * 100
        print(f"  {sev.upper():10} {count:3} alerts ({pct:5.1f}%)")
    
    # True positive rate
    true_positives = sum(1 for gt in ground_truth if gt["is_true_positive"])
    print(f"\nTrue Positive Rate: {true_positives}/{len(ground_truth)} ({(true_positives/len(ground_truth))*100:.1f}%)")
    
    # Action required
    action_required = sum(1 for gt in ground_truth if gt["requires_action"])
    print(f"Alerts Requiring Action: {action_required}/{len(ground_truth)} ({(action_required/len(ground_truth))*100:.1f}%)")
    
    # Event type distribution
    event_counts = {}
    for alert in alerts:
        event = alert["event_type"]
        event_counts[event] = event_counts.get(event, 0) + 1
    
    print("\nTop Event Types:")
    for event, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {event:40} {count:3}")
    
    print("="*60)

def main():
    """Main execution function"""
    print(" SIEM Alert Data Generator")
    print("Generating realistic security alerts for SOC triage testing...\n")
    
    # Generate alerts
    alerts, ground_truth = generate_realistic_alerts(num_alerts=150, seed=42)
    
    # Save to files
    save_alerts_to_json(alerts)
    save_ground_truth_to_csv(ground_truth)
    
    # Print statistics
    print_statistics(alerts, ground_truth)
    
    print("\n✅ Data generation complete!")
    print("\nNext steps:")
    print("  1. Review data/siem_alerts_raw.json")
    print("  2. Review data/ground_truth_labels.csv")
    print("  3. Run: python src/ai_triage_engine.py")

if __name__ == "__main__":
    main()
