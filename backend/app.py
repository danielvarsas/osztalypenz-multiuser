from flask import Flask
from api.classes import classes_bp
from api.children import children_bp
from api.transactions import transactions_bp
from api.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = 'key123'  # Change this to something secure

CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(classes_bp, url_prefix='/api')
app.register_blueprint(children_bp, url_prefix='/api')
app.register_blueprint(transactions_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the auth blueprint


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
