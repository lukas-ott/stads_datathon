import pandas as pd

anomaly_categories = {
    "value_based": {
        "name": "Value-Based Anomalies",
        "explanation": "Anomalies based on unusual transaction amounts",
        "detection_metrics": ["z-score", "IQR method", "threshold analysis"],
    },
    "pattern_based": {
        "name": "Pattern Anomalies",
        "explanation": "Unusual combinations of fields or values that deviate from normal business patterns",
        "detection_metrics": [
            "association rules",
            "frequent pattern mining",
            "co-occurrence matrices",
        ],
    },
    "temporal": {
        "name": "Temporal Anomalies",
        "explanation": "Timing-related irregularities in transaction postings",
        "detection_metrics": [
            "time series analysis",
            "seasonality detection",
            "change point analysis",
        ],
    },
    "process_violations": {
        "name": "Process Violations",
        "explanation": "Transactions that violate standard accounting procedures or workflows",
        "detection_metrics": ["rule-based validation", "process mining", "sequence analysis"],
    },
    "user_system_behavior": {
        "name": "User/System Behavior Anomalies",
        "explanation": "Unusual patterns in how users or systems interact with the accounting system",
        "detection_metrics": ["user profiling", "behavioral analysis", "access pattern mining"],
    },
    "regulatory_compliance": {
        "name": "Regulatory/Compliance Anomalies",
        "explanation": "Transactions that might raise regulatory concerns or compliance issues",
        "detection_metrics": ["compliance rule checking", "regulatory pattern matching"],
    },
    "statistical": {
        "name": "Statistical Anomalies",
        "explanation": "Transactions that violate expected statistical properties of the data",
        "detection_metrics": [
            "Benford analysis",
            "clustering",
            "distribution testing",
            "isolation forest",
        ],
    },
    "business_context": {
        "name": "Business Context Anomalies",
        "explanation": "Transactions that may be technically valid but unusual given the business context",
        "detection_metrics": [
            "domain-specific rules",
            "business process modeling",
            "contextual outlier detection",
        ],
    },
}


def categorize_anomalies(anomaly: pd.DataFrame) -> str:
    """
    Categorize anomalies based on their characteristics and detection metrics
    """
    return NotImplementedError