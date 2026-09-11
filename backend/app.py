from flask import Flask, jsonify
from flask_cors import CORS
from models import db   # 从 models.py 导入刚才创建的 db

app = Flask(__name__)
CORS(app)

# 告诉 app 数据库文件叫 gift.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gift.db"
db.init_app(app)   # 把 db 正式绑定到这个 app 上

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong", "status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)