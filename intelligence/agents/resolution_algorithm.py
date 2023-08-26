from fuzzywuzzy import fuzz, process
import json
import pandas as pd

# Load incident description and resolution data from an XLSX file
incident_data = pd.read_excel("intelligence/data/incident_resolution_data.xlsx")
incident_data = incident_data.drop(columns = "Type")
incident_resolution_pairs = incident_data.to_dict("records")

with open("intelligence/data/resolutionKB.json") as json_file:
    kb = json.load(json_file)
    knowledge_base = kb["calculators"]
    incident_res = kb["algorithms"]

for incident, resoln in incident_res.items():
    incident_resolution_pairs.append({"Issue":incident, "Resolution":"\n".join(resoln)})

def calculate_risk(root_cause, sim = 40):

    maxsim = 0

    closest_match = None

    for i in knowledge_base.keys():
            similarity = fuzz.ratio(root_cause, i)
            if (similarity >= sim) and (similarity >maxsim):
                maxsim = similarity
                closest_match = i

    if closest_match:
        severity = knowledge_base[closest_match]["severity"]
        probability = knowledge_base[closest_match]["probability"]
        exposure = knowledge_base[closest_match]["exposure"]
        risk = severity * probability * exposure * 100
        return risk
    
    # Return a default risk value if no close match is found
    return 0.0

def resolve_incident(incident, algorithms):
    root_causes = incident["Cause"]
    sorted_root_causes = sorted(root_causes, key=calculate_risk, reverse=True)
    
    resolutions = []
    for root_cause in sorted_root_causes:
        resolution_steps = algorithms.get(root_cause)
        if resolution_steps != []:
            resolutions.append({
                "cause": root_cause,
                "risk": max([calculate_risk(root_cause), calculate_risk(resolution_steps, sim=15)]),
                "resolution": resolution_steps
            })
        else:
            resolutions.append({
                "cause": root_cause,
                "resolution": "No Available Resolution."
            })
    
    return resolutions

def generate_algorithm(incident_resolution_pairs):
    myAlgorithms = {}
    for pair in incident_resolution_pairs:
        incident_description = pair["Issue"]
        resolution_steps = pair["Resolution"]

        for i in incident_res.keys():
            similarity = fuzz.ratio(incident_description, i)
            if similarity >=75:
                myAlgorithms[i] = resolution_steps

    return myAlgorithms

def resolveAlgorithm(incident):
    generated_algorithms = generate_algorithm(incident_resolution_pairs)
    # Resolve the incident
    resolutions = resolve_incident(incident, generated_algorithms)
    return resolutions

def main():
    # Generate the algorithm from incident-resolution pairs
    generated_algorithms = generate_algorithm(incident_resolution_pairs)

    # Sample input
    incident = {
        "Category": "Application Performance Drop",
        "Cause": [
              "Network Connection Failure",
              "Missing Required Libraries",
              "Incorrect log level configuration",
              "Disk Space Exhaustion",
              "Incompatible Log4J library version",
              "Conflicts with other logging frameworks",
              "Log4J library bugs",
              "Interactions with specific code paths"
            ]
    }

    # Resolve the incident
    resolutions = resolve_incident(incident, generated_algorithms)
    for resolution in resolutions:
        print("Cause:", resolution["cause"],"\nRisk:", resolution["risk"], "%")
        print("Resolution Steps:")
        print(resolution['resolution'])
        print("\n")

if __name__ == '__main__':
    main()