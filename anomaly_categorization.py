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
    "BSCHL": {
        "name": "BSCHL ist wrongly assigned",
        "explanation": "Every BSCHL not being A1 to A3 is an anomaly",
        "detection_metrics": [
            "BSCHL is not A1 to A3"
        ]
    },
        "BUKRS": {
        "name": "BUKRS ist wrongly assigned",
        "explanation": "Every BUKRS not starting with C is an anomaly",
        "detection_metrics": [
            "BUKRS does not start with C"
        ]
    },
        "DMBTR": {
        "name": "DMBTR ist is in anomaly interval",
        "explanation": "DMBTR is in one of two intervals with mostly anomalies",
        "detection_metrics": [
            "DMBTR above 90E6",
            "DMBTR between 9106E2 and 9107E2",
        ]
    },
        "PRCTR": {
        "name": "PRCTR ist wrongly assigned",
        "explanation": "Every PRCTR not starting with C is an anomaly",
        "detection_metrics": [
            "PRCTR does not start with C"
        ]
    },
        "KTOSL": {
        "name": "KTOSL ist wrongly assigned",
        "explanation": "Every KTOSL not being C1 to C9 is an anomaly",
        "detection_metrics": [
            "KTOSL does not C1 to C9"
        ]
    },
    "HKONT": {
        "name": "HKONT ist wrongly assigned",
        "explanation": "Every HKONT not being B1 to B3 is an anomaly",
        "detection_metrics": [
            "HKONT is not B1 to B3"
        ]
    },
    "WAERS": {
        "name": "WAERS ist wrongly assigned",
        "explanation": "Every WAERS not being C1 to C9 is an anomaly",
        "detection_metrics": [
            "WAERS is not C1 to C9"
        ]
    },
    "WRBTR": {
        "name": "WRBTR ist is in anomaly interval",
        "explanation": "WRBTR is in one of two intervals with mostly anomalies",
        "detection_metrics": [
            "WRBTR above 5.9E7",
            "WRBTR between 544E2 and 545E2",
        ]
    }
}


def calculate_overall_conditional_probability(detected_sub_anomalies, df):
    # input is a df containing the columns as keys where the value of the data point is suspicious
    # init mask with True and the lenght of the df
    mask = df.index = df.index
    if 'BSCHL' in detected_sub_anomalies.keys():
        mask &= ~df['BSCHL'].isin(["A1", "A2", "A3"])
    if 'BUKRS' in detected_sub_anomalies.keys():
        mask &= ~df['BSCHL'].str.startswith('C')
    if 'DMBTR' in detected_sub_anomalies.keys():
        mask &= (df['DMBTR'] > 90E6) | (9106E2 <= df['DMBTR'] <= 9107E2)
    if 'PRCTR' in detected_sub_anomalies.keys():
        mask &= ~df['PRCTR'].str.startswith('C')        
    if 'KTOSL' in detected_sub_anomalies.keys():
        mask &= ~df['KTOSL'].isin([f"C{i}" for i in range(1, 10)])
    if 'BSCHL' in detected_sub_anomalies.keys():
        mask &= ~df['BSCHL'].isin(["B1", "B2", "B3"])
    if 'WAERS' in detected_sub_anomalies.keys():
        mask &= ~df['WAERS'].isin([f"C{i}" for i in range(1, 10)])
    if 'WRBTR' in detected_sub_anomalies.keys():
        mask &= (df['WRBTR'] > 5.9E7) | (544E2 <= df['DMBTR'] <= 545E2)
    
    return len(df.loc[mask, 'anomal']) / len(df.loc[mask])


def categorize_anomalies(anomaly: pd.DataFrame) -> str:
    """
    Categorize anomalies based on their characteristics and detection metrics
    """
    return NotImplementedError