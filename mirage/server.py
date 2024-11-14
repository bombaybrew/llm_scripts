from flask import Flask, jsonify, send_from_directory, render_template
import json
import os

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
