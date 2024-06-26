from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,func
from flask import jsonify
import base64
from My_packages import email
app=Flask(__name__)
class Base(DeclarativeBase):
    pass
mail=email.Mail()
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///user_data.db"
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "image_uploads"
app.jinja_env.filters['decode'] = base64.b64decode
db = SQLAlchemy(model_class=Base)
db.init_app(app)
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    First_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Last_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    Password:Mapped[str]=mapped_column(String(250),nullable=False)
    Confirm_Password:Mapped[str]=mapped_column(String(250),nullable=False)
    Branch:Mapped[str] = mapped_column(String(250),nullable=False)
    # Status:Mapped[str] = mapped_column(String(250),nullable=False)
    Current_Company:Mapped[str] = mapped_column(String(250),nullable=False)
    Current_Working_Position:Mapped[str] = mapped_column(String(250),unique=False,nullable=False)
    Image:Mapped[str] = mapped_column(String(100000),nullable=False)
    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template('indexc.html')
@app.route('/login')
def logs():
    return render_template('index4.html')
@app.route('/loginform')
def login():
    return render_template('login.html')
@app.route('/signup',methods=['GET','POST'])
def done():
    global fname
    global lname
    fname=request.form["firstname"].title()
    lname=request.form["lastname"].title()
    email=request.form["email"]
    password=request.form["password"]
    conpassword=request.form["conpassword"]
    # status=request.form["status"]
    branch=request.form["branch"]
    company=request.form["company"]
    position=request.form["position"]
    file=request.files["pic"]
    if password==conpassword:
        image_content = file.read()
            # Encode the bytes-like object as a base64 string
        image_64_encode = base64.b64encode(image_content).decode()
        with app.app_context():
            new_user = User(First_Name=f"{fname}",Last_Name=f"{lname}",Email=f"{email}",Password=f"{password}",Confirm_Password=f"{conpassword}",Branch=f"{branch}",Current_Company=f"{company}",Current_Working_Position=f"{position}",Image=f"{image_64_encode}")
        db.session.add(new_user)
        db.session.commit()

    return render_template('login.html')
@app.route('/login/successful',methods=['GET','POST'])
def loggedin():
    email=request.form["email"]
    password=request.form["password"]
    var=False
    result = db.session.execute(db.select(User).order_by(User.First_Name))
    all_users=result.scalars()
    global firstnames
    for user in all_users:
        Demail=user.Email
        Dpassword=user.Password
        # firstnames=firstnames+user.First_Name
        if Demail==email and Dpassword==password:
            var=True
    if var==True:
        return render_template('index.html')
    else:
        return render_template('login.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/searchuser',methods=['GET','POST'])
def search():
    user_id = request.form['searchuser'].lower()

    # Retrieve users with matching first name (case-insensitive)
    matching_users = []
    users = User.query.filter(func.lower(User.First_Name) == user_id).all()
    for user in users:
        matching_users.append(user.to_dict())

    if matching_users:
        return render_template('namecard.html',users=matching_users,var=True,name=user_id)
    else:
        return render_template('namecard.html',var=False,name=user_id)
if __name__=="__main__":
    app.run(debug=True)