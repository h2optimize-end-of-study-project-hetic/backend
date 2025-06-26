from flask import request, jsonify, Blueprint

from src.use_cases.version.get_version import GetVersion

version_routes = Blueprint('version_routes', __name__)

def create_version_routes(get_version_use_case: GetVersion) -> Blueprint:
    @version_routes.route('/version', methods=['GET'])
    def get_version():            
      result = get_version_use_case.execute()
      return {"name": result.name, "version": result.version}
    



