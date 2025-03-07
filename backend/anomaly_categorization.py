
# dict containing all rules dedecting anomalies
anomaly_categories = {
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

