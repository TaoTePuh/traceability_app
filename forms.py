from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from models import User, Project, Machine

class UserForm(FlaskForm):
    username        = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    full_name       = StringField('Vollständiger Name', validators=[Length(max=120)])
    remarks         = StringField('Bemerkungen', validators=[Length(max=256)])
    submit_redirect = SubmitField('Benutzer anlegen und auswählen')
    submit_stay     = SubmitField('Benutzer anlegen und weitere anlegen')

class ProjectForm(FlaskForm):
    name            = StringField('Projektname', validators=[DataRequired(), Length(min=1, max=128)])
    description     = StringField('Beschreibung', validators=[Length(max=256)])
    remarks         = StringField('Bemerkungen', validators=[Length(max=256)])
    submit_redirect = SubmitField('Projekt anlegen und auswählen')
    submit_stay     = SubmitField('Projekt anlegen und weitere anlegen')

class MachineForm(FlaskForm):
    name            = StringField('Maschinenname', validators=[DataRequired(), Length(min=1, max=128)])
    description     = StringField('Beschreibung', validators=[Length(max=256)])
    remarks         = StringField('Bemerkungen', validators=[Length(max=256)])
    submit_redirect = SubmitField('Maschine anlegen und auswählen')
    submit_stay     = SubmitField('Maschine anlegen und weitere anlegen')

class SetupForm(FlaskForm):
    benutzer        = SelectField('Benutzer',   coerce=int, validators=[DataRequired()])
    projekt         = SelectField('Projekt',    coerce=int, validators=[DataRequired()])
    maschine        = SelectField('Maschine',   coerce=int, validators=[DataRequired()])
    name            = StringField('Setup-Name', validators=[DataRequired()])
    bemerkungen     = TextAreaField('Bemerkungen')
    submit_redirect = SubmitField('Setup anlegen und auswählen')
    submit_stay     = SubmitField('Setup anlegen und weitere anlegen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Choices laden, analog zu anderen Formen
        self.benutzer.choices = [(u.id, u.username) for u in User.query.order_by(User.username)]
        self.projekt.choices  = [(p.id, p.name)     for p in Project.query.order_by(Project.name)]
        self.maschine.choices = [(m.id, m.name)     for m in Machine.query.order_by(Machine.name)]


