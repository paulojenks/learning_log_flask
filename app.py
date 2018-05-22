from flask import (Flask, g, render_template, flash, redirect, url_for)

import models
import forms

DEBUG = True
PORT = 5000
HOST = '127.0.0.1'

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'l;joi3;llak;ij;3oij'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    stream = models.Entry.select().limit(100)
    return render_template('index.html', stream=stream)


@app.route('/entries')
def stream():
    template = 'index.html'
    stream = models.Entry.select().limit(100)
    return render_template(template, stream=stream)


@app.route('/entry', methods=["GET", "POST"])
def new():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Entry.create_entry(
            title=form.title.data.strip(),
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned = form.what_i_learned.data.strip(),
            resources_to_remember = form.resources_to_remember.data.strip()
        )
        flash("Entry Posted!", "success")
        return redirect(url_for('index'))
    return render_template('entry.html', form=form)


@app.route('/entries/<int:entry_id>')
def details(entry_id):
    entries = models.Entry.select().where(
        models.Entry.id == entry_id
    )
    return render_template('detail.html', stream=entries)


@app.route('/entries/delete/<int:entry_id>')
def delete_entry(entry_id):
    try:
        models.Entry.get(models.Entry.id == entry_id).delete_instance()
    except models.IntegrityError:
        pass
    flash("Entry Deleted", "success")
    return redirect(url_for('index'))


@app.route('/entries/edit/<int:entry_id>', methods=('GET', 'POST'))
def edit_entry(entry_id):
    edit = models.Entry.select().where(models.Entry.id == entry_id).get()
    form = forms.PostForm(obj=edit)
    form.populate_obj(edit)
    if form.validate_on_submit():
        q = models.Entry.update(
            title=form.title.data.strip(),
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned = form.what_i_learned.data.strip(),
            resources_to_remember = form.resources_to_remember.data.strip()).where(models.Entry.id == entry_id)
        q.execute()
        flash("Entry updated", "success")
        return redirect(url_for('stream'))
    return render_template('entry.html', form=form)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)