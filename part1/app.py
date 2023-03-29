from flask import Flask, request, jsonify, render_template
from client import Client

app = Flask(__name__)
client = Client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.json["message"]
    response = client.send_message(message)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
