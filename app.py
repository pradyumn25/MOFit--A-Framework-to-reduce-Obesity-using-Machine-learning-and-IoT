from flask import Flask,render_template, request, redirect
# from flask.globals import session
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_mail import Mail
import pickle
# import pyrebase

app = Flask(__name__)
app.secret_key = 'super_secret_key'

config = {
    "apiKey": "AIzaSyBQlseqhUdxSJ0Yggqu0erfkf5ScCz4HWk",
    "authDomain": "mofit-cf8a6.firebaseapp.com",
    "databaseURL": "https://mofit-cf8a6-default-rtdb.firebaseio.com/",
    "projectId": "mofit-cf8a6",
    "storageBucket": "mofit-cf8a6.appspot.com",
    "messagingSenderId": "278465517798",
    "appId": "1:278465517798:web:90c7014bb3dd7a822b8327",
    "measurementId": "G-796RD4BSL4"
}

local_server =  "True"


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "pundirdemo@gmail.com",
    MAIL_PASSWORD=  "Par@12345"
)

s = Serializer('sekrit', expires_in=300)

mail = Mail(app)

# class Signup(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     first = db.Column(db.String(80), unique=False, nullable=False)
#     last = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(20),  nullable=False)
#     email = db.Column(db.String(80),  nullable=False)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route("/") #home page------------------------
def index():
    return render_template('index.html')

@app.route("/logout")  #logout
def logout():
    session.pop('name')
    return render_template('index.html')


    # ------------------------------------ sign up ---------------------

@app.route("/signup",methods = ['GET', 'POST'])  
def signup():
    all_users = db.child("names").get()
    # for user in all_users.each():
    #     print(user.key())  # Morty

    if (request.method == 'POST'):
        code = request.form.get('code')
        email = request.form.get('email')
        if(s.loads(code) == email):

            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            password = request.form.get('pass')

            for user in all_users.each():
                if(user.key() == email):
                    error = "You are already Registered"
                    return render_template('signup.html', error=error)
                    break
                else:
                    error = "You are Now Registered Please Sign In"

            if(error == "You are Now Registered Please Sign In"):
                db.child("users").push({
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password,
                    "email": email
                })
                return render_template('signup.html',error=error)

        else:
            token_status = "Wrong Token Or Email Already Registered Please Renter Email-Address"
            return render_template('id_check.html', token_status= token_status)

    return render_template('signup.html')

    # ------------------------------------ sign in ---------------------

# @app.route("/signin",methods = ['GET', 'POST'])
# def signin():
#     if (request.method == 'POST'):
#         details = Signup.query.filter_by().all()
#
#         email = request.form.get('email')
#         password = request.form.get('password')
#
#         for details in details:
#             if(details.email == email and details.password == password):
#                 status = "Ok"
#                 session['name'] = details.first
#                 break
#             else:
#                 status = "Provide Right Details"
#
#         if(status == "Provide Right Details"):
#             return render_template('signin.html',status=status)
#
#         elif(status == "Ok"):
#             return render_template('index.html')
#
#
#
#     return render_template('signin.html')
#
#     # ------------------------------------ id check (if you are already registered or not) ---------------------
#
#
@app.route('/id_check',methods=['GET','POST'])
def id_check():
    all_users = db.child("names").get()
    # for user in all_users.each():
    #     print(user.key())  # Morty

    if (request.method == 'POST'):
        id_check_email = request.form.get('id_check_email')
        for user in all_users.each():
            print(user.key())  # Morty
            if id_check_email == user.key():
                error = 'Email-id Already Registered'
                break
            else:
                error = 'A verification link has been sent to your Email-id'

        if(error == 'Email-id Already Registered'):
            return render_template('id_check.html',id_check_error=error)

        else:
            token = s.dumps(id_check_email)
            token = token.decode("utf-8")
            reci = id_check_email

            mail.send_message('New Message From '+ 'Mo-fit',
                            sender='pundirdemo@gmail.com',
                            recipients = [reci],
                            body="please copy this token ==> " +  token + " (valid for 5 minutes only) "
                            )

            return redirect('signup')

    return render_template('id_check.html')

#     # ------------------------------------ forgot password ---------------------
#
#
# @app.route("/forgot", methods=['GET','POST'])
# def forgot():
#
#     if (request.method == 'POST'):
#         email = request.form.get('email')
#         details = Signup.query.filter_by().all()
#
#         for details in details:
#             if (email == details.email):
#                 token = s.dumps(email)
#                 token = token.decode("utf-8")
#
#                 mail.send_message('New Message From '+ 'Mo-fit',
#                                 sender='pundirdemo@gmail.com',
#                                 recipients = [email],
#                                 body="please copy this token ==> " +  token + " (valid for 5 minutes only) "
#                                 )
#
#                 return redirect('reset_pass')
#                 break
#             else:
#                 error = "You are not Registered"
#
#         if(error == "You are not Registered"):
#             return render_template("forgot.html", error=error)
#
#         else:
#             pass
#
#     return render_template('forgot.html')
#
#     # ------------------------------------ reset password ---------------------
#
# @app.route("/reset_pass", methods=['GET','POST'])
# def reset_pass():
#     if (request.method == 'POST'):
#         code = request.form.get('verify')
#         email = request.form.get('email')
#         password = request.form.get('new_pass')
#
#         if(s.loads(code) == email):
#             details = Signup.query.filter_by(email = email).first()
#             details.password = password
#             db.session.commit()
#
#             return render_template('success.html')
#         else:
#             error = 'Verifaication Code Error Retry'
#             return render_template('forgot.html', reset_error = error)
#     return render_template("reset_pass.html",sent = "A Verification Code has Been Send To your Email.")
#
#     # ------------------------------------ body_fat ---------------------
#
# @app.route("/body_fat", methods=['GET','POST'])
# def calculate():
#     if ('name' in session):
#         if (request.method == 'POST'):
#             age = int(request.form.get('age'))
#             weight = float(request.form.get('weight'))
#             height = float(request.form.get('height'))
#             neck = float(request.form.get('neck'))
#             chest = float(request.form.get('chest'))
#             abdomen = float(request.form.get('abdomen'))
#             hip = float(request.form.get('hip'))
#             thigh = float(request.form.get('thigh'))
#             knee = float(request.form.get('knee'))
#             ankle = float(request.form.get('ankle'))
#             biceps = float(request.form.get('biceps'))
#             forearm = float(request.form.get('forearm'))
#             wrist = float(request.form.get('wrist'))
#
#             with open('BodyFat_RandomForest.pkl', 'rb') as file:
#                 model = pickle.load(file)
#
#             result = model.predict([[age,weight,height,neck,chest,abdomen,hip,thigh,knee,ankle,biceps,forearm,wrist]])
#             result = result[0]
#             result = float("{:.2f}".format(result))
#             result = str(result)
#             # new_result = "{:.2f}".format(result[0])
#             return render_template('body_fat.html', result="Your Body Fat Percentage is "+result)
#     else:
#         return render_template('signin.html')
#
#     return render_template('body_fat.html')
#
#     # ------------------------------------ obesity ---------------------
#
# @app.route("/obesity", methods=['GET','POST'])
# def obesity():
#     if ('name' in session):
#         if (request.method == 'POST'):
#             gender = int(request.form.get('gender'))
#             age = int(request.form.get('age'))
#             weight = request.form.get('weight')
#             height = request.form.get('height')
#             history = int(request.form.get('history'))
#             favc = int(request.form.get('favc'))
#             fcvc = float(request.form.get('fcvc'))
#             ncp = float(request.form.get('ncp'))
#             scc = int(request.form.get('scc'))
#             caec = float(request.form.get('caec'))
#             smoke = int(request.form.get('smoke'))
#             ch2o = float(request.form.get('ch2o'))
#             faf = float(request.form.get('faf'))
#             tue = float(request.form.get('tue'))
#             calc = request.form.get('calc')
#             mtrans = request.form.get('mtrans')
#
#             bmi = float(weight)/(float(height)*float(height))
#             bmi = str(bmi)
#
#             if (calc == 'f'):
#                 frequently = 1
#                 sometimes = 0
#                 no = 0
#             elif (calc == 's'):
#                 frequently = 0
#                 no = 0
#                 sometimes = 1
#             elif (calc == 'n'):
#                 frequently = 0
#                 sometimes = 0
#                 no = 1
#
#             if (mtrans == 'b'):
#                 bike = 1
#                 motorbike = 0
#                 public = 0
#                 walking = 0
#             elif (mtrans == 'm'):
#                 motorbike = 1
#                 bike = 0
#                 public = 0
#                 walking = 0
#             elif (mtrans == 'p'):
#                 public = 1
#                 bike = 0
#                 motorbike = 0
#                 walking = 0
#             elif (mtrans == 'w'):
#                 walking = 1
#                 bike = 0
#                 public = 0
#                 motorbike = 0
#
#
#             with open('Obesity_level_RandomForest.pkl', 'rb') as file:
#                 model = pickle.load(file)
#
#             result = model.predict([[gender,age,history,favc,fcvc,ncp,caec,smoke,ch2o,scc,faf,tue,1,frequently,sometimes,no,bike,motorbike,public,walking]])
#             result = result[0]
#             result = float("{:.2f}".format(result))
#             result = str(result)
#
#             if (result == '0'):
#                 lvl = 'Insufficient_Weight'
#             elif (result == '1'):
#                 lvl = 'Normal_Weight'
#             elif (result == '2'):
#                 lvl = 'Overweight_Level_I'
#             elif (result == '3'):
#                 lvl = 'Overweight_Level_II'
#             elif (result == '4'):
#                 lvl = 'Overweight_Level_III'
#
#             return render_template('obesity.html', bmi="Your BMI = "+bmi, result="Your Obesity Status = "+lvl)
#
#     else:
#         return render_template('signin.html')
#
#     return render_template('obesity.html')
#
# @app.route("/contact", methods=['GET','POST'])  #--------------------------- contact us---------
# def contact():
#     if (request.method == 'POST'):
#         content = request.form.get('contact')
#         email = request.form.get('email')
#         mail.send_message('New Message From '+ 'Mo-fit',
#                                     sender='pundirdemo@gmail.com',
#                                     recipients = ['pundirdemo@gmail.com'],
#                                     body = "this message is from = "+email+" ==> "+content
#                                     )
#     return render_template('index.html')
#
#
# @app.route("/store", methods=['GET','POST'])  #--------------------------- calorie counter and plan your diet---------
# def store():
#     if ('name' in session):
#         if (request.method == 'POST'):
#             gender = request.form.get('gender')
#             age = request.form.get('age')
#             weight = request.form.get('weight')
#             height = request.form.get('height')
#
#             if (gender == '1'):
#                 result = (10*float(weight))+(6.25*float(height))-(5*float(age))+5
#                 result = str(result)
#                 return render_template('store.html',result = "Basal Metabolic Rate (BMR) = "+result)
#             elif (gender == '0'):
#                 result = (10*float(weight))+(6.25*float(height))-(5*float(age))-161
#                 result = str(result)
#                 return render_template('store.html',result = "Basal Metabolic Rate (BMR) = "+result)
#
#     else:
#         return render_template('signin.html')
#
#     return render_template('store.html')
#
#
        
app.run(debug=True)