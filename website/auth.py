from flask import Blueprint,session,render_template,url_for,redirect,request,flash
from .models import Voice
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sqlite3
import traceback
import pyttsx3
import os
import time
import re
import json
import random
import threading

global command
global texts
ac=0
global a
a=[]
command ='s'

def lo():
	voice=Voice.query.with_entities(Voice.question)
	return voice

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def rands():
	ranum = random.randint(1000, 9999)
	strin = str(ranum)
	return strin
def talk(text):
	engine = pyttsx3.init()
	voice = engine.getProperty('voices')
	engine.setProperty('voice',voice[1].id)
	engine.say(text)
	engine.runAndWait()

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password,password):
				flash('Logged in successfull', category='success')
				login_user(user,remember=True)
				log = logstat.query.filter(logstat.user_id==current_user.id).first()
				log.status = 1
				db.session.commit()
				return redirect(url_for('views.home'))
			else:
				flash('incorrect password.',category='error')
		else:
			flash('Email does not exist.', category='error')
	return render_template('login.html',user=current_user)


@auth.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
	log = logstat.query.filter(logstat.user_id==current_user.id).first()
	log.status = 0
	db.session.commit()
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/useredit',methods=['GET','POST'])
@login_required
def user_edit():

	return render_template('useredit.html',user=current_user)

@auth.route('/sigup',methods=['GET','POST'])
def sigin_up():
	if request.method=='POST':
		
		types = request.form.get('types')
		
		email=request.form.get('email')
		
		firstname=request.form.get('firstname')
	
		lastname=request.form.get('lastname')
		
		password1=request.form.get('password1')
		
		password2=request.form.get('password2')
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email alredy.',category='error')
		elif len(email) < 4:
			flash('Email is To Short',category='error')

		elif len(firstname) < 2:
			flash('Firstname is To Short',category='error')

		elif len(lastname) < 2:
			flash('Lastname is To Short',category='error')

		elif len(password1) < 7:
			flash('Password is To Short',category='error')

		elif password2 != password1:
			flash('Password Mis-Matched',category='error')

		else:
			global message
			global new_user
			new_user = User(email=email,types=types, firstname=firstname,lastname=lastname,password=generate_password_hash(password1,method='sha256'))
			r_mail = email
			session['email']=r_mail
			session['lastname']=lastname
			session['firstname']=firstname
			session['password']=generate_password_hash(password1,method='sha256')
			message = str(Mail.send(r_mail))
			return render_template('verify.html')
	
	return render_template('sigup.html',user=current_user)

@auth.route('/verify',methods=['GET','POST'])
def verify():
	global message
	global new_user
	emails=session['email']
	lastname=session['lastname']
	firstname=session['firstname']
	password=session['password']
	if request.method=='POST':
		if message == str(request.form.get('otp')):
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user,remember=True)
			lol=User.query.count()
			kl=User.query.all()
			new_logstat = logstat(status=1,user_id=kl[lol-1].id)
			db.session.add(new_logstat)
			db.session.commit()
			messages = MIMEMultipart()
			text = """<html><head><style>h1{{color:blue;}}
			p{{font-size:14px;}}</style></head><body>
			Welcome! Hello{lastname}{firstname}
			<h1>successfull Registered with COES</h1>
			<p>your Login details:<br>Email:{emails}
			<br>password:{password}</p></body>
			</html>""".format(emails=emails,lastname=lastname,firstname=firstname,password=password)
			part = MIMEText(text, 'html')
			messages.attach(part)
			message_str = messages.as_string()
			if is_valid_email(emails):
				Mail.sending(emails,message_str)
			else:
				flash('It is User name not to send result',category='warning')
			flash('Account created!',category='success.')
			return redirect(url_for('views.home'))
		else:
			flash('Otp is incorrect!',category='failure.')
			return redirect(url_for('auth.verify'))
	else:
		return render_template('verify.html')

@auth.route('/about')
def about():
	return render_template('about.html',user=current_user)

@auth.route('/policy')
def policy():
	return render_template('Privacy.html',user=current_user)

@auth.route('/help')
def helps():
	return render_template('help.html',user=current_user)

@auth.route('/contact')
def contact():
	return render_template('contact.html',user=current_user)

@auth.route('/tests')
@login_required
def test():

	return render_template('tests.html',user=current_user)

@auth.route('/custom', methods =['POST','GET'])
@login_required
def custom():
	return render_template('custom.html',user=current_user)

@auth.route('/result')
@login_required
def result():	
	Mcq=Result.query.filter(Result.types=='mcq',Result.user_id==current_user.id).all()
	Mcqlen=len(Mcq)
	total_list = [item.total for item in Mcq]
	marks_list = [item.marks for item in Mcq]
	name_list=[item.name for item in Mcq]
	
	Voice=Result.query.filter(Result.types=='voice',Result.user_id==current_user.id).all()
	Voicelen=len(Voice)
	total_list_Vo=[item.total for item in Voice]
	marks_list_Vo=[item.marks for item in Voice]
	name_list_Vo=[item.name for item in Voice]
	
	Fill=Result.query.filter(Result.types=='fill',Result.user_id==current_user.id).all()
	Filllen = len(Fill)
	total_list_fill=[item.total for item in Fill]
	marks_list_fill=[item.marks for item in Fill]
	name_list_fill=[item.name for item in Fill]
	return render_template('result.html',nlv=name_list_Vo,mlv=marks_list_Vo,tlv=total_list_Vo,Mlv=Voicelen,mlf=marks_list_fill,nlf=name_list_fill,tlf=total_list_fill,Mlf=Filllen,user=current_user,Ml=Mcqlen,tl=total_list,ml=marks_list,nl=name_list)


@auth.route('/goim',methods=['POST','GET'])
@login_required
def uptos():
	if request.method=='POST':
		global upr
		global up
		name=str(request.form.get('name'))
		hours=str(request.form.get('sec'))
		minutes=str(request.form.get('Min'))
		seconds=str(request.form.get('hours'))
		up=str(request.form.get('types'))
		upr=str(request.form.get('nvexam'))
		namess = Names.query.filter_by(ename=name).first()
		if namess:
			flash('name alredy.',category='error')
		elif name in ['nvoice','voice','fillin','voicequestion','fillinquestion','mcquestion']:
			flash('name alredy.',category='error')
		else:
			if(up=='voice'):
				voice=Voicequestion.query.all()
				voicelen=Voicequestion.query.count()
				if voicelen==0:
					flash('no  data is present in database, please upload',category='error')
				else:
					return render_template('import.html',length=voicelen,user=current_user,voice=voice)
			else:
				if(upr=='fill'):
					fill=Fillinquestion.query.all()
					filllen=Fillinquestion.query.count()
					if filllen==0:
						flash('no  data is present in database, please upload',category='error')
					else:
						return render_template('importf.html',length=filllen,user=current_user,fill=fill)
				elif(upr=='MCQ'):
					mcq=mcquestion.query.all()
					mcqlen=mcquestion.query.count()
					if mcqlen==0:
						flash('no  data is present in database, please upload',category='error')
					else:
						return render_template('importm.html',length=mcqlen,user=current_user,mcq=mcq)
	return render_template('custom.html',user=current_user)
	
@auth.route('/prepare',methods=['POST','GET'])
@login_required
def prepare():
	types=str(request.form.get('type'))
	lists=request.args.get('list').split(',')
	if(types=='voice'):
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Voice")
		for i in range(len(lists)):
			cursor.execute('''INSERT INTO Voice SELECT * FROM Voicequestion where id='''+lists[i])
		conn.commit()
		conn.close()
		messages='successfull creation.'
	elif(types=='fill'):
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Fillin")
		for i in range(len(lists)):
			cursor.execute('''INSERT INTO Fillin SELECT * FROM Fillinquestion where id='''+lists[i])
		conn.commit()
		conn.close()
		messages='successfull creation.'
	elif(types=='mcq'):
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Nvoice")
		for i in range(len(lists)):
			cursor.execute('''INSERT INTO Nvoice SELECT * FROM mcquestion where id='''+lists[i])
		conn.commit()
		conn.close()
		messages='successfull creation.'
	else:
		types='sorry that is not proper exam table.'
		lists=[]
		messages='Sorry'
	return render_template('addexam.html',messages=messages,types=types,lists=lists,user=current_user)
@auth.route('/go',methods=['POST','GET'])
@login_required
def upto():
	if request.method=='POST':
		global ups
		global upss
		upss=str(request.form.get('types'))	
		ups=str(request.form.get('nvexam'))
		name=str(request.form.get('name'))
		hours=str(request.form.get('sec'))
		minutes=str(request.form.get('Min'))
		seconds=str(request.form.get('hours'))
		namess = Names.query.filter_by(ename=name).first()
		if namess:
			flash('name alredy.',category='error')
		elif name in ['nvoice','voice','fillin','voicequestion','fillinquestion','mcquestion']:
			flash('name alredy.',category='error')
		else:
			if(upss=='voice'):
				return render_template('upload.html',hours=hours,minutes=minutes,seconds=seconds,user=current_user,name=name)
			else:
				if(ups=='fill'):
					return render_template('upload11.html',hours=hours,minutes=minutes,seconds=seconds,user=current_user,name=name)
				elif(ups=='MCQ'):
					return render_template('upload12.html',hours=hours,minutes=minutes,seconds=seconds,user=current_user,name=name)
	return render_template('custom.html',user=current_user)	
@auth.route('/upload',methods=['POST','GET'])
@login_required
def upload():
	ac=str(request.form.get('file'))
	ty=str(request.form.get('type'))
	name=str(request.form.get('ename'))
	hours=int(request.form.get('hours'))
	minutes=int(request.form.get('minutes'))
	seconds=int(request.form.get('seconds'))
	tab = Ctime.query.filter_by(types='voice').first()
	name=name.replace(' ', '_')
	if tab:
		db.session.delete(tab)
		table=Ctime(name=name,types='voice',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
		db.session.add(table)
		db.session.commit()
	tables=Names(ename=name,types='voice',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
	db.session.add(tables)
	db.session.commit()
	messager=Mail.uploadvoice(ac,ty,current_user)
	df = pd.read_csv(ac)
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	create_table_query = "CREATE TABLE IF NOT EXISTS "+name+" (id INTEGER PRIMARY KEY,subject TEXT NOT NULL,question TEXT UNIQUE)"
	cursor.execute(create_table_query)
	for index, row in df.iterrows():
		# Extract the data from the row
		column1_data = row['subject']
		column2_data = row['question']
		# Store the data in a temporary list
		temp_list = [column1_data,column2_data]
		# Store the data in the database
		cursor.execute("INSERT INTO "+name+" (subject,question) VALUES (?,?)",(column1_data,column2_data))
	conn.commit()
	conn.close()
	if messager=='user':
		flash("successfull creation of model and main exam but user not allowed to store the data.",category="success")
		return render_template('upload1.html',user=current_user)
	elif messager=='fail':
		flash("successfull creation of model and main exam but data is present in main database.",category="success")
		return render_template('upload1.html',user=current_user)
	else:
		return render_template('upload1.html',user=current_user)

@auth.route('/upload11',methods=['POST','GET'])
@login_required
def upload11():
	ac=str(request.form.get('file'))
	ty=str(request.form.get('type'))
	name=str(request.form.get('ename'))
	hours=int(request.form.get('hours'))
	minutes=int(request.form.get('minutes'))
	seconds=int(request.form.get('seconds'))
	tab = Ctime.query.filter_by(types='fill').first()
	name=name.replace(' ', '_')
	if tab:
		db.session.delete(tab)
		table=Ctime(name=name,types='fill',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
		db.session.add(table)
		db.session.commit()
	tables=Names(ename=name,types='fill',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
	db.session.add(tables)
	db.session.commit()
	messager=Mail.uploadfill(ac,ty,current_user)
	df = pd.read_csv(ac)
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	create_table_query = "CREATE TABLE IF NOT EXISTS "+name+" (id INTEGER PRIMARY KEY,subject TEXT NOT NULL,question TEXT UNIQUE,ans TEXT NOT NULL)"
	cursor.execute(create_table_query)
	for index, row in df.iterrows():
		# Extract the data from the row
		column1_data = row['subject']
		column2_data = row['question']
		column3_data = row['ans']
		# Store the data in a temporary list
		temp_list = [column1_data,column2_data,column3_data]
		# Store the data in the database
		cursor.execute("INSERT INTO "+name+" (subject,question,ans ) VALUES (?,?,?)",(column1_data,column2_data,column3_data))
	conn.commit()
	conn.close()
	if messager=='user':
		flash("successfull creation of model and main exam but user not allowed to store the data.",category="success")
		return render_template('upload1.html',user=current_user)
	elif messager=='fail':
		flash("successfull creation of model and main exam but data is present in main database.",category="success")
		return render_template('upload1.html',user=current_user)
	else:
		return render_template('upload1.html',user=current_user)

@auth.route('/upload12',methods=['POST','GET'])
@login_required
def upload12():
	ac=str(request.form.get('file'))
	ty=str(request.form.get('type'))
	name=str(request.form.get('ename'))
	hours=int(request.form.get('hours'))
	minutes=int(request.form.get('minutes'))
	seconds=int(request.form.get('seconds'))
	tab = Ctime.query.filter_by(types='mcq').first()
	name=name.replace(' ', '_')
	if tab:
		db.session.delete(tab)
		table=Ctime(name=name,types='mcq',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
		db.session.add(table)
		db.session.commit()
	tables=Names(ename=name,types='mcq',hours=hours,minutes=minutes,seconds=seconds,user_id=current_user.id)
	db.session.add(tables)
	db.session.commit()
	
	messager=Mail.uploadmcq(ac,ty,current_user)
	df = pd.read_csv(ac)
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	create_table_query = "CREATE TABLE IF NOT EXISTS "+name+" (id INTEGER PRIMARY KEY,subject TEXT NOT NULL,question TEXT UNIQUE,opt1 TEXT NOT NULL,opt2 TEXT NOT NULL,opt3 TEXT NOT NULL,opt4 TEXT NOT NULL,main TEXT NOT NULL)"
	cursor.execute(create_table_query)
	for index, row in df.iterrows():
		# Extract the data from the row
		column1_data = row['subject']
		column2_data = row['question']
		column3_data = row['opt1']
		column4_data = row['opt2']
		column5_data = row['opt3']
		column6_data = row['opt4']
		column7_data = row['main']
		# Store the data in a temporary list
		temp_list = [column1_data,column2_data,column3_data,column4_data,column5_data,column6_data,column7_data]
		# Store the data in the database
		cursor.execute("INSERT INTO "+name+" (subject,question,opt1,opt2,opt3,opt4,main ) VALUES (?,?,?,?,?,?,?)",(column1_data,column2_data,column3_data,column4_data,column5_data,column6_data,column7_data))
	conn.commit()
	conn.close()
	if messager=='user':
		flash("successfull creation of model and main exam but user not allowed to store the data.",category="success")
		return render_template('upload1.html',user=current_user)
	elif messager=='fail':
		flash("successfull creation of model and main exam but data is present in main database.",category="success")
		return render_template('upload1.html',user=current_user)
	else:
		return render_template('upload1.html',user=current_user)

@auth.route('/fill',methods =['POST','GET'])
@login_required
def fill():
	exams=Fillin.query.all()
	a=Ctime.query.filter(Ctime.types=='fill').all()
	minutes=a[0].minutes
	hours=a[0].hours
	seconds=a[0].seconds
	length=len(exams)
	for i in range(0,length):
		exams[i].ans=exams[i].ans.replace(',', '_')
	return render_template('fill.html',hours=hours,minutes=minutes,seconds=seconds,length=length,user=current_user,exams=exams)


@auth.route('/as',methods =['POST','GET'])
@login_required
def testing():
	exams=Nvoice.query.all()
	a=Ctime.query.filter(Ctime.types=='mcq').all()
	minutes=a[0].minutes
	seconds=a[0].seconds
	hours=a[0].hours
	length=len(exams)
	for i in range(0,length):
		exams[i].opt1=exams[i].opt1.replace(',', '_')
		exams[i].opt2=exams[i].opt2.replace(',', '_')
		exams[i].opt3=exams[i].opt3.replace(',', '_')
		exams[i].opt4=exams[i].opt4.replace(',', '_')
	return render_template('testing.html',hours=hours,minutes=minutes,seconds=seconds,length=length,user=current_user,exams=exams)

@auth.route('/add', methods =['POST','GET'])
@login_required
def add():
	mark=0
	lists = request.args.get('list').split(',')
	exams=Nvoice.query.all()
	types="mcq"
	answers=[]
	ansd=[]
	
	for i in range(0,len(lists)):
		lists[i]=lists[i].replace(' ','_')
		lists[i]=lists[i].replace(',','_')
		lists[i]=lists[i].lower()
	length=len(exams)
	
	for i in range(0,length):
		exams[i].main=exams[i].main.replace(',','_')
		exams[i].main=exams[i].main.replace(' ','_')
		exams[i].main=exams[i].main.lower()
		answers.append(exams[i].main)
	
	for i in range(len(lists)):
		if lists[i] in answers:
			mark=mark+1
			ansd.append(1)
		else:
			ansd.append(0)
	emails=User.query.filter(User.id==current_user.id).with_entities(User.email).all()
	email=str(emails[0].email)
	mark=int(mark)
	total=int(len(answers))
	names=Ctime.query.filter(Ctime.types=='mcq').with_entities(Ctime.name).all()
	name=str(names[0].name)
	print(name)
	marking=Result(name=name,types=types,total=total,marks=mark,user_id=current_user.id)
	db.session.add(marking)
	db.session.commit()
	messages = MIMEMultipart()
	text = """<html><head><style>h1{{color:blue;}}
	p{{font-size:14px;}}</style></head><body>
	Welcome! Hello<br><b>Exam name:</b>{name}
	<h1>Your marks:{mark}/{total}</h1>
	</html>""".format(mark=mark,total=total,name=name)
	part = MIMEText(text, 'html')
	messages.attach(part)
	message_str = messages.as_string()
	if is_valid_email(email):
		Mail.sending(email,message_str)
	else:
		flash('It is User name not to send result',category='warning')
	return render_template('result.html',types=types,ansd=ansd,total=total,user=current_user,answers=answers,lists=lists,mark=mark)

@auth.route('/vocal', methods =['POST','GET'])
@login_required
def vocal():
	mark=0
	lists = request.form.get('lists').split(',')
	exams=Voice.query.all()
	types='voice'
	answers=[]
	ansd=[]
	
	for i in range(0,len(lists)):
		lists[i]=lists[i].replace(' ','_')
		lists[i]=lists[i].replace(',','_')
		lists[i]=lists[i].lower()
	length=len(exams)
	
	for i in range(0,length):
		exams[i].question=exams[i].question.replace(',','_')
		exams[i].question=exams[i].question.replace(' ','_')
		exams[i].question=exams[i].question.lower()
		answers.append(exams[i].question)
	
	for i in range(len(lists)):
		if lists[i] in answers:
			mark=mark+1
			ansd.append(1)
		else:
			ansd.append(0)
	mark=int(mark)
	total=int(len(answers))
	names=Ctime.query.filter(Ctime.types=='voice').with_entities(Ctime.name).all()
	name=str(names[0].name)
	print(name)
	emails=User.query.filter(User.id==current_user.id).with_entities(User.email).all()
	email=str(emails[0].email)
	marking=Result(name=name,types=types,total=total,marks=mark,user_id=current_user.id)
	db.session.add(marking)
	db.session.commit()
	messages = MIMEMultipart()
	text = """<html><head><style>h1{{color:blue;}}
	p{{font-size:14px;}}</style></head><body>
	Welcome! Hello<br><b>Exam name:</b>{name}
	<h1>Your marks:{mark}/{total}</h1>
	</html>""".format(mark=mark,total=total,name=name)
	part = MIMEText(text, 'html')
	messages.attach(part)
	message_str = messages.as_string()
	if is_valid_email(email):
		Mail.sending(email,message_str)
	else:
		flash('It is User name not to send result',category='warning')
	return render_template('result.html',types=types,ansd=ansd,total=total,user=current_user,answers=answers,lists=lists,mark=mark)

@auth.route('/store',methods=['POST','GET'])
@login_required
def store():
	typer=request.args.get('types')
	ansd = request.form.get('ansd').split(',')
	answers =request.form.get('answers').split(',')
	lists =request.form.get('lists').split(',')
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	for i in range(len(ansd)):
		time.sleep(1)
		if typer=='mcq':
			cursor.execute("INSERT INTO Top (types,status,user_id) VALUES (?,?,?)",('mcq',ansd[i],current_user.id))
		elif typer=='fill':
			cursor.execute("INSERT INTO Top (types,status,user_id) VALUES (?,?,?)",('fill',ansd[i],current_user.id))
		elif typer=='voice':
			cursor.execute("INSERT INTO Top (types,status,user_id) VALUES (?,?,?)",('voice',ansd[i],current_user.id))
	conn.commit()
	conn.close()
	return render_template('store.html',user=current_user)

@auth.route('/adds', methods =['POST','GET'])
@login_required
def adds():
	mark=0
	lists = request.args.get('list').split(',')
	exams=Fillin.query.all()
	types='fill'
	answers=[]
	ansd=[]
	length=len(exams)
	
	for i in range(0,len(lists)):
		lists[i]=lists[i].replace(' ','_')
		lists[i]=lists[i].replace(',','_')
		lists[i]=lists[i].lower()
	
	for i in range(0,length):
		exams[i].ans=exams[i].ans.replace(',','_')
		exams[i].ans=exams[i].ans.replace(' ','_')
		exams[i].ans=exams[i].ans.lower()
		answers.append(exams[i].ans)

	for i in range(len(lists)):
		if lists[i] in answers:
			mark=mark+1
			ansd.append(1)
		else:
			ansd.append(0)

	total=len(answers)
	mark=int(mark)
	total=int(len(answers))
	emails=User.query.filter(User.id==current_user.id).with_entities(User.email).all()
	email=str(emails[0].email)
	mark=int(mark)
	names=Ctime.query.filter(Ctime.types=='fill').with_entities(Ctime.name).all()
	name=str(names[0].name)
	print(name)
	marking=Result(name=name,types=types,total=total,marks=mark,user_id=current_user.id)
	db.session.add(marking)
	db.session.commit()
	messages = MIMEMultipart()
	text = """<html><head><style>h1{{color:blue;}}
	p{{font-size:14px;}}</style></head><body>
	Welcome! Hello<br><b>Exam name:</b>{name}
	<h1>Your marks:{mark}/{total}</h1>
	</html>""".format(mark=mark,total=total,name=name)
	part = MIMEText(text, 'html')
	messages.attach(part)
	message_str = messages.as_string()
	if is_valid_email(email):
		Mail.sending(email,message_str)
	else:
		flash('It is User name not to send result',category='warning')
	return render_template('result.html',types=types,ansd=ansd,total=total,user=current_user,answers=answers,lists=lists,mark=mark)


@auth.route('/voice', methods=['POST','GET'])
@login_required
def index():
	return render_template('voicetest.html')

@auth.route('/voicetest', methods=['POST','GET'])
@login_required
def index1():
	k=0
	count=Voice.query.count()
	voice=lo()
	return render_template('qdisplay.html',voice=voice,i=k,user=current_user)

@auth.route('/voice/<i>/<text>',methods=['POST','GET'])
@login_required
def voice(i,text):
	
	k = int(i)
	text=text
	voice=lo()
	
	return render_template('qdisplay.html',voice=voice,i=k,user=current_user)

@auth.route('/buffer',methods=['POST','GET'])
@login_required
def buffer():
	k = int(request.args.get('i'))
	
	return render_template('qset.html',i=k,user=current_user)

@auth.route('/record', methods=['POST','GET'])
@login_required
def record():
	global a
	k = int(request.args.get('i'))
	
	count=Voice.query.count()
	texts=Mail.take_word()
	a.append(texts)
	session['alist']=a
	return render_template('qrecord.html',text=texts,i=k,user=current_user,count=count)

@auth.route('/process', methods=['POST','GET'])
@login_required
def process():
	texts = str(request.args.get('text'))
	k = int(request.args.get('i'))
	types='voice'
	count=Voice.query.count()
	a=session['alist']
	a=["wrong" if item is None else item for item in a]
	if k==(count):
		return render_template('qview.html',count=count,lists=a,types=types,user=current_user)
	else:
		return redirect(url_for('auth.voice',i=k,text=texts,user=current_user))

@auth.route('/otherexams', methods=['POST','GET'])
@login_required
def oexams():
	
	klist=[]
	k=Names.query.with_entities(Names.ename)
	
	for i in k:
		klist.append(i[0])
	klistl=len(klist)
	
	return render_template('otherexams.html',k=klist,lens=klistl,user=current_user)


@auth.route('/gousertutor',methods=['POST','GET'])
@login_required
def gousertutor():
	
	a=User.query.filter(User.types=='user').all()
	b=User.query.filter(User.types=='tutor').all()
	
	al=len(a)
	bl=len(b)
	
	return render_template('delete.html',user=current_user,alen=al,blen=bl,tutor=b,useri=a)

@auth.route('/remove',methods=['POST','GET'])
@login_required
def remove():
	lists = request.args.get('list').split(',')
	less=len(lists)
	
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	
	for i in range(0,less):
		cursor.execute("DELETE FROM User where id=="+lists[i])
	conn.commit()
	conn.close()
	
	return render_template('remove.html',user=current_user,lists=lists)

@auth.route('/passup',methods=['POST','GET'])
def updatep():

	return render_template('update.html',user=current_user)

@auth.route('/updating',methods=['POST','GET'])
def passup():
	emails=str(request.form.get('email'))
	print(emails)
	user = User.query.filter_by(email=emails).first()
	if user:
		message = str(Mail.send(emails))
		session['otp']=message
		session['email']=emails
		return render_template('passup.html',user=current_user)
	else:
		flash('Email not Registered.',category='error')
		return redirect(url_for('auth.sigup',user=current_user))



@auth.route('/verifys',methods=['POST','GET'])
def verifys():
	message=session['otp']
	emails=session['email']
	password=str(request.form.get('password'))
	if request.method=='POST':
		if message == str(request.form.get('otp')):
			updates= User.query.filter(User.email == emails ).all()
			for user in updates:
				user.password = generate_password_hash(password,method='sha256')
			db.session.commit()
			flash('Password updated!',category='success.')
			return redirect(url_for('auth.login'))
		else:
			flash('Otp is incorrect! trt again',category='failure.')
			return redirect(url_for('auth.passup'))
	else:
		return render_template('passup.html')

@auth.route('/gotoquestions',methods=['POST','GET'])
@login_required
def gotoquestion():
	a=mcquestion.query.all()
	b=Voicequestion.query.all()
	c=Fillinquestion.query.all()
	al=len(a)
	bl=len(b)
	cl=len(c)
	return render_template('questions.html',user=current_user,alen=al,blen=bl,clen=cl,b=b,a=a,c=c)

@auth.route('/removel',methods=['POST','GET'])
@login_required
def removel():
	lista = request.args.get('lista').split(',')
	listb = request.args.get('listb').split(',')
	listc = request.args.get('listb').split(',')
	lessa=len(lista)
	lessb=len(listb)
	lessc=len(listc)
	
	conn = sqlite3.connect('E:/#project/instance/coes.db')
	cursor = conn.cursor()
	
	for i in range(0,lessa):
		cursor.execute("DELETE FROM mcquestion where id=="+lista[i])
	for i in range(0,lessb):
		cursor.execute("DELETE FROM Voicequestion where id=="+listb[i])
	for i in range(0,lessc):
		cursor.execute("DELETE FROM Fillinquestion where id=="+listc[i])
	
	conn.commit()
	conn.close()
	return render_template('removel.html',user=current_user)
