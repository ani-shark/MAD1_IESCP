from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices = [('sponsor', 'Sponsor'), ('influencer', 'Influencer')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class UpdateSponsorProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class UpdateInfluencerProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    niche = TextAreaField('Niche', validators=[DataRequired()])
    reach = StringField('Reach', validators=[DataRequired()])
    instagram_handle = StringField('Instagram Handle')
    profile_picture = StringField('Profile Picture URL')
    submit = SubmitField('Update Profile')

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    submit = SubmitField('Create Campaign')

class AdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign', coerce=int, validators=[DataRequired()])
    influencer_id = SelectField('Influencer', coerce=int, validators=[DataRequired()])
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Create Ad Request')

class SearchInfluencerForm(FlaskForm):
    category = StringField('Category', validators=[Optional()])
    min_reach = FloatField('Minimum Reach', validators=[Optional()])
    max_reach = FloatField('Maximum Reach', validators=[Optional()])
    submit = SubmitField('Search', validators=[Optional()])

class NegotiateAdRequestForm(FlaskForm):
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    submit = SubmitField('Negotiate')

class SearchPublicCampaignForm(FlaskForm):
    niche = StringField('Niche')
    submit = SubmitField('Search')
