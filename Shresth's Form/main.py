from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
app=Flask(__name__)
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\Users\hgp99\OneDrive\Desktop\Python learning\Shresth's Form\login_data.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    First_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Last_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    Password:Mapped[str]=mapped_column(String(250),nullable=False)

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
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
    cpassword=request.form["conpassword"]
    if password==cpassword:
        with app.app_context():
            new_user = User(First_Name=f"{fname}",Last_Name=f"{lname}",Email=f"{email}",Password=f"{password}")
        db.session.add(new_user)
        db.session.commit()

    return f"<h1>Succesful Submission</h1>"
@app.route('/login/successful',methods=['GET','POST'])
def loggedin():
    email=request.form["email"]
    password=request.form["password"]
    var=False
    with app.app_context():
        result = db.session.execute(db.select(User).order_by(User.First_Name))
        all_users=result.scalars()
        for user in all_users:
            Demail=user.Email
            Dpassword=user.Password
            print(Demail)
            if Demail==email and Dpassword==password:
                var=True
                key=user
        if var:
            return f"<h1>Successfully Logged in as {key.First_Name} {key.Last_Name}</h1>"
        else:
            return f"<h1>Your credentials dont match</h1>"
if __name__=="__main__":
    app.run(debug=True)