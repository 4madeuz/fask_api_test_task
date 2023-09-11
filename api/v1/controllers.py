from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
import uuid

from ... import db
from .models import Note


def list_of_all_notes():
    notes = Note.query.all()
    response = []
    for note in notes:
        response.append(note.toDict())
    return jsonify(response)


def create_note():
    request_form = request.form.to_dict()
    id = str(uuid.uuid4())
    user = get_jwt_identity()
    new_note = Note(
        id=id,
        title=request_form['title'],
        description=request_form['description'],
        author=user.id,
    )
    db.session.add(new_note)
    db.session.commit()
    response = Note.query.get(id).toDict()
    return jsonify(response)


def retrive_note(note_id):
    response = Note.query.get(note_id).toDict()
    return jsonify(response)


def update_note(note_id):
    request_form = request.form.to_dict()
    note = Note.query.get(note_id)
    user = get_jwt_identity()
    if user.id != note.author:
        return jsonify("Wrong username or password"), 401
    note.title = request_form['title']
    note.description = request_form['description']
    response = Note.query.get(note_id).toDict()
    return jsonify(response)


def delete_note(note_id):
    note = Note.query.get(note_id)
    user = get_jwt_identity()
    if user.id != note.author:
        return jsonify("Wrong username or password"), 401
    note.delete()
    db.session.commit()
    return ('Account with Id "{}" deleted successfully!').format(note_id)
