#🔽=============================================================🔽#
import flask
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
app = Flask(__name__)   #🔸1# create the app

#🔽=============================================================🔽#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired
import os

app.secret_key = os.getenv('SCK')

class UsersForm(FlaskForm):
    name = StringField(label='', validators=[DataRequired()])
    email = EmailField(label='', validators=[DataRequired()])
    pswd = PasswordField(label='', validators=[DataRequired()])
    submit = SubmitField('Sign Me In')

class LogForm(FlaskForm):
    log_mail = EmailField(label='', validators=[DataRequired()])
    log_pw = PasswordField(label='', validators=[DataRequired()])
    log_submit = SubmitField('Log In')

#🔽=============================================================🔽#
from flask_bootstrap import Bootstrap5
bstrap = Bootstrap5(app)

#🔽=============================================================🔽#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)    #🔸2# initialize the app with the extension

#🔸3# Define Models
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] =mapped_column(nullable=False, unique=True)
    pword: Mapped[str] =mapped_column(nullable=False)
    name: Mapped[str] =mapped_column(nullable=False,)

#🔸4# Create the Tables
with app.app_context():
    db.create_all()

#🔽=============================================================🔽#
from werkzeug.security import generate_password_hash

#🔽=============================================================🔽#


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/log', methods=['POST','GET'])
def login_page():
    form = LogForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == 'alaa@yahoo.com')).scalar()
        login_user(user)
        flask.flash('Logged in successfully')
        
    return render_template('log.html', form=form)


@app.route('/reg', methods=['POST', 'GET'])
def register():
    form = UsersForm()
    if form.validate_on_submit():
        hashed_salted_pw = generate_password_hash(form.pswd.data,
                                                  method='pbkdf2:sha256:600000',
                                                  salt_length=8)
        new_user = User(
                        email=form.email.data,
                        name=form.name.data,
                        pword=hashed_salted_pw)
        db.session.add(new_user)
        db.session.commit()
        return render_template('secret.html', name=form.name.data)



    return render_template('register.html', form=form)

@app.route('/download')
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')




app.run(debug=True)



