import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
df = pd.read_csv("Ransomware_Data.csv")

print("================================")
print("DATASET LOADED")
print("================================")
print("Shape:", df.shape)

# Separate features and target
X = df.drop("Ware Type", axis=1)

y = df["Ware Type"].map({
    "good": 0,
    "ransom": 1
})

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

# Train
print("\nTraining Random Forest...")
model.fit(X_train, y_train)

print("Training completed!")

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print("MODEL RESULTS")
print("================================")

print("\nAccuracy:", accuracy)
print("Accuracy (%):", round(accuracy * 100, 2), "%")

# Classification report
print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Benign", "Ransomware"]
    )
)

# Confusion matrix
print("Confusion Matrix:")

print(confusion_matrix(y_test, y_pred))