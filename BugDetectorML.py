import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import itertools

# Title
st.title("Bug-Aware Commit Advisor")

# Upload commits.csv
uploaded = st.file_uploader("Upload commits.csv", type="csv")

if uploaded:
    # Read data
    data = pd.read_csv(uploaded)
    st.write("### Sample Data", data.head())

    # Features and labels
    X = data.drop("label", axis=1)
    y = data["label"]

    feature_names = X.columns.tolist()  # Get all feature names

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train RandomForest model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    st.write("### Model Accuracy", clf.score(X_test, y_test))

    # Dynamically create inputs for all features
    st.write("### Try a new commit")
    user_input = {}
    for feature in feature_names:
        # Make a slider for numeric features
        min_val = int(X[feature].min())
        max_val = int(X[feature].max())
        default_val = int(X[feature].median())
        user_input[feature] = st.slider(feature, min_val, max_val, default_val)

    # Predict risk for original commit
    input_values = [user_input[f] for f in feature_names]
    original_risk = clf.predict_proba([input_values])[0][1]
    st.write(f"Original commit risk: {original_risk:.2%}")

    # Generate safer commit suggestions (<20% risk)
    st.write("### Suggested safer commits (<20% risk)")

    # For simplicity, only vary numeric features slightly
    variation_options = []
    for feature in feature_names:
        val = user_input[feature]
        variation_options.append([max(int(X[feature].min()), val - 1), val, min(int(X[feature].max()), val + 1)])

    # Generate all combinations
    suggestions = []
    for combo in itertools.product(*variation_options):
        risk = clf.predict_proba([list(combo)])[0][1]
        if risk <= 0.20:
            suggestions.append(list(combo) + [risk])

    # Display suggestions
    if suggestions:
        suggestions_df = pd.DataFrame(suggestions, columns=feature_names + ["Predicted Risk"])
        st.dataframe(suggestions_df.style.format({"Predicted Risk": "{:.2%}"}))
    else:B
    st.write("No safe commit suggestions found with <20% predicted risk.")
