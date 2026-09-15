# Experiment Log: The Journey to the Final Model

## Experiment 1: The Rule-Based Baseline (Week 1)
- **Hypothesis:** Simple rules will catch 80% of threats.
- **What I did:** Wrote 47 regex rules for known bad IPs and event types.
- **Result:** Accuracy was only 62%. 
- **Failure Analysis:** It flagged the CEO's travel login as "Critical" because it was from a new country. Rules lack context.
- **Lesson:** Rules are too rigid for modern SOCs.

## Experiment 2: Random Forest ML (Week 2)
- **Hypothesis:** Machine learning will find hidden patterns.
- **What I did:** Engineered 23 features (time of day, IP geolocation, etc.) and trained a Random Forest model.
- **Result:** Accuracy improved to 74%, but the False Positive Rate was still 28%.
- **Failure Analysis:** The model couldn't distinguish between a sysadmin doing their job and an attacker moving laterally. It was a "black box"—I couldn't tell the SOC manager *why* it flagged something.
- **Lesson:** Accuracy isn't enough; explainability is required for analyst trust.

## Experiment 3: LLM Few-Shot Prompting (Week 3 - Final)
- **Hypothesis:** An LLM can understand the nuance of security logs like a human.
- **What I did:** Fed GPT-4 a system prompt acting as a Tier 3 Analyst, along with 50 examples of good vs. bad alerts.
- **Result:** Accuracy hit 84%. Crucially, it provided a text explanation for *every* decision.
- **Optimization:** I lowered the "temperature" setting to 0.1 to make the AI less creative and more deterministic/consistent.
- **Conclusion:** This is the production-ready approach.

## Next Steps / Future Work
- Fine-tune an open-source model (like Llama-3) to reduce API costs.
- Implement a feedback loop where analyst corrections automatically update the few-shot examples.
