from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import *
from . import db

routes = Blueprint(__name__, 'routes')


@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        results = 'Search results for "'+request.form.get('search')+'"'
        notes = Note.query.filter_by(
            user_id=current_user.id, name=request.form.get('search').title()).all()
        return render_template('home.html', user=current_user, results=results, notes=notes)

    results = 'Your Notes'
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', user=current_user, results=results, notes=notes)


@routes.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        name = request.form.get('name').title()
        note = request.form.get('note')

        new_note = Note(name=name, code=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for('website.routes.home'))

    return render_template('new.html', user=current_user)


@routes.route('/<username>/<id>')
def note(username, id):
    note = Note.query.filter_by(id=id, user_id=username).first()
    if note:
        return render_template('note.html', user=current_user, note=note)
