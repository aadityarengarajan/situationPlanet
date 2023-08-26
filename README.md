# SituationPlanet Incident Management System Documentation

The **SituationPlanet** system employs three intelligent agents to enhance incident management: the **Incident Classifier**, **Root Cause Analyzer**, and **Resolution Algorithmizer**.

## User Interface: `app.py`

The user interface of the system is implemented in `app.py` and utilizes the Flask framework for web application development.

## WatchDog/SelfHeal: `watchdog.py`

Given log files are auto-monitored in `watchdog.py` to raise alerts on-time.

## Incident Classifier

### Performance Measure

- **Accuracy**: Measures how accurately incidents are categorized.
- **Speed of Classification**: Measures how quickly incidents are categorized.

### Environment

- **Incoming Incident Descriptions**: Textual descriptions of incoming incidents.
- **Historical Incident Data**: Previously categorized incident data.

### Actuators

- **Categorization Labels**: Labels assigned to incidents indicating their category.

### Sensors

- **Incident Descriptions**: Textual descriptions of incidents to be categorized.
- **Historical Incident Data**: Previously categorized incident data used for training and comparison.

### Function

1. Analyzes incident descriptions using Natural Language Processing (NLP) techniques.
2. Matches incidents to predefined categories using machine learning.
3. Provides accurate and rapid incident categorization.
4. Utilizes RandomForest from scikit-learn and TfidfVectorizer for feature extraction.

## Root Cause Analyzer

### Performance Measure

- **Accuracy**: Measures the accuracy of identifying the root causes of incidents.
- **Speed of Analysis**: Measures how quickly root causes are identified.

### Environment

- **Incident Data**: Data about the incidents, including their descriptions and categories.
- **System Logs**: Logs containing relevant information about the system's behavior.
- **Historical Incident Data**: Past incident data for historical context.

### Actuators

- **Identified Root Causes**: Output that identifies the underlying causes of incidents.

### Sensors

- **Incident Data**: Information about incidents, including descriptions and categorizations.
- **System Logs**: Log data for analysis.
- **Historical Incident Data**: Past incident data for reference and analysis.

### Function

1. Analyzes incident details and relevant logs to understand the context.
2. Identifies the root causes and contributing factors behind incidents.
3. Aims to prevent incident recurrence by addressing underlying issues.
4. Utilizes RandomForest from scikit-learn and TfidfVectorizer for analyzing textual data.

## Resolution Algorithmizer

### Performance Measure

- **Effectiveness of Resolution Suggestions**: Measures how effective the suggested resolution strategies are.
- **Relevance to Incident**: Measures how relevant the suggested strategies are to the specific incident.

### Environment

- **Incident Data**: Data about incidents, including descriptions and categories.
- **Resolution Techniques Knowledge Base**: Information about various resolution strategies.

### Actuators

- **Suggested Resolution Strategies**: Output that suggests strategies for resolving incidents.

### Sensors

- **Incident Data**: Information about incidents, including descriptions and categorizations.
- **Resolution Techniques Knowledge Base**: Repository of resolution strategies.

### Function

1. Examines the incident category and details to understand the context.
2. Matches incidents to appropriate resolution techniques based on historical data.
3. Provides a range of strategies for incident resolution.
4. Utilizes RandomForest from scikit-learn, TfidfVectorizer for feature extraction, and fuzzywuzzy for string matching.
