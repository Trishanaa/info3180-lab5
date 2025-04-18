"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from app import app
from flask import render_template, Flask, jsonify, send_file, send_from_directory
import os
from app.forms import MovieForm
from app.models import db, Movie
from flask_wtf.csrf import generate_csrf
from .models import Movie



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():

        upload_folder = 'C:\\Users\\kaydeen\\Documents\\info3180\\info3180-lab5\\uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)


        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        filename = secure_filename(poster.filename)
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        poster.save(poster_path)

        movie = Movie(
            title=title,
            description=description,
            poster=filename,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": movie.title,
            "poster": movie.poster,
            "description": movie.description

        }), 201
    return jsonify({"errors": form_errors(form)}), 400

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_list.append({
          'id': movie.id,
          'title': movie.title,
          'description': movie.description,
          'poster': f'/api/v1/posters/{movie.poster}' 
        })
    return jsonify({'movies': movie_list})

@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404