from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for home page...")
    return (
        f"Welcome to the Hawaiian Weather API <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

if __name__ == "__main__":
    app.run(debug=True)