from flask import Flask,request,jsonify
import json
from task import module_task

app = Flask(__name__)
app.register_blueprint(module_task)

@app.route("/")
def home():
    return "Home"


if __name__ == "__main__":
    app.run(debug=True)
