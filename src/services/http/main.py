from flask_cors import CORS
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.interfaces import VersionRepository
from src.use_cases.version import GetVersion
from src.services.http.api.routes.version import create_version_routes

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db.init_app(app)

    ConnectionResetError(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    versionRepository =  VersionRepository(db)
    get_version_use_cases = GetVersion()
    
    version_routes = create_version_routes(get_version_use_cases)
    app.register_blueprint(version_routes, url_prefix='/api')


    @app.route('/')
    def hello():
        return "hello", 200

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'message': str(error), 'content': '', 'error': str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': str(error), 'content': '', 'error': str(error)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)



