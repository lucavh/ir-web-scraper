from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
from app.cust_functions import rankedSearchTFIDF
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
index_file = os.path.join(SITE_ROOT, "static/collection/indexed", "ii_weights.pickle")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
      flash('Query: {}'.format(form.query.data))

      flash('Results:')

      results = rankedSearchTFIDF(form.query.data, index_file)

      if len(results) == 0:
        flash('Sorry, no results found for this query!')
      else:
        for i in range(len(results)):
          flash('{} \t\t - {}'.format(i+1,results[i][0]))

      return redirect(url_for('index'))

    return render_template('index.html',  title='Search', form=form)

