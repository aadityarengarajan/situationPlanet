import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz, process
import yaml
import json

# Load your dataset (replace with actual file path)
data = pd.read_excel("intelligence/data/incident_history.xlsx")

# Load heuristics from YAML file
with open("intelligence/data/rcaKB.yaml", "r") as yaml_file:
    heuristics_data = yaml.safe_load(yaml_file)
    heuristics = heuristics_data['Incidents']

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X = tfidf_vectorizer.fit_transform(data['description'])

# Encode categorical features
encoder = LabelEncoder()
y = encoder.fit_transform(data['incident_type'])

# Train a Random Forest classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)

# Function to generate root causes
def generate_root_causes(incident_description):
    incident_vector = tfidf_vectorizer.transform([incident_description])
    incident_type_encoded = classifier.predict(incident_vector)[0]
    incident_type = encoder.inverse_transform([incident_type_encoded])[0]
    
    root_causes = []
    for heuristic in heuristics:
        if heuristic['Category'] == incident_type:
            similarity = fuzz.ratio(incident_description, heuristic["Incident"])
            if similarity >=40:
                root_causes.extend(heuristic['Cause'])
    
    return root_causes

def show_yaml(new_incident):
    
    print(yaml.dump(new_incident, indent=2))

def rcaAlgorithm(incident:dict):
    # Test with a sample incident description
    sample_incident_description = incident["incident"]
    category = incident["type"]
    root_causes = generate_root_causes(sample_incident_description)
    final = []
    for i in root_causes:
        for j in i:
            final.append(j)
    return {"Category": category,
            "Cause": final}


def main():
    # Test with a sample incident description
    sample_incident_description = "Application Log4J Error: Critical Logging Failure Detected"
    category = "Application"
    root_causes = generate_root_causes(sample_incident_description)
    new_incident = {
            "Incident": sample_incident_description,
            "Category": category,
            "Cause": root_causes
    }
    final = []
    for i in root_causes:
        for j in i:
            final.append(j)
    print(final)

if __name__ == '__main__':
    main()