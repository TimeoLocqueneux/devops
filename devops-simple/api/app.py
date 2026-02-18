from flask import Flask, jsonify
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route("/welcome")
def index():
    return jsonify({"message": "Bienvenue sur l'API", "version": VERSION, "status": "running"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": VERSION}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
