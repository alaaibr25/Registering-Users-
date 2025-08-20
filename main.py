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
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)    #🔸2# initialize the app with the extension

#🔸3# Define Models
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] =mapped_column(nullable=False, unique=True)
    pword: Mapped[str] =mapped_column(nullable=False)
    name: Mapped[str] =mapped_column(nullable=False,)

#🔸4# Create the Tables
with app.app_context():
    db.create_all()

#🔽=============================================================🔽#
from werkzeug.security import generate_password_hash, check_password_hash

#Configuring Application
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

#🔽=============================================================🔽#


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/log', methods=['POST','GET'])
def login_page():
    form = LogForm()
    if form.validate_on_submit():
        email = form.log_mail.data
        pw = form.log_pw.data
        
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if check_password_hash(user.pword, pw):
            login_user(user)
            flask.flash('Logged in successfully')
            return redirect(url_for('secret_page'))
        
    return render_template('log.html', form=form)


@app.route('/reg', methods=['POST', 'GET'])
def register():
    form = UsersForm()
    if form.validate_on_submit():
        hashed_salted_pw = generate_password_hash(form.pswd.data,
                                                  method='pbkdf2:sha256:600000',
                                                  salt_length=8)
        new_user = User()
        new_user.email=form.email.data
        new_user.name=form.name.data
        new_user.pword=hashed_salted_pw
        
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        
        return render_template('secret.html')
    return render_template('register.html', form=form)

@app.route('/sec')
@login_required
def secret_page():
    return render_template('secret.html', name=current_user.name)


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))


app.run(debug=True)





