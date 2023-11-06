from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from app import db
from app.models import *
from flask_login import current_user


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    sign_up = SubmitField('Sign Up')

    def validate_username(self, username):
        """Function that checks he uniqueness of the username"""
        user = User.query.filter_by(username=username.data.rstrip()).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        """Function that checks the uniqueness of the email"""
        user = User.query.filter_by(email=email.data.rstrip()).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different email.')
        
    # def validate_password(self, password):
    #     """Function that checks the strength of the password"""
    #     if any(char.isdigit() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one number.')
    #     if any(char.isupper() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one uppercase letter.')
    #     if any(char.islower() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one lowercase letter.')
    #     special_character_ranges = [(33, 48), (58, 65), (123, 127)]
    #     for char in password.data:
    #         if any(start <= ord(char) <= end for start, end in special_character_ranges):
    #             break
    #     else:
    #         raise ValidationError('Password must contain at least one special character.')
        
class SignInForm(FlaskForm):
    """Sign in form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    sign_in = SubmitField('Sign In')

    def validate_username(self, username):
        """Function that checks if the username exists"""
        user = User.query.filter_by(username=username.data.rstrip()).first()
        if user is None:
            raise ValidationError('Username does not exist. Please try again.')

    def validate_password(self, password):
        """Function that checks if the password is correct"""
        user = User.query.filter_by(username=self.username.data.rstrip()).first()
        if user is not None:
            if check_password_hash(user.password_hash, password.data.rstrip()) == False:
                raise ValidationError('Password is incorrect. Please try again.')


class EditDetails(FlaskForm):
    """Edit user details"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    edit = SubmitField('Edit')

    def validate_username(self, username):
        """Function that checks he uniqueness of the username"""
        user = User.query.filter_by(username=username.data.rstrip()).first()
        if user and user.email != current_user.email:
            raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        """Function that checks the uniqueness of the email"""
        user = User.query.filter_by(email=email.data.rstrip()).first()
        if user and user.username != current_user.username:
            raise ValidationError('Email already exists. Please choose a different email.')
        
class EditPassword(FlaskForm):
    """Edit user password"""
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8, max=64)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=64)])
    edit = SubmitField('Change')

    def validate_old_password(self, old_password):
        """Function that checks if the password is correct"""
        user = User.query.filter_by(username=current_user.username.rstrip()).first()
        if user is not None:
            if check_password_hash(user.password_hash, old_password.data.rstrip()) == False:
                raise ValidationError('Password is incorrect. Please try again.')
    
    # def validate_new_password(self, password):
    #     """Function that checks the strength of the password"""
    #     if any(char.isdigit() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one number.')
    #     if any(char.isupper() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one uppercase letter.')
    #     if any(char.islower() for char in password.data) == False:
    #         raise ValidationError('Password must contain at least one lowercase letter.')
    #     special_character_ranges = [(33, 48), (58, 65), (123, 127)]
    #     for char in password.data:
    #         if any(start <= ord(char) <= end for start, end in special_character_ranges):
    #             break
    #     else:
    #         raise ValidationError('Password must contain at least one special character.')

class DeleteAccount(FlaskForm):
    """Delete user account"""
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    delete = SubmitField('Delete')

    def validate_password(self, password):
        """Function that checks if the password is correct"""
        user = User.query.filter_by(username=current_user.username.rstrip()).first()
        if user is not None:
            if check_password_hash(user.password_hash, password.data.rstrip()) == False:
                raise ValidationError('Password is incorrect. Please try again.')
