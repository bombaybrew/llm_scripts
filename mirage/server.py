from flask import Flask, jsonify, send_from_directory, request
import json, time
import os

import llm_simple as llm

app = Flask(__name__, static_folder="static")

# Route for JSON data
@app.route('/data')
def data():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)

# Route to serve the main HTML file
@app.route('/')
def index():
    return send_from_directory("static", "index.html")

# Route to serve the main HTML file
@app.route('/mirage')
def mirage():
    return send_from_directory("static", "mirage.html")

@app.route('/prompt', methods=['POST'])
def prompt():
    form_payload = request.form.to_dict()
    print("Form Payload:",form_payload, request, request.form, request.args, request.values.to_dict())
    llm.generate_code(form_payload.get("user_prompt"))
    
    return "Payload received", 200

# Route to serve pages dynamically
@app.route('/pages/<path:page>')
def serve_page(page):
    return send_from_directory("static/pages", page)

# Route to serve components dynamically
@app.route('/components/<path:component>')
def serve_component(component):
    return send_from_directory("static/components", component)

if __name__ == "__main__":
    app.run(debug=True)
