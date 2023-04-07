from app import app
from flask import render_template,request,redirect,flash,url_for,jsonify,session
from app import DynamoDB
import boto3,json
from datetime import datetime,timedelta
import logging

ses_client = boto3.client("ses",
                          aws_access_key_id="AKIARQKRVO4SRFYI4KPJ",
		                  aws_secret_access_key="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",
		                  region_name="us-east-1"
		                  )

client = boto3.client('lambda',
                          aws_access_key_id="AKIARQKRVO4SRFYI4KPJ",
		                  aws_secret_access_key="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",
		                  region_name="us-east-1"
		                  )

@app.before_request
def before_request():
	print(session)


@app.route('/')
def login():
	session.pop('username',None)
	return render_template('login.html')
"""def index():
    return render_template('index.html')
"""
@app.route('/api/')
def api():
    return {'hello' : 'world'}

@app.route('/register')
def register():
	return render_template('Register.html')




@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
	Username=request.form.get("Username")
	Password=request.form.get("Password")
	result=DynamoDB.get_item(Username=Username,Email="")
	if(result[0]==[]):
			flash('Username does not exist')
			return redirect(url_for('login'))
	try:
		if(result[0][0]['User_Type'] == 'Admin'):
			res=ses_client.get_identity_verification_attributes(Identities=[result[0][0]['Email_Id'],])
			if(res['VerificationAttributes'][result[0][0]['Email_Id']]['VerificationStatus']=='Success'):
				if(result[0][0]['Password']==Password):
					if 'username' not in session:
						session['username'] = request.form.get("Username")
						return redirect(url_for('admin'))
					else:
						return render_template('error.html')
				else:
					flash('Incorrect Password')
					return redirect(url_for('login'))
			elif(res['VerificationAttributes'][result[0][0]['Email_Id']]['VerificationStatus']=='Pending'):
				flash('Email needs to be activate')
				return redirect(url_for('login'))
	except:
		res=ses_client.get_identity_verification_attributes(Identities=[result[0][0]['Email_Id'],])
		if(res['VerificationAttributes'][result[0][0]['Email_Id']]['VerificationStatus']=='Success'):
			if(result[0][0]['Password']==Password):
				if 'username' not in session:
					session['username'] = request.form.get("Username")
					return redirect(url_for('user'))
				else:
					return render_template('error.html')
			else:
				flash('Incorrect Password')
				return redirect(url_for('login'))
		elif(res['VerificationAttributes'][result[0][0]['Email_Id']]['VerificationStatus']=='Pending'):
			flash('Email needs to be activate')
			return redirect(url_for('login'))

@app.route('/admin')
def admin():
	return render_template('adminhomepage.html')


@app.route('/registration', methods=['POST','GET'])
def registration():
	Email=request.form.get("email")
	Username=request.form.get("Username")
	Password=request.form.get("Password")
	result=DynamoDB.add_item(Username=Username,Email=Email,Password=Password)
	if(result[0] == True):
		flash('registration successful')
		response = ses_client.verify_email_address(EmailAddress=Email)
		return redirect(url_for('login'))
	else:
		flash(f'{result[1]} already in use')
		return redirect(url_for('register'))