# 🛡️ SOC Triage Automation: AI vs. Human Performance Study

## 📌 Project Overview Here
Security Operations Centers (SOCs) are drowning in alert fatigue. This project investigates and benchmarks the performance of AI-driven triage against traditional manual triage. We test multiple approaches (Rule-based, Random Forest, XGBoost, and LLM) to find the optimal balance of speed, accuracy, and explainability.

## 📊 Key Results
| Metric | Manual Triage | AI-Assisted (LLM) | Improvement |
|--------|---------------|-------------------|-------------|
| Time (150 alerts) | 11.25 hours | 30 seconds + 5 min review | **~135x faster** |
| Accuracy | 78% | 84% | **+6%** |
| False Negative Rate| 12% | 8% | **-33%** |

## 🚀 Quick Start
```bash
git clone https://github.com/NehaAIML/soc-triage-demo.git
cd soc-triage-demo
pip install -r requirements.txt
python data/generate_sample_data.py
python src/ai_triage_engine.py
