from . import db
from flask_login import UserMixin
from sqlalchemy import func
import smtplib
import random
import speech_recognition as sr
import pandas as pd
import sqlite3

global scc
global v1
global v2
global v3
global v4
global types
global firstname
global lastname
global password1
global password2
global email
email ="9"
global vk
vk=[]
global answer
answer={}
global count
global c
global keen
global mark
global a
global keen_list
keen_list=[]
global answer_list
answer_list=[]
global mark
global k
k=0
global ko
ko=[]
mark=0
a=['0']
keen={}
i=0

class logstat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.Integer, db.CheckConstraint('status IN (0, 1)'), nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", back_populates="status")
	
class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	email =db.Column(db.String(250),unique=True)
	types =db.Column(db.String(250),nullable=False)
	password=db.Column(db.String(500),nullable=False)
	firstname=db.Column(db.String(150),nullable=False)
	lastname=db.Column(db.String(150),nullable=False)
	status = db.relationship('logstat',back_populates="user")
	names = db.relationship("Names", back_populates="user")
	result = db.relationship("Result", back_populates="user")
	top = db.relationship("Top", back_populates="user")
	ctime = db.relationship("Ctime", back_populates="user")
class Names(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	ename=db.Column(db.String(200),nullable=True)
	types=db.Column(db.String(200),nullable=False)
	hours =db.Column(db.Integer,nullable=False)
	minutes=db.Column(db.Integer,nullable=False)
	seconds=db.Column(db.Integer,nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", back_populates="names")
#project
class Ctime(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(200),nullable=False)
	types=db.Column(db.String(200),nullable=False)
	hours =db.Column(db.Integer,nullable=False)
	minutes=db.Column(db.Integer,nullable=False)
	seconds=db.Column(db.Integer,nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", back_populates="ctime")

class Result(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(200),nullable=False)
	types=db.Column(db.String(200),nullable=False)
	total = db.Column(db.Integer,nullable=False)
	marks = db.Column(db.Integer,nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", back_populates="result")

class Top(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	types=db.Column(db.String(200),nullable=False)
	status = db.Column(db.Integer,nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", back_populates="top")
#INSERT INTO nvoice (subject,question, opt1, opt2, opt3, opt4, main) 
#VALUES ('Gk','What is the capital of France?', 'Paris', 'Rome', 'Madrid', 'Berlin', 'Paris');

#permenent
class mcquestion(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(200),nullable=False)
	question = db.Column(db.String(500),unique=True)
	opt1 =db.Column(db.String(250),nullable=False)
	opt2 =db.Column(db.String(250),nullable=False)
	opt3 =db.Column(db.String(250),nullable=False)
	opt4 =db.Column(db.String(250),nullable=False)
	main =db.Column(db.String(250),nullable=False)

class Voicequestion(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(100),nullable=False)
	question = db.Column(db.String(500),unique=True)

class Fillinquestion(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(100),nullable=False)
	question = db.Column(db.String(500),unique=True)
	ans = db.Column(db.String(100),nullable=False)
	
#temporay
class Voice(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(100),nullable=False)
	question = db.Column(db.String(500),unique=True)

class Fillin(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(100),nullable=False)
	question = db.Column(db.String(500),unique=True)
	ans = db.Column(db.String(100),nullable=False)

class Nvoice(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	subject = db.Column(db.String(200),nullable=False)
	question = db.Column(db.String(500),unique=True)
	opt1 =db.Column(db.String(250),nullable=False)
	opt2 =db.Column(db.String(250),nullable=False)
	opt3 =db.Column(db.String(250),nullable=False)
	opt4 =db.Column(db.String(250),nullable=False)
	main =db.Column(db.String(250),nullable=False)
#send OTP to mail
class Mail():
	def send(mail):
		otp = str(random.randint(100000, 999999))
		sender_email = "saikumap@gmail.com"
		receiver_email = mail
		password = "iymkukmmfhftedhk"
	
		message=otp

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, password)

		server.sendmail(sender_email, receiver_email, message)
		print("OTP sent successfully")

		server.quit()

		return message
	
	def sending(mail,message):
		
		sender_email = "saikumap@gmail.com"
		receiver_email = mail
		password = "iymkukmmfhftedhk"
		messages = message
		success="done"
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, password)

		server.sendmail(sender_email, receiver_email, messages)
		print("OTP sent successfully")

		server.quit()

		return success
	# Read the Excel file
	def uploadvoice(k,t,user):
		df = pd.read_csv(k)
		# Connect to the database
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		# Iterate over each row in the DataFrame
		cursor.execute("DELETE FROM Voice")
		for index, row in df.iterrows():
			# Extract the data from the row
			column1_data = row['subject']
			column2_data = row['question']
			# Store the data in a temporary list
			temp_list = [column1_data,column2_data]
			# Store the data in the database
			cursor.execute("INSERT INTO Voice (subject,question ) VALUES (?,?)",(column1_data,column2_data))
		cursor.execute("SELECT question FROM Voice")
		voice_questions = [row[0] for row in cursor.fetchall()]
		cursor.execute("SELECT question FROM Voicequestion")
		voice_question_questions = [row[0] for row in cursor.fetchall()]
		a='fail'
		b='user'
		if any(question in voice_question_questions for question in voice_questions):
			print("false")
			conn.commit()
			conn.close()
			return a
		else:
			print("success")
			if t =="yes":
				cursor.execute("INSERT INTO Voicequestion SELECT * FROM Voice")
				conn.commit()
				conn.close()
			else:
				print("the user didn't allowed.")
				conn.commit()
				conn.close()
				return b
			# Commit the changes and close the connection
	def uploadmcq(k,t,user):
		df = pd.read_csv(k)
		# Connect to the database
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		# Iterate over each row in the DataFrame
		cursor.execute("DELETE FROM Nvoice")
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
			cursor.execute("INSERT INTO Nvoice (subject,question,opt1,opt2,opt3,opt4,main ) VALUES (?,?,?,?,?,?,?)",(column1_data,column2_data,column3_data,column4_data,column5_data,column6_data,column7_data))
		cursor.execute("SELECT question FROM Nvoice")
		voice_questions = [row[0] for row in cursor.fetchall()]
		cursor.execute("SELECT question FROM mcquestion")
		voice_question_questions = [row[0] for row in cursor.fetchall()]
		a='fail'
		b='user'
		if any(question in voice_question_questions for question in voice_questions):
			print("false")
			conn.commit()
			conn.close()
			return a 
		else:
			print("success")
			if t =="yes":
				cursor.execute("INSERT INTO mcquestion SELECT * FROM Nvoice")
				conn.commit()
				conn.close()
			else:
				print("the user didn't allowed.")
				conn.commit()
				conn.close()
				return b

	def uploadfill(k,t,user):
		df = pd.read_csv(k)
		# Connect to the database
		conn = sqlite3.connect('E:/#project/instance/coes.db')
		cursor = conn.cursor()
		# Iterate over each row in the DataFrame
		cursor.execute("DELETE FROM Fillin")
		for index, row in df.iterrows():
			# Extract the data from the row
			column1_data = row['subject']
			column2_data = row['question']
			column3_data = row['ans']
			
			temp_list = [column1_data,column2_data,column3_data]
			# Store the data in the database
			cursor.execute("INSERT INTO Fillin (subject,question,ans ) VALUES (?,?,?)",(column1_data,column2_data,column3_data))
		cursor.execute("SELECT question FROM Fillin")
		voice_questions = [row[0] for row in cursor.fetchall()]
		cursor.execute("SELECT question FROM Fillinquestion")
		voice_question_questions = [row[0] for row in cursor.fetchall()]
		a='fail'
		b='user'
		if any(question in voice_question_questions for question in voice_questions):
			print("false")
			conn.commit()
			conn.close()
			return a
		else:
			print("success")
			if t =="yes":
				cursor.execute("INSERT INTO Fillinquestion SELECT * FROM Fillin")
				conn.commit()
				conn.close()
			else:
				print("the user didn't allowed.")
				conn.commit()
				conn.close()
				return b

	def take_word():
		def stop_listening():
			listener.stop()
		listener = sr.Recognizer()
		command = 'node'
		with sr.Microphone() as source:
			print('Listening...')
			voice = listener.listen(source, timeout=10, phrase_time_limit=5)    
			try:
				command = listener.recognize_google(voice)
				return command
			except sr.UnknownValueError:
				print("Unable to recognize speech")
			except sr.RequestError as e:
				print(f"Speech recognition request error: {str(e)}")
				# Cancel the timer if the function completes before the timeout
		return command  # Return None if no speech is recognized
