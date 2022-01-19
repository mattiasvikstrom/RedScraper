"""
Routes and views for the flask application.
"""
from typing_extensions import Required
from flask import Flask, redirect, url_for
from datetime import datetime
from flask import render_template, request, jsonify
from os import environ
from scraper import *
from scraper_comments import *
from analyze import *
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "hey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

load_dotenv()

#database instance. created if not avaliable.
class mainmenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu = db.Column(db.String(20))
    choice = db.Column(db.String(20))
    name = db.Column(db.String(20))

    # def __init__(self, menu, choice, name):
    #     self.menu = menu
    #     self.choice = choice
    #     self.name = name

    def __repr__(self):
        return f"Choice('{self.menu}', '{self.choice}', '{self.name}')"

#database instance. created if not avaliable.
class choicemenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(20))
    sub = db.Column(db.String(20))

    # def __init__(self, choice, sub):
    #     self.choice = choice
    #     self.sub = sub

    def __repr__(self):
        return f"Choice('{self.choice}', '{self.sub}')"

#database instance. created if not avaliable.
class analyzemenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu = db.Column(db.String(20))
    choice = db.Column(db.String(20))
    name = db.Column(db.String(20))

    # def __init__(self, menu, choice, name):
    #     self.menu = menu
    #     self.choice = choice
    #     self.name = name

    def __repr__(self):
        return f"Choice('{self.menu}', '{self.choice}', '{self.name}')"

#reusable Flask form
class Form(FlaskForm):
    scrapemethod = SelectField('Method', choices=[])
    scrapechoice = SelectField('Subreddit', choices=[])

class Analyzeform(FlaskForm):
    scrapemethod = SelectField('Method', choices=[])
    scrapechoice = SelectField('Subreddit', choices=[])
    analyzemethod = SelectField('Analyze', choices=[])
    filechoice = SelectField('files', choices=[])

class Filesform(FlaskForm):
    browsefiles = SelectField('Files',files=[])
        
@app.route('/analyze', methods=['GET', 'Post'])
def analyze():
    form = Analyzeform()
    form.scrapemethod.choices = [(mainmenu.choice, mainmenu.name ) for mainmenu in mainmenu.query.filter_by(menu='analyzemenu').all()]
    form.analyzemethod.choices = [(analyzemenu.choice, analyzemenu.name ) for analyzemenu in analyzemenu.query.filter_by(menu='analyzemenu').all()]
    form.scrapechoice.choices = [(choicemenu.sub) for choicemenu in choicemenu.query.filter_by(choice='').all()]
    if request.method == 'POST':
        choice = request.form["scrapemethod"]
        method = request.form['analyzemethod']
        sub = request.form['scrapechoice']
        file = request.form['filechoice']
        #buttoncheck = request.form['formsubmit']
        if choice is not None:
            if method == 'MM':
                analyzeresults = RedditScraper_analyze()
                results = analyzeresults.analyze_mostmentioned(choice, sub, file)
                return render_template(
                    'analyze.html', form=form,
                    title=(f'Most mentions from {choice} successful'),
                    results = results
                )
            if method == 'SA':
                return redirect(url_for('analyze', title=(f'Sentiment analysis from {choice} successful')))
                # return render_template(
                #     'scrape_test.html', form=form,
                #     title=(f'scraping topics from {choice} successful')
                # )
        else:
            return render_template(
                'analyze.html', form=form,
                title=(f'scraping of {choice} unsuccessful')
            )
    return render_template('analyze.html', form=form, title='Analyze data from reddit')

#In the route, instanciate the Form query for the initial values displayed in second dropdown.
@app.route('/scrape', methods=['GET', 'Post'])
def scrape():
    form = Form()
    form.scrapemethod.choices = [(mainmenu.choice, mainmenu.name ) for mainmenu in mainmenu.query.filter_by(menu='mainmenu').all()]
    form.scrapechoice.choices = [(choicemenu.sub) for choicemenu in choicemenu.query.filter_by(choice='').all()]
    if request.method == 'POST':
        choice = request.form["scrapechoice"]
        method = request.form['scrapemethod']
        #buttoncheck = request.form['formsubmit']
        if choice is not None:
            if method == 'SC':
                scraper_comments = RedditScraper_comments()
                scraper_comments.scrapered(choice)
                return render_template(
                    'scrape.html', form=form,
                    title=(f'scraping comments from {choice} successful')
                )
            if method == 'ST':
                scraper = RedditScraper()
                scraper.scrapered(choice)
                return redirect(url_for('scrape', title=(f'scraping topics from {choice} successful')))
                # return render_template(
                #     'scrape_test.html', form=form,
                #     title=(f'scraping topics from {choice} successful')
                # )
        else:
            return render_template(
                'scrape.html', form=form,
                title=(f'scraping of {choice} unsuccessful')
            )
    return render_template('scrape.html', form=form, title='Select from list below to scrape')

#When new category is selected fetch and return the avaliable choices for second dropdown
@app.route('/sub/<choice>')
def choice(choice):
    choices = choicemenu.query.filter_by(choice=choice).all()
    choiceArray = []

    for choice in choices:
        choiceObj = {}
        choiceObj['sub'] = choice.sub
        choiceArray.append(choiceObj)
    
    return jsonify({'choices' : choiceArray})

@app.route('/choice/<choice>/<method>')
def files(choice, method):
    data_folder = (os.environ.get('pth'))

    #choices = request.form["scrapechoice"] #wallstreetbets ex
    #method = request.form['scrapemethod'] #'ST' ex

    choiceArray = []

    mainmenustring = fetchmainmenustring(method, choice)
    full_path = (f'{data_folder}{mainmenustring}' + '/')

    for file in os.listdir(full_path):
            choiceObj = {}
            filename = os.fsdecode(file)
            if filename.endswith(".csv"): 
                choiceObj['file'] = filename
                choiceArray.append(choiceObj)
            #     continue
            # else:
            #     continue

    return jsonify({'files' : choiceArray})

def fetchmainmenustring(method, choice):
    path = ""
    if(method is not None):
        if(method == 'AT'):
            return (f'{choice}')
        if(method == 'AC'):
            return (f'{choice}' + 'comments')
    return path

@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.html',
        title='Home Page',
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        message='Your contact page.'
    )

@app.route('/scrape2', methods=['GET', 'POST'])
def scrape2():
    if request.method == 'POST':
        choice = request.form.get('scrapedrop')
        if choice is not None:
            scraper = RedditScraper()
            scraper.scrapered(choice)
            return render_template(
                'scrape.html',
                title=(f'scraping of {choice} successful')
            )
        else:
            return render_template(
            'scrape.html',
            title='Nothing happend.'
        )
    return render_template(
    'scrape.html',
        title='Select from list below to scrape'
        )

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, threaded=True)