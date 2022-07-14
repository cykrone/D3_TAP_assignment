from datetime import datetime
from core.models import ShortUrls
from core import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for


def generate_short_url(num_of_chars: int):
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_url = generate_short_url(6)

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        new_link = ShortUrls(
            original_url=url, short_url=short_url)
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + short_url

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    link = ShortUrls.query.filter_by(short_url=short_url).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))