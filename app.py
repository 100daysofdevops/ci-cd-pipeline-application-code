from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "this is coming from v1"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)