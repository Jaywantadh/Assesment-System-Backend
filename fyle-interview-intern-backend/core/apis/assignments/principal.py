# api/assignments/principal.py

from flask import Blueprint, jsonify, request
from ..decorators import principal_required
from ..responses import success_response, error_response
from models.teachers import Teacher
from models.assignments import Assignment

# Create a Blueprint object for the principal API related to assignments
assignments_principal_api = Blueprint('assignments_principal_api', __name__)

# Endpoint to list all submitted and graded assignments
@assignments_principal_api.route('/principal/assignments', methods=['GET'])
@principal_required
def list_submitted_and_graded_assignments():
    try:
        # Query the database for assignments submitted and graded
        assignments = Assignment.query.filter_by(state='SUBMITTED').filter(Assignment.grade.isnot(None)).all()
        # Format the response
        assignment_data = [{
            'content': assignment.content,
            'created_at': assignment.created_at,
            'grade': assignment.grade,
            'id': assignment.id,
            'state': assignment.state,
            'student_id': assignment.student_id,
            'teacher_id': assignment.teacher_id,
            'updated_at': assignment.updated_at
        } for assignment in assignments]
        # Return the response
        return jsonify(success_response(assignment_data))
    except Exception as e:
        return jsonify(error_response(str(e))), 500
    
# Endpoint to list all teachers
@assignments_principal_api.route('/principal/teachers', methods=['GET'])
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

# Endpoint to grade or re-grade an assignment
@assignments_principal_api.route('/principal/assignments/grade', methods=['POST'])
@principal_required
def grade_assignment():
    try:
        # Parse request data
        data = request.get_json()
        assignment_id = data.get('id')
        grade = data.get('grade')

        # Retrieve the assignment from the database
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify(error_response('Assignment not found')), 404

        # Update the assignment grade
        assignment.grade = grade
        assignment.state = 'GRADED'  # Update assignment state if needed

        # Save changes to the database
        assignment.save()

        # Return success response
        return jsonify(success_response('Assignment graded successfully')), 200
    except Exception as e:
        return jsonify(error_response(str(e))), 500
