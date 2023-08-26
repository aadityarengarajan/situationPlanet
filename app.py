from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from intelligence.agents.incident_classifier import predictAlgorithm
from intelligence.agents.root_cause_analyser import rcaAlgorithm
from intelligence.agents.resolution_algorithm import resolveAlgorithm
from flask_cors import CORS
import zipfile, os, json

app = Flask(__name__)
CORS(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.PROPAGATE_EXCEPTIONS = True


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resolve_incident', methods=['POST', 'GET'])
def resolute():
    req = dict(request.json).get("data")

    forRCA = predictAlgorithm(req)
    forResolution = rcaAlgorithm(forRCA)
    forFinal = resolveAlgorithm(forResolution)

    return {"Causes and Resolutions": forFinal, "Category": forRCA}

@app.route('/kbase')
def viewKbase():
    directory = 'intelligence/data'
    excluded_keyword = 'bak'
    zip_filename = 'knowledge_base.zip'

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                if excluded_keyword not in file:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory))

    return send_file(zip_filename, as_attachment=True)

@app.route('/update_rcaKB', methods=['POST'])
def learnToKB():
    print(dict(request.json))
    cause = dict(request.json).get("data").get("cause")
    resolution = dict(request.json).get("data").get("resolution")
    print(resolution)
    with open("intelligence/data/resolutionKB.json") as f:
        resKB = json.load(f)
    resKB["algorithms"][cause] = resolution.split("\n")
    with open("intelligence/data/resolutionKB.json", "w") as f:
        resKB = json.dump(resKB, f, indent=4)
    
    return {"json": dict(request.json), "form": dict(request.form)}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def main():

    app.run(host='0.0.0.0',debug=True)

if __name__ == '__main__':
    main()