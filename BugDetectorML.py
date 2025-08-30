import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import itertools
import matplotlib.pyplot as plt

# --- Title ---
st.title("Developer Analysis | Bug Rate")

# --- Upload Data ---
uploaded = st.file_uploader("Upload commit history data (CSV format)", type="csv")

if uploaded:
    data = pd.read_csv(uploaded)
    st.write("### Sample Data")
    st.dataframe(data.head())

    # --- Features and Labels ---
    X = data.drop("label", axis=1)
    y = data["label"]
    categorical_cols = ["developer", "commit_type", "code_area"]
    numeric_cols = [col for col in X.columns if col not in categorical_cols]

    X_encoded = pd.get_dummies(X, columns=categorical_cols)

    # --- Train/Test Split & Model ---
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(X_train, y_train)
    st.write("### Model Accuracy")
    st.write(f"{clf.score(X_test, y_test):.2%}")

    # --- Feature Importance ---
    st.write("### Feature Importance")
    feat_importances = pd.Series(clf.feature_importances_, index=X_encoded.columns)
    st.bar_chart(feat_importances.sort_values(ascending=False))

    # --- Suggested Safer Commits ---
    st.write("### Suggested Safer Commits")
    user_input = {col: int(X[col].median()) for col in numeric_cols}
    user_input.update({col: X[col].mode()[0] for col in categorical_cols})

    variation_options = []
    for col in numeric_cols:
        val = user_input[col]
        min_val = max(int(X[col].min()), int(val * 0.5))
        variation_options.append([min_val, val] if min_val != val else [val])

    numeric_combos = list(itertools.product(*variation_options))
    categorical_combos = list(itertools.product(*[X[col].unique() for col in categorical_cols]))

    suggestions = []
    for num_combo in numeric_combos:
        for cat_combo in categorical_combos:
            combo_dict = {col: val for col, val in zip(numeric_cols, num_combo)}
            combo_dict.update({col: val for col, val in zip(categorical_cols, cat_combo)})

            combo_encoded = pd.get_dummies(pd.DataFrame([combo_dict]))
            combo_encoded = combo_encoded.reindex(columns=X_encoded.columns, fill_value=0)

            proba = clf.predict_proba(combo_encoded)[0]
            idx = list(clf.classes_).index(1) if len(proba) > 1 else 0
            risk = proba[idx] if len(proba) > 1 else float(clf.classes_[0] == 1)

            if risk <= 0.40:
                suggestions.append(list(num_combo) + list(cat_combo) + [risk])

    if suggestions:
        col_names = numeric_cols + categorical_cols + ["Predicted Risk"]
        st.dataframe(pd.DataFrame(suggestions, columns=col_names).style.format({"Predicted Risk": "{:.2%}"}))
    else:
        st.write("No safe commit suggestions found under 40% predicted risk.")

    # --- Developer-specific Safe Patterns ---
    st.write("### Developer-specific Safe Patterns")
    commit_type_map = {0: "new feature/refactor", 1: "bug fix"}
    code_area_map = {0: "side module", 1: "core module"}

    for dev in data["developer"].unique():
        low_risk = data[(data["developer"] == dev) & (data["label"] == 0)]
        if low_risk.empty:
            continue

        tip_parts = []
        for col in numeric_cols:
            q25, q75 = int(low_risk[col].quantile(0.25)), int(low_risk[col].quantile(0.75))
            if col == "lines_changed":
                tip_parts.append(f"changing between {q25}-{q75} lines of code")
            elif col == "files_changed":
                tip_parts.append(f"modifying {q25}-{q75} files")
            elif col == "message_length":
                tip_parts.append(f"writing commit messages of {q25}-{q75} words")

        cat_parts = []
        for col, mapping in [("commit_type", commit_type_map), ("code_area", code_area_map)]:
            mode_val = low_risk[col].mode()[0]
            cat_parts.append(f"{col.replace('_',' ').title()} as '{mapping[mode_val]}'")

        st.write(f"**{dev}** performs best when {', '.join(tip_parts)}; optimal conditions include {', '.join(cat_parts)}.")

    # --- Experiment Section ---
    with st.expander("Experiment: Try a New Commit"):
        for col in numeric_cols:
            min_val, max_val = int(X[col].min()), int(X[col].max())
            default_val = user_input[col]
            user_input[col] = st.slider(col, min_val, max_val, default_val) if min_val != max_val else min_val

        for col in categorical_cols:
            options = X[col].unique()
            default_idx = list(options).index(user_input[col])
            user_input[col] = st.selectbox(col, options=options, index=default_idx)

        input_encoded = pd.get_dummies(pd.DataFrame([user_input]))
        input_encoded = input_encoded.reindex(columns=X_encoded.columns, fill_value=0)

        proba = clf.predict_proba(input_encoded)[0]
        idx = list(clf.classes_).index(1) if len(proba) > 1 else 0
        user_risk = proba[idx] if len(proba) > 1 else float(clf.classes_[0] == 1)
        st.write(f"Predicted risk: {user_risk:.2%}")

        top_features = feat_importances[numeric_cols].sort_values(ascending=False).head(3)
        st.write("Top numeric features contributing to risk:")
        st.write(top_features)
