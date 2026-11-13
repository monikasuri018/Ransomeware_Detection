import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("Ransomware_Data.csv")

# Separate features and target
X = df.drop("Ware Type", axis=1)
y = df["Ware Type"]

# Create held-out test set
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Combine test features and labels
test_data = X_test.copy()
test_data["Ware Type"] = y_test.values

# Select 20 benign + 20 ransomware samples
benign = test_data[test_data["Ware Type"] == "good"].head(20)
ransomware = test_data[test_data["Ware Type"] == "ransom"].head(20)

demo_data = pd.concat(
    [benign, ransomware],
    ignore_index=True
)

# Shuffle
demo_data = demo_data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Remove target because the app performs its own prediction
demo_data = demo_data.drop(
    columns=["Ware Type"]
)

# Save
demo_data.to_csv(
    "unseen_test_samples.csv",
    index=False
)

print("================================")
print("Unseen test dataset created!")
print("================================")
print("Samples:", len(demo_data))
print("Saved as: unseen_test_samples.csv")