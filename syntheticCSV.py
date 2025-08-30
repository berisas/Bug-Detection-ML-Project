import pandas as pd
import numpy as np
import random

# Parameters
num_commits = 200
developers = ["dev1", "dev2", "dev3", "dev4", "dev5"]
commit_types = [0, 1]  # 0 = new code, 1 = bug fix
code_areas = [0, 1]    # 0 = low-risk area, 1 = core/high-risk area

# Fixed developer bug rates
developer_bug_rates = {
    "dev1": 0.05,
    "dev2": 0.10,
    "dev3": 0.08,
    "dev4": 0.03,
    "dev5": 0.12
}

data = []

for _ in range(num_commits):
    lines_changed = np.random.randint(1, 200)
    files_changed = np.random.randint(1, 10)
    message_length = np.random.randint(10, 300)
    developer = random.choice(developers)
    commit_type = random.choice(commit_types)
    code_area = random.choice(code_areas)
    
    developer_bug_rate = min(developer_bug_rates[developer], 0.4)

    risk_score = developer_bug_rate
    risk_score += 0.0002 * lines_changed
    risk_score += 0.001 * files_changed
    risk_score += 0.01 * code_area
    risk_score += 0.005 * (commit_type == 0)

    # Add small noise for randomness
    risk_score += np.random.uniform(-0.01, 0.01)

    # Clamp risk to reasonable range 
    risk_score = np.clip(risk_score, 0, 0.4)

    label = 1 if np.random.rand() < risk_score else 0

    data.append([
        lines_changed, files_changed, message_length,
        developer, developer_bug_rate, commit_type, code_area, label
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "lines_changed", "files_changed", "message_length", 
    "developer", "developer_bug_rate", "commit_type", "code_area", "label"
])

# Save CSV
df.to_csv("synthetic_commits_low_risk.csv", index=False)
print("Synthetic commits CSV created: synthetic_commits_low_risk.csv")
