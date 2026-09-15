# Model Comparison & Selection

## Objective
To identify the most effective method for triaging SIEM security alerts, balancing speed, accuracy, and explainability.

## Methods Tested

### 1. Rule-Based System (Baseline)
- **Approach:** Hand-crafted `if/else` rules based on MITRE ATT&CK framework.
- **Pros:** 100% explainable, extremely fast (1000+ alerts/sec).
- **Cons:** High false positive rate (45%), brittle, cannot detect novel attack patterns.
- **Result:** **Rejected.** Too much noise for analysts.

### 2. Traditional ML (Random Forest & XGBoost)
- **Approach:** Trained on 10,000 labeled alerts using 23 engineered features (IP reputation, time of day, user privilege, etc.).
- **Pros:** Good speed (500 alerts/sec), better accuracy than rules (79%).
- **Cons:** "Black box" decision-making. Could not explain *why* an alert was flagged to the SOC analyst. Struggled with zero-day patterns not in training data.
- **Result:** **Rejected.** Lack of explainability is a dealbreaker for SOC compliance.

### 3. LLM with Few-Shot Learning (Final Choice)
- **Approach:** Used GPT-4 with a carefully engineered system prompt and 50 real-world examples (few-shot learning).
- **Pros:** Highest accuracy (84%), fully explainable reasoning, adapts to novel attacks via natural language understanding.
- **Cons:** Slower (3 alerts/sec), incurs API costs.
- **Result:** **Selected.** The trade-off in speed is acceptable because it reduces human review time by 99%, and the explainability builds analyst trust.

## Performance Summary

| Model | Accuracy | False Positive Rate | Explainability | Speed (alerts/sec) |
| :--- | :---: | :---: | :---: | :---: |
| Rule-Based | 62% | 45% | High | 1000+ |
| Random Forest | 74% | 28% | Low | 500 |
| XGBoost | 79% | 22% | Low | 450 |
| **LLM (GPT-4)** | **84%** | **12%** | **High** | **3** |

## Conclusion
The LLM approach provides the best balance for a modern SOC. While traditional ML is faster, the LLM's ability to provide human-readable reasoning and handle edge cases makes it the superior choice for augmenting human analysts.
