import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Step 1: Data Preparation
def data_preparation(file_path):
    data = pd.read_excel(file_path)
    
    data['description'].fillna('', inplace=True)
    
    X = data['description']
    y = data['incident_type']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

# Step 2: Incident Classification
def train_classification_model(X_train, y_train):
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train_tfidf, y_train)
    
    return classifier, tfidf_vectorizer

def save_models(classifier, vectorizer, model_path, vectorizer_path):
    joblib.dump(classifier, model_path)
    joblib.dump(vectorizer, vectorizer_path)

def predict_category(feature, train:bool = False):

    if train:

        data_file = "intelligence/data/incident_history.xlsx"
        model_output_path = "intelligence/models/incident_classifier_model.pkl"
        vectorizer_output_path = "intelligence/models/tfidf_vectorizer.pkl"

        X_train, X_test, y_train, y_test = data_preparation(data_file)

        trained_classifier, trained_vectorizer = train_classification_model(X_train, y_train)

        save_models(trained_classifier, trained_vectorizer, model_output_path, vectorizer_output_path)

    # Load the trained classifier model
    model_path = "intelligence/models/incident_classifier_model.pkl"
    loaded_classifier = joblib.load(model_path)

    # Load the trained TF-IDF vectorizer
    vectorizer_path = "intelligence/models/tfidf_vectorizer.pkl"
    loaded_tfidf_vectorizer = joblib.load(vectorizer_path)

    # Feature extraction using the loaded TF-IDF vectorizer
    new_tfidf_vector = loaded_tfidf_vectorizer.transform([feature])

    # Perform prediction
    predicted_incident_type = loaded_classifier.predict(new_tfidf_vector)

    return predicted_incident_type

def save_prediction(type, incident):
    # Load the Excel sheet into a DataFrame
    excel_file = 'intelligence/data/incident_history.xlsx'
    sheet_name = 'Sheet1'
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Create a dictionary for the new row
    new_row = {
        'incident_type': type,
        'description': incident,
    }

    # Append the new row to the DataFrame
    new_row_df = pd.DataFrame([new_row])

    # Concatenate the new row DataFrame with the existing DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)

    # Write the DataFrame back to the Excel sheet
    with pd.ExcelWriter(excel_file, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def predictAlgorithm(incident:str):
    prediction = predict_category(incident, train=True)
    return {"incident": incident,
            "type": prediction[0]}


def main():

    test_case = "Application Log4J Error: Critical Logging Failure Detected"


    prediction = predict_category(test_case)
    print(prediction)
    while input("Validate Prediction (Y/N): ").strip() in "nN":
        if input("Enter Category Manually? (Y/N): ").strip() in "yY":
            print('''Categories:
1. FTR
2. Essbase
3. Database
4. Application
5. Server Outage
6. Database Performance Degradation
7. Network Connectivity Issues
8. Application Performance Drop
9. Data Import Failure
10. Security''')
            predno = 11
            while predno not in range(1,11):
                predno = int(input("Enter Category #:"))
            categories = [
            "FTR",
            "Essbase",
            "Database",
            "Application",
            "Server Outage",
            "Database Performance Degradation",
            "Network Connectivity Issues",
            "Application Performance Drop",
            "Data Import Failure",
            "Security"
            ]
            predicton = [categories[predno-1]]
            break
        else:
            prediction = predict_category(test_case, train=True)
            print(prediction)
    save_prediction(prediction[0], test_case)

if __name__ == '__main__':
    main()