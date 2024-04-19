# api/teachers/principal.py

from flask import Blueprint, jsonify, request
from ..decorators import principal_required
from ..responses import success_response, error_response
from models.teachers import Teacher

# Create a Blueprint object for the principal API related to teachers
teachers_principal_api = Blueprint('teachers_principal_api', __name__)

# Endpoint to list all teachers
@teachers_principal_api.route('/principal/teachers', methods=['GET'])
@principal_required
def list_teachers():
    try:
        # Query the database to retrieve all teachers
        teachers = Teacher.query.all()
        # Format the response
        teacher_data = [{
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at,
            'updated_at': teacher.updated_at
            # Add other fields as needed
        } for teacher in teachers]
        # Return the response
        return jsonify({'data': teacher_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
