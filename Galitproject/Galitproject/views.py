"""
Routes and views for the flask application.
"""



from Galitproject import app

from Galitproject.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request, flash

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from Galitproject.models.QueryFormStructure import QueryFormStructure 
from Galitproject.models.QueryFormStructure import LoginFormStructure 
from Galitproject.models.QueryFormStructure import UserRegistrationFormStructure 
from Galitproject.models.QueryFormStructure import olimform 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

db_Functions = create_LocalDatabaseServiceRoutines() 

#home page
#מידע על העולים 
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
#contact page
#המידע עלי 
@app.route('/contact')
def contact():
    
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='my contact page.'
    )
#data base page
#מידע על המאגר מידע שלי ומכיל את קישור לעמוד של המאגר
@app.route('/data')
def data():
    """Renders the contact page."""
    return render_template(
        'data.html',
        title='data',
        year=datetime.now().year,
        message='my data page.'
    )
#abut page
#בעמוד זה המשתמשים יוכלו לקרוא על הכלים הטכנולוגיים שהשתמשתי כדי לכתוב את האתר
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='about page.'
    )

#query page
#גרף של השננים שהמשתמש בוחר
@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    
    form1 = olimform()
    chart = ''
     
   
    df = pd.read_excel( path.join(path.dirname(__file__), 'static\\data\\olim4.xlsx'),encoding = "utf-8")
    x=df["Year"].tolist()
    year_choices=list(zip(x,x))
   
    form1.years.choices = year_choices 


    if request.method == 'POST':
        year_list = form1.years.data
        
        df=df.drop('olim',1 )
        df=df.set_index('Year')
        df.index=df.index.astype(str)
        df=df.loc[year_list]
        df=df.transpose()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        df.plot(kind='bar',ax=ax)
        chart = plot_to_img(fig)

    
    return render_template(
        'Query.html',
        form1 = form1,
        chart = chart
    )
#register page
#כדי להירשם
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        ) 


# Login page
# כדי להתחבר

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash ('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

#מכיל את מאגר המידע ונמצא בתוך העמוד של ההסבר על מאגר
@app.route('/olim')
def olim():
    
    df = pd.read_excel( path.join(path.dirname(__file__), 'static\\data\\olim4.xlsx'),encoding = "utf-8")
    raw_data_table = df.to_html(classes = 'table table-hover')
   
    """Renders the contact page."""
    return render_template(
        'olim.html',
      
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'

    )

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
