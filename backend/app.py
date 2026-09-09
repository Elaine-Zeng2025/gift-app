from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端跨端口调用后端

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong", "status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)