from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from flask_migrate import Migrate
from forms import UserForm, ProjectForm, MachineForm
from extensions import db
from models import User, Project, Machine

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.context_processor
def inject_common_data():
    users = User.query.order_by(User.username).all()
    projects = Project.query.order_by(Project.name).all()
    machines = Machine.query.order_by(Machine.name).all()
    
    # Lies Werte aus GET-Parameter oder der Session
    selected_user = request.args.get('selected_user') or session.get('selected_user')
    selected_project = request.args.get('selected_project') or session.get('selected_project')
    selected_machine = request.args.get('selected_machine') or session.get('selected_machine')
    
    # Speichere in der Session, falls vorhanden
    if selected_user:
        session['selected_user'] = selected_user
    if selected_project:
        session['selected_project'] = selected_project
    if selected_machine:
        session['selected_machine'] = selected_machine

    try:
        selected_user = int(selected_user) if selected_user else None
    except (ValueError, TypeError):
        selected_user = None
    try:
        selected_project = int(selected_project) if selected_project else None
    except (ValueError, TypeError):
        selected_project = None
    try:
        selected_machine = int(selected_machine) if selected_machine else None
    except (ValueError, TypeError):
        selected_machine = None

    return dict(users=users, selected_user=selected_user,
                projects=projects, selected_project=selected_project,
                machines=machines, selected_machine=selected_machine)


@app.route('/')
def index():
    # Deine Hauptseite – greift auf selected_user via context_processor zu
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    form = UserForm()
    # --- Lösch-Logik:
    if request.method == 'POST' and 'delete_user_id' in request.form:
        user_id = request.form['delete_user_id']
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f'Benutzer "{user.username}" erfolgreich gelöscht.')
        else:
            flash('Benutzer nicht gefunden.')
        # Nach dem Löschen zurück auf die Verwaltungsseite
        return redirect(url_for('manage_users'))
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Benutzer existiert bereits.')
        else:
            new_user = User(username=form.username.data, full_name=form.full_name.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Benutzer erfolgreich angelegt.')
            # Unterscheiden, welcher Button geklickt wurde
            if form.submit_redirect.data:
                # Weiterleitung zur Startseite, damit der neue Benutzer im Dropdown vorausgewählt wird
                return redirect(url_for('index', selected_user=new_user.id))
            elif form.submit_stay.data:
                # Bleibt in der Benutzerverwaltung. Optional: Übergabe der neuen Benutzer-ID,
                # falls du das Dropdown auch in der Verwaltung aktualisieren möchtest.
                return redirect(url_for('manage_users', selected_user=new_user.id))
    users = User.query.order_by(User.username).all()
    return render_template('manage_users.html', form=form, users=users)


@app.route('/projects', methods=['GET', 'POST'])
def manage_projects():
    form = ProjectForm()
    if form.validate_on_submit():
        existing_project = Project.query.filter_by(name=form.name.data).first()
        if existing_project:
            flash('Projekt existiert bereits.')
        else:
            new_project = Project(name=form.name.data, description=form.description.data)
            db.session.add(new_project)
            db.session.commit()
            flash('Projekt erfolgreich angelegt.')
            if form.submit_redirect.data:
                # Bei "Projekt anlegen und auswählen" leiten wir zur Indexseite weiter.
                return redirect(url_for('index', selected_project=new_project.id))
            elif form.submit_stay.data:
                # Bei "Projekt anlegen und weitere anlegen" bleiben wir auf der Verwaltungsseite.
                return redirect(url_for('manage_projects', selected_project=new_project.id))
    projects = Project.query.order_by(Project.name).all()
    return render_template('manage_projects.html', form=form, projects=projects)


@app.route('/maschinen', methods=['GET', 'POST'])
def manage_machines():
    form = MachineForm()
    if form.validate_on_submit():
        existing_machine = Machine.query.filter_by(name=form.name.data).first()
        if existing_machine:
            flash('Maschine existiert bereits.')
        else:
            new_machine = Machine(name=form.name.data, description=form.description.data)
            db.session.add(new_machine)
            db.session.commit()
            flash('Maschine erfolgreich angelegt.')
            if form.submit_redirect.data:
                return redirect(url_for('index', selected_machine=new_machine.id))
            elif form.submit_stay.data:
                return redirect(url_for('manage_machines', selected_machine=new_machine.id))
    machines = Machine.query.order_by(Machine.name).all()
    return render_template('manage_machines.html', form=form, machines=machines)


if __name__ == '__main__':
    app.run(debug=True)
