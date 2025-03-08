import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
import graphviz
from sklearn.tree import export_graphviz

# Read the dataset
df = pd.read_csv(r"C:\Users\julia\Downloads\datathon_data.csv")
df = df.drop(columns="BELNR")

# List of categorical and numeric columns
categorical_columns = ['WAERS', 'BUKRS', 'KTOSL', 'PRCTR', 'BSCHL', 'HKONT']
numeric_columns = ['DMBTR', 'WRBTR']

count_anomal = df[df['label'] == 'anomal'].shape[0]
count_regular = df[df['label'] == 'regular'].shape[0]

print(f"Number of rows where label = 'anomal': {count_anomal}")
print(f"Number of rows where label = 'regular': {count_regular}")

# Encode categorical columns
label_encoder = LabelEncoder()
for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col])

# Scale numeric columns
scaler = StandardScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Convert target variable
df["label"] = df["label"].apply(lambda x: 1 if x == "anomal" else 0)

# Features (X) and Target (y)
X = df.drop('label', axis=1)
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Upsample minority class
df_train = pd.concat([X_train, y_train], axis=1)
df_train_regular = df_train[df_train['label'] == 0]
df_train_anomal = df_train[df_train['label'] == 1]
df_train_anomal_upsampled = resample(df_train_anomal, replace=True, n_samples=426323, random_state=42)
df_train_upsampled = pd.concat([df_train_regular, df_train_anomal_upsampled]).sample(frac=1, random_state=42)
X_train_upsampled = df_train_upsampled.drop(columns=['label'])
y_train_upsampled = df_train_upsampled['label']

# Define and tune Decision Tree model
param_grid = {
    'max_depth': [3, 4, 5, 6, 7, 8, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2']
}

decision_tree = DecisionTreeClassifier(random_state=42)
grid_search = GridSearchCV(decision_tree, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=2)
grid_search.fit(X_train_upsampled, y_train_upsampled)
best_model = grid_search.best_estimator_
print("Best Model:", best_model)

# Plot decision tree
def plot_decision_tree():
    dot_data = export_graphviz(best_model, out_file=None, feature_names=X.columns,
                               class_names=['Regular', 'Anomal'], filled=True, rounded=True, special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("decision_tree")
    return graph

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

def explain_decision(sample_row):
    # Convert sample row to DataFrame
    sample_df = pd.DataFrame([sample_row], columns=X.columns)

    # Encode categorical columns properly and ensure unseen values are handled
    for col in categorical_columns:
        if sample_df[col].iloc[0] in label_encoder.classes_:  # Avoid unseen values
            sample_df[col] = label_encoder.transform(sample_df[col])
        else:
            sample_df[col] = -1  # Assign a default value (e.g., -1 for unseen categories)

    # Scale numeric columns only for prediction
    sample_df_scaled = sample_df.copy()  # Keep original sample for inverse scaling later
    sample_df[numeric_columns] = scaler.transform(sample_df[numeric_columns])

    # Get prediction
    prediction = best_model.predict(sample_df)[0]

    # Extract decision path for rules and condition explanation
    decision_path = best_model.decision_path(sample_df)
    feature_names = X.columns
    threshold_values = best_model.tree_.threshold
    feature_indices = best_model.tree_.feature

    rules = []
    violated_conditions = {}

    for node_index in decision_path.indices:
        if feature_indices[node_index] != -2:  # Ignore leaf nodes
            feature_name = feature_names[feature_indices[node_index]]
            threshold = threshold_values[node_index]
            feature_value = sample_df.iloc[0, feature_indices[node_index]]

            if feature_value <= threshold:
                rules.append(f"{feature_name} ≤ {threshold:.2f} (value: {feature_value:.2f})")
            else:
                rules.append(f"{feature_name} > {threshold:.2f} (value: {feature_value:.2f})")
                
                if prediction == 1:  # Anomal classification
                    # Handle violated conditions and inverse transform for numeric columns
                    if feature_name in numeric_columns:
                        # Inverse transform for numeric columns
                        original_values = scaler.inverse_transform(sample_df_scaled[numeric_columns].values.reshape(1, -1))
                        original_value = original_values[0][numeric_columns.index(feature_name)]
                        violated_conditions[feature_name] = f"{feature_name} was expected to be ≤ {threshold:.2f} but was {original_value:.2f}"
                    else:
                        # For categorical columns, map back to original value
                        original_value = label_encoder.inverse_transform([int(feature_value)])[0]
                        violated_conditions[feature_name] = f"{feature_name} was expected to be ≤ {threshold:.2f} but was {original_value}"

    # Prepare final explanation
    explanation = "\n".join(rules)
    
    if violated_conditions:
        explanation += "\n\nViolated conditions for 'Anomal':\n"
        explanation += "\n".join([f"{k}: {v}" for k, v in violated_conditions.items()])

    classification = "Anomal" if prediction == 1 else "Regular"

    # Plot the decision tree
    plt.figure(figsize=(15, 10))
    plot_tree(best_model, feature_names=feature_names, filled=True, rounded=True, class_names=["Regular", "Anomal"])
    plt.title("Decision Tree Visualization")
    plt.show()

    return classification, explanation

# Example usage
sample_row = {
    "WAERS": "J41",
    "BUKRS": "H70",
    "KTOSL": "P46",
    "PRCTR": "R91",
    "BSCHL": "L19",
    "HKONT": "Q81",
    "DMBTR": 9.24455E+11,
    "WRBTR": 5.95851E+11
}

classification, explanation = explain_decision(sample_row)
print("Classification:", classification)
print("Explanation:", explanation)