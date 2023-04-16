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

@app.route('/admin/modify_device',methods=['POST','GET'])
def modify_device():
	Title = request.form.get("devname")
	MFD = request.form.get("mfd")
	Units = request.form.get("units")
	Brand = request.form.get("brand")
	result=DynamoDB.modify_device(Title=Title,Brand=Brand,MFD=MFD,Units=Units)
	if(result==True):
		flash("Device Modified")
		return redirect(url_for('modify'))
	else:
		flash("Device information does not exist")
		return redirect(url_for('modify'))

@app.route('/admin/delete')
def delete():
	return render_template('deletdevice.html')

@app.route('/admin/delete_device',methods=['POST','GET'])
def delete_device():
	title=request.form.get("devname")
	#author=request.form.get("author")
	#edition=request.form.get("edition")
	DynamoDB.delete_device(title.upper())
	flash("Device info deleted")
	return redirect(url_for('delete'))

@app.route('/admin/add')
def add():
	return render_template('adddevice.html')


@app.route('/admin/delete_user')
def delete_user():
	return render_template('delete_user.html')

@app.route('/admin/delete_user',methods=['POST','GET'])
def user_deleted():
	Email=request.form.get("email")
	Username=request.form.get("Username")
	result=DynamoDB.delete_item(Username=Username,Email=Email)
	if(result=="Done"):
		flash("User Deleted")
		return render_template('delete_user.html')
	elif(result=="Not Done"):
		flash("No User Found")
		return render_template('delete_user.html')

@app.route('/admin/view_list')
def view_list():
	#display=DynamoDB.get_all_devices()
	display=DynamoDB.searching_devices("")
	return render_template('view_list.html', display=display)

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

@app.route('/Normal/user')
def user():
	return render_template('userhomepage.html')



@app.route('/Normal/user/search')
def search():
	return render_template('search.html')

@app.route('/Normal/user/search/result',methods=['POST','GET'])
def search_executed():
	searching=request.form.get('search')
	result=DynamoDB.searching_devices(searching)
	return render_template('issue_device.html', display=result)

@app.route('/Normal/user/issue',methods=['POST','GET'])
def issue():
	if request.method == 'POST':
		device={"Device_Title":"","Brand":"","Units":0,"Issue_Date":"","End_Date":""}
		splits=[]
		Check=request.form.get('Rent')
		splits=Check.split("_")
		device['Device_Title']=splits[0]
		device['Brand']=splits[1]
		device['Units']=int(splits[2])
		device['Issue_Date']=str(datetime.now().date())
		device['End_Date']=str((datetime.now().date() + timedelta(10)))
		return render_template('Rent.html', Device_info=device)
	display=DynamoDB.searching_devices("")
	return render_template('issue_device.html', display=display)

@app.route('/Normal/user/renew',methods=['POST','GET'])
def renew():
	if request.method == 'POST':
		Title=request.form.get('devname')
		#Brand=request.form.get('brand')
		Days=request.form.get('days')
		username=session.get('username')
		result=DynamoDB.renew(username,Title.upper(), Days)
		if(result == "Done"):
			flash("Return date extended")
			return render_template('renew.html')
		else:
			flash("Device not rented. Please provide correct data")
			return render_template('renew.html')
	else:
		return render_template('renew.html')


@app.route('/Normal/user/confirmation',methods=['POST','GET'])
def confirmation():
	if request.method == 'POST':
		if(request.form.get('action2') == "Cancel"):
			return redirect(url_for('search'))
		else:
			username=session.get('username')
			result=DynamoDB.RentingDevice(username,request.form.get('devname'),request.form.get('brand'),request.form.get('Units'),request.form.get('IssueDate'),request.form.get('ReturnDate'))
			if(result=="Done"):
				username=session.get('username')
				#print(username)
				email=DynamoDB.get_email1_item(Username=username)
				title=request.form.get('devname')
				return_date=request.form.get('ReturnDate')
				#print(return_date)
				#print(email)
				#print(title)
				#payload = {"from_address": "preetha1999@gmail.com","from_name": "Cloud Library","to_address":email,"email_subject": "Book Rented today"}
				#payload={"from_address": "preetha1999@gmail.com","from_name": "Cloud Library","to_address": email, "email_subject": "Book Rented today", "text":" Thank you for renting the book from our library.Please return the book by the ","issue_date":return_date,"text1":"to avoid any fine."}
				#payload={"from_address": "preetha1999@gmail.com","from_name": "Cloud Library","to_address": email, "email_subject": "Book Rented today","user":username,"book:":title,"issue_date":return_date}
				payload={
  							"from_address": "ruchita.bhadre@mail.utoronto.ca",
  							"from_name": "ECE TOOLS LIBRARY",
  							"to_address": email,
  							"email_subject": "Device Rented",
  							"issue_date": return_date,
  							"user": username,
  							"device": title}
				response = client.invoke(FunctionName='sendMail',InvocationType='RequestResponse',Payload=json.dumps(payload))
				flash("Please collect the Device from Lab in Galbraith Building on 3rd floor")
				return redirect(url_for('search'))
			elif(result=="Already There"):
				flash("Cant rent the same device again")
				return redirect(url_for('search'))
			elif(result=="No Device"):
				flash("No units left")
				return redirect(url_for('search'))
			else:
				flash("Maximum number of devices in account exceeded")
				return redirect(url_for('search')) 
