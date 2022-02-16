"""
Routes and views for the flask application.
"""
from flask import Flask, redirect, url_for, g, render_template, request, jsonify
import os
from scraper import *
from scraper_comments import *
from sentiment import *
from analyze import *
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import time

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

    def __repr__(self):
        return f"Choice('{self.menu}', '{self.choice}', '{self.name}')"

#database instance. created if not avaliable.
class choicemenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(20))
    sub = db.Column(db.String(20))

    def __repr__(self):
        return f"Choice('{self.choice}', '{self.sub}')"

#database instance. created if not avaliable.
class analyzemenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu = db.Column(db.String(20))
    choice = db.Column(db.String(20))
    name = db.Column(db.String(20))

    def __repr__(self):
        return f"Choice('{self.menu}', '{self.choice}', '{self.name}')"

#Flask form for scraping
class Form(FlaskForm):
    scrapemethod = SelectField('Method', choices=[])
    scrapechoice = SelectField('Subreddit', choices=[])
#Flask form for analyzing
class Analyzeform(FlaskForm):
    scrapemethod = SelectField('Method', choices=[])
    scrapechoice = SelectField('Subreddit', choices=[])
    analyzemethod = SelectField('Analyze', choices=[])
    filechoice = SelectField('files', choices=[])
#Flask form for file selection
class Filesform(FlaskForm):
    browsefiles = SelectField('Files',files=[])

@app.route('/analyze', methods=['GET', 'Post'])
def analyze():
    form = Analyzeform() #initialize flask form
    #query database for available menu options
    form.scrapemethod.choices = [(mainmenu.choice, mainmenu.name ) for mainmenu in mainmenu.query.filter_by(menu='analyzemenu').all()]
    form.analyzemethod.choices = [(analyzemenu.choice, analyzemenu.name ) for analyzemenu in analyzemenu.query.filter_by(menu='analyzemenu').all()]
    form.scrapechoice.choices = [(choicemenu.sub) for choicemenu in choicemenu.query.filter_by(choice='').all()]
    sub, file = "",""
    if request.method == 'POST':
        choice = request.form["scrapemethod"] #requests value from scrapemethod dropdown
        method = request.form['analyzemethod'] 
        try:
            sub = request.form['scrapechoice']
            file = request.form['filechoice']
        except:
            print(type(sub))
        #if strings are not empty
        if choice and sub and file:
            if method == 'MM': #mostmentioned
                g.start = time.time() #start timer for measurement of execution
                analyzeresults = RedditScraper_analyze() #instantiate class
                results = analyzeresults.analyze_mostmentioned(choice, sub, file) #call most mentioned method
                returntime = time.time() - g.start # calculate execution time
                returntime = "{:.2f}".format(returntime) #format time to 0,00 decimals
                #prepare lists for value append
                d = []
                v = []
                #iterate results from analyze to visualize in chartjs
                for i in results:
                    d.append(results[i])
                    v.append(i)
                return render_template(
                    'analyze.html', form=form,
                    title=(f'Most mentions from {choice} successful'),
                    results = results, values = v, datavalues = d, returntime = (f'in {str(returntime)} seconds')
                )
            if method == 'SA':
                g.start = time.time() #start timer for measurement of execution
                analyzeresults = RedditScraper_analyzer() #instantiate class
                results = analyzeresults.sentiment(choice, sub, file) #call sentiment method
                returntime = time.time() - g.start # calculate execution time
                returntime = "{:.2f}".format(returntime) #format time to 0,00 decimals
                #create the plot and save, fetch and link to it in the return to analyze page.
                img = BytesIO() #instanciate in memory buffer
                results.plot(kind = 'bar') #plot a bar type grapf
                plt.savefig(img, format='png') #save graph plot as png 
                plt.close() #close
                img.seek(0) #locate image 
                plot_url = base64.b64encode(img.getvalue()).decode('utf8') #create plot url to be displayed as results
                
                return render_template(
                    'analyze.html', form=form,
                    title=(f'Sentiment analysis from {choice} successful'),
                    res = results, plot_url=plot_url, rt = (f'in {str(returntime)} seconds')
                )
        else:
            return render_template(
                'analyze.html', form=form,
                title=(f'analyze unsuccessful, make sure all choices are selected')
            )
    return render_template('analyze.html', form=form, title='Analyze data from reddit')

#In the route, instanciate the Form query for the initial values displayed in second dropdown.
#When a POST is triggered it routes to its correct method for scraping.
@app.route('/scrape', methods=['GET', 'Post'])
def scrape():
    form = Form() #instanciate scrape form
    method, choice = "", ""
    #query database for dropdown options
    form.scrapemethod.choices = [(mainmenu.choice, mainmenu.name ) for mainmenu in mainmenu.query.filter_by(menu='mainmenu').all()]
    form.scrapechoice.choices = [(choicemenu.sub) for choicemenu in choicemenu.query.filter_by(choice='').all()]
    if request.method == 'POST':
        try:
            method = request.form['scrapemethod'] #request value from dropdown
            choice = request.form['scrapechoice']
        except:
            print('error')
        #buttoncheck = request.form['formsubmit']
        if choice and method:
            g.start = time.time() #start timer for measurement of execution
            if method == 'SC':
                scraper_comments = RedditScraper_comments() # instansiate class
                scraper_comments.scrapered(choice) # call scraper method
                returntime = time.time() - g.start #calculate execution time
                returntime = "{:.2f}".format(returntime) #format time to 0,00 decimals
                return render_template(
                    'scrape.html', form=form,
                    title=(f'scraping comments from {choice} successful'), returntime = returntime
                )
            if method == 'ST':
                scraper = RedditScraper() # instansiate class
                scraper.scrapered(choice) # call scraper method
                returntime = time.time() - g.start #calculate execution time
                returntime = "{:.2f}".format(returntime) #format time to 0,00 decimals
                return redirect(url_for('scrape', title=(f'scraping topics from {choice} successful'), returntime = returntime))

        else:
            return render_template(
                'scrape.html', form=form,
                title=(f'scraping unsuccessful, make sure all choices are selected ')
            )
    return render_template('scrape.html', form=form, title='Select from list below to scrape')

#When new category is selected fetch and return the avaliable choices for second dropdown
@app.route('/sub/<choice>')
def choice(choice): #input refers to method choice
    choices = choicemenu.query.filter_by(choice=choice).all() #query all results for choicemenu with marching method choice
    choiceArray = []

    for choice in choices:
        choiceObj = {}
        choiceObj['sub'] = choice.sub
        choiceArray.append(choiceObj)
    
    return jsonify({'choices' : choiceArray})

@app.route('/choice/<choice>/<method>')
def files(choice, method):
    data_folder = (os.environ.get('pth')) #get folderpath
    choiceArray = [] #instanciate return array
    mainmenustring = fetchmainmenustring(method, choice) #fetch the correct folder string
    full_path = (f'{data_folder}{mainmenustring}' + '/') #complete the path string
    #itterate over all avaliable files in that path
    for file in os.listdir(full_path):
            choiceObj = {}
            filename = os.fsdecode(file)
            if filename.endswith(".csv"): #as of now only .csv files are of interest
                choiceObj['file'] = filename
                choiceArray.append(choiceObj) #append files to the array

    return jsonify({'files' : choiceArray})

#complete full path
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, threaded=True)