from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load JSON data
with open('data.json') as json_file:
    data = json.load(json_file)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
