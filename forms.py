from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

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
    # Pulldowns: coerce=int, damit wir direkt mit IDs arbeiten
    benutzer       = SelectField('Benutzer',   coerce=int, validators=[DataRequired()])
    projekt        = SelectField('Projekt',    coerce=int, validators=[DataRequired()])
    maschine       = SelectField('Maschine',   coerce=int, validators=[DataRequired()])

    setupname      = StringField('Setupname', validators=[DataRequired()])
    bemerkungen    = TextAreaField('Bemerkungen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Choices beim Form-Init laden
        self.benutzer.choices = [(b.id, b.name) for b in Benutzer.query.order_by(Benutzer.name)]
        self.projekt.choices  = [(p.id, p.name) for p in Projekt.query.order_by(Projekt.name)]
        self.maschine.choices = [(m.id, m.name) for m in Maschine.query.order_by(Maschine.name)]
