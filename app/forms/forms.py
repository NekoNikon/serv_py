from flask_wtf import FlaskForm
from wtforms import TextField  , BooleanField , PasswordField , SelectField , SubmitField , DateField
from wtforms.validators import DataRequired , Email

# TODO create forms for each page and task
# TODO create methods for initializations forms and filed on role

class LoginForm(FlaskForm):
    btn_sbt     = SubmitField("OK" , validators=[DataRequired()])
    text         = TextField("логин"       , validators=[DataRequired() , Email()])
    iin_text     = TextField("ИИН"          , validators=[DataRequired()])
    f_name       = TextField("first name"   , validators=[DataRequired()])
    s_name       = TextField("second name"  , validators=[DataRequired()])
    t_name       = TextField("third name"   , validators=[DataRequired()])
    iin_key_text = TextField("iin"          , validators=[DataRequired()])
    f_name       = TextField("first name"   , validators=[DataRequired()])
    s_name       = TextField("second name"  , validators=[DataRequired()])
    t_name       = TextField("third name"   , validators=[DataRequired()])
    category     = SelectField('Category'   , choices=[('some1' , 'some1_'),('some2' , 'some2_')])
    
    pass_field   = PasswordField("enter a password" , validators=[DataRequired()])
    pass_repeat  = PasswordField("repeat a password" , validators=[DataRequired()])
    pas          = PasswordField("password", validators=[DataRequired()])

class SetRate(FlaskForm):
    submit              = SubmitField('SET')
    select_teacher      = SelectField('select teacher')
    date                = DateField('season')
    value_rate          = TextField('value rate')
    indicator           = SelectField('indicator')

class Forms(FlaskForm):
    select = SelectField('select' , validators=[DataRequired()])

    def init(self):
        self.select.choices=[('her_val' , 'her_text') , ('some_val' , 'some_text')]
        
