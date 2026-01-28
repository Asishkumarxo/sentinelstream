# Machine Learning Approach Selection

This document explains the choice of machine learning approach
used for fraud detection in SentinelStream.

The goal is to detect anomalous and suspicious transactions
in real time while maintaining low latency and high scalability.

---

## Why Machine Learning is Needed

Rule-based fraud detection alone is not sufficient because:
- Fraud patterns evolve over time
- Not all fraudulent behavior can be predefined as rules
- New users and new fraud types may bypass static thresholds

Machine learning helps detect **unknown and subtle patterns**
that rules may miss.

---

## Supervised vs Unsupervised Learning

### Supervised Learning
- Requires large amounts of labeled fraud data
- Fraud labels are often noisy or unavailable
- Difficult to maintain in real-time systems

### Unsupervised Learning
- Does not require labeled data
- Learns normal transaction behavior
- Flags deviations as anomalies

**Chosen Approach:** ✅ Unsupervised Learning

---

## Why Isolation Forest

Isolation Forest is selected as the anomaly detection model
for the following reasons:

- Efficient on large-scale datasets
- Works well with high-dimensional feature spaces
- Fast inference suitable for real-time systems
- Low memory and computational overhead
- Widely used in fraud and intrusion detection systems

---

## Model Output Interpretation

- The model produces an **anomaly score** for each transaction
- Higher anomaly scores indicate higher deviation from normal behavior
- The score is normalized to a range of **0.0 – 1.0**

This anomaly score is combined with rule-based risk scores
to make the final fraud decision.

---

## Role of ML in the Overall System

- ML does **not directly block** transactions
- ML provides a **risk signal**
- Final decision is made using:
  - Rule-based score
  - ML anomaly score
  - Configurable thresholds
