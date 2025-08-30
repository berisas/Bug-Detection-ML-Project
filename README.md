BugRiskEvaluatorML is a Streamlit-based machine learning project that predicts the risk of bugs in code commits and provides developer-specific insights to improve software quality.

Features

Bug Risk Prediction
Upload commit history CSVs to train a Random Forest model and predict the likelihood of bugs in new commits.

Suggested Safer Commits
Generate commit combinations to minimize risk under a defined threshold.

Personalized Developer Analysis
Provides human-readable tips for each developer based on historical low-risk commits.
Example:

"Dev1 performs best when changing 10–50 lines of code and modifying 1–3 files; optimal conditions include commit type as 'bug fix' and work in 'core module'."

Experiment Section
Test a new commit interactively and view predicted risk in real time.

Feature Importance
Visualizes which commit features contribute most to bug risk.

Installation Prerequisites

Python 3.8+

pip

Clone Repository
git clone https://github.com/<your-username>/BugDetectorML.git
cd BugDetectorML

Install Dependencies
pip install -r requirements.txt

Running the App
streamlit run bug_detector_app.py


Upload your commit history CSV file and explore predictions, suggested safer commits, and developer insights.

CSV Format

Input CSV should have the following columns:

lines_changed, files_changed, message_length, developer, developer_bug_rate, commit_type, code_area, label


commit_type: 0 = new feature/refactor, 1 = bug fix

code_area: 0 = side module, 1 = core module

label: 0 = no bug, 1 = bug

Generating Synthetic Data

Use the included script to generate synthetic commits:

python generate_synthetic_csv.py


Developer-specific bug rates can be set to simulate realistic behavior.

Notes

Developer-specific safe patterns are derived from historical low-risk commits.

Feature importance shows which metrics contribute most to bug risk.

Risk predictions are probabilities (0–100%).

