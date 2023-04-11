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
	session.pop('username', None)
	return render_template('login.html')


@app.route('/register')
def register():
	return render_template('Register.html')




@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
	Username=request.form.get("Username")
	Password=request.form.get("Password")
	result=DynamoDB.get_item(Username=Username,Email="")
	print(result)
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
				flash('Email needs to be activated')
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
			flash('Email needs to be activated')
			return redirect(url_for('login'))

@app.route('/user')
def user():
	return render_template('userhomepage.html')



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
		flash('Registration Successful')
		response = ses_client.verify_email_address(EmailAddress=Email)
		return redirect(url_for('login'))
	else:
		flash(f'{result[1]} already in use')
		return redirect(url_for('register'))

@app.route('/admin/add_device',methods=['POST','GET'])
def add_device():
	Title=request.form.get("devname")
	MFD=request.form.get("mfd")
	Units=request.form.get("units")
	Brand=request.form.get("brand")
	result=DynamoDB.add_device(Title=Title,MFD=MFD,Units=Units,Brand=Brand)
	if(result == True):
		flash('Device Added Successfully')
		return redirect(url_for('add'))
	else:
		flash('Device Already exists')
		return redirect(url_for('add'))

@app.route('/admin/modify')
def modify():
	return render_template('modify.html')

@app.route('/admin/delete')
def delete():
	return render_template('deletedevice.html')


@app.route('/admin/add')
def add():
	return render_template('adddevice.html')


@app.route('/admin/delete_user')
def delete_user():
	return render_template('delete_user.html')

@app.route('/admin/view_list')
def view_list():
	display=DynamoDB.get_all_devices()
	return render_template('view_list.html',display=display)

@app.route('/admin/view_user_list')
def view_user_list():
	display=DynamoDB.get_all_rental()
	return render_template('view_user_list.html',display=display)


@app.route('/admin/return_device',methods=['POST','GET'])
def ret_device():
	if request.method == 'POST':
		result=DynamoDB.returned_device(request.form.get('Username'),request.form.get('Title'))
		if(result == "Done"):
			flash("Device Returned")
			return render_template('return_device.html')
		elif(result == "User Invalid"):
			flash("User has not rented any device")
			return render_template('return_device.html')
		else:
			flash("Incorrect Device. Device not rented by user")
			return render_template('return_device.html')
	return render_template('return_device.html')