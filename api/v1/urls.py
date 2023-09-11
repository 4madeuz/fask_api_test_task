from flask import request

from ...app import app
from .controllers import list_of_all_notes, create_note, update_note, retrive_note, delete_note
from flask_jwt_extended import jwt_required


@app.route("/notes", methods=['GET', 'POST'])
def list_create_accounts():
    if request.method == 'GET':
        return list_of_all_notes()
    if request.method == 'POST':
        return create_note()
    return 'Method is Not Allowed'


@app.route("/notes/<note_id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def retrieve_update_destroy_accounts(account_id):
    if request.method == 'GET':
        return retrive_note(account_id)
    if request.method == 'PUT':
        return update_note(account_id)
    if request.method == 'DELETE':
        return delete_note(account_id)
    return 'Method is Not Allowed'
