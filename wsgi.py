from app import app
import flask_cors

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    flask_cors.CORS(app)
