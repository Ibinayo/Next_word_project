from flask import Flask, jsonify, request
from flask_cors import CORS
from api.v1.views import app_views
from app import app


app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

