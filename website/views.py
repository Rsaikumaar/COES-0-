from flask import Blueprint,render_template
from flask_login import login_required,current_user
from .models import *

views = Blueprint('views',__name__)
global users

@views.route('/')
@login_required
def home():
	active =logstat.query.filter_by(status=1).count()
	permin_questions=(mcquestion.query.count()+Fillinquestion.query.count()+Voicequestion.query.count())
	questions=(Nvoice.query.count()+Voice.query.count()+Fillin.query.count())
	users=User.query.filter_by(types='student').count()
	tutor=User.query.filter_by(types='tutor').count()
	admin=User.query.filter_by(types='admin').count()
	tot_pop_db=users+admin+tutor
	return render_template("home.html",user=current_user,total=tot_pop_db,users=users,tutor=tutor,admin=admin,questions=questions,per=permin_questions,active=active)