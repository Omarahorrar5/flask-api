from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200
    
    @app.get("/api/greet/<name>")
    def greet(name):
        return jsonify(message=f"Hello, {name}!"), 200
    
    return app

app = create_app()

#run app: flask --app app.main run --debug
# gunicorn -b 0.0.0.0:8000 app.main:app
#tests: python -m pytest -v