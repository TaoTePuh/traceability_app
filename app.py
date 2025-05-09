from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from flask_migrate import Migrate
from forms import UserForm, ProjectForm, MachineForm, SetupForm
from extensions import db
from models import User, Project, Machine, Setup
from flask import abort

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
            new_user = User(
                username=form.username.data,
                full_name=form.full_name.data,
                remarks=form.remarks.data
            )
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
    # --- Lösch-Logik:
    if request.method == 'POST' and 'delete_project_id' in request.form:
        project_id = request.form['delete_project_id']
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            flash(f'Projekt „{project.name}“ erfolgreich gelöscht.')
        else:
            flash('Projekt nicht gefunden.')
        return redirect(url_for('manage_projects'))
    if form.validate_on_submit():
        existing_project = Project.query.filter_by(name=form.name.data).first()
        if existing_project:
            flash('Projekt existiert bereits.')
        else:
            new_project = Project(
                name=form.name.data,
                description=form.description.data,
                remarks=form.remarks.data
            )
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
    # --- Lösch-Logik:
    if request.method == 'POST' and 'delete_machine_id' in request.form:
        machine_id = request.form['delete_machine_id']
        machine = Machine.query.get(machine_id)
        if machine:
            db.session.delete(machine)
            db.session.commit()
            flash(f'Maschine „{machine.name}“ erfolgreich gelöscht.')
        else:
            flash('Maschine nicht gefunden.')
        return redirect(url_for('manage_machines'))
    if form.validate_on_submit():
        existing_machine = Machine.query.filter_by(name=form.name.data).first()
        if existing_machine:
            flash('Maschine existiert bereits.')
        else:
            new_machine = Machine(
                name=form.name.data,
                description=form.description.data,
                remarks=form.remarks.data
            )
            db.session.add(new_machine)
            db.session.commit()
            flash('Maschine erfolgreich angelegt.')
            if form.submit_redirect.data:
                return redirect(url_for('index', selected_machine=new_machine.id))
            elif form.submit_stay.data:
                return redirect(url_for('manage_machines', selected_machine=new_machine.id))
    machines = Machine.query.order_by(Machine.name).all()
    return render_template('manage_machines.html', form=form, machines=machines)

@app.route('/setups', methods=['GET', 'POST'])
def manage_setups():
    form = SetupForm()
    # --- Lösch-Logik:
    if request.method == 'POST' and 'delete_setupd_id' in request.form:
        setup_id = request.form['delete_setup_id']
        setup = Setup.query.get(setup_id)
        if setup:
            db.session.delete(setup)
            db.session.commit()
            flash(f'Setup „{setup.name}“ erfolgreich gelöscht.')
        else:
            flash('Setup nicht gefunden.')
        return redirect(url_for('manage_setups'))
    if form.validate_on_submit():
        existing_setup = Setup.query.filter_by(name=form.name.data).first()
        if existing_setup:
            flash('Ssetup existiert bereits.')
        else:
            new_setup = Setup(
                benutzer_id  = form.benutzer.data,
                projekt_id   = form.projekt.data,
                maschine_id  = form.maschine.data,
                name         = form.name.data,
                bemerkungen  = form.bemerkungen.data
            )
            db.session.add(new_setup)
            db.session.commit()
            flash('Setup erfolgreich angelegt.', 'success')
            if form.submit_redirect.data:
                return redirect(url_for('index', selected_setup=new_setup.id))
            elif form.submit_stay.data:
                return redirect(url_for('manage_setups', selected_setup=new_setup.id))
    setups = Setup.query.order_by(Setup.name).all()
    return render_template('manage_setups.html', form=form, setups=setups)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # 1) Lade bestehenden Benutzer oder 404-Fehler
    user = User.query.get_or_404(user_id)

    # 2) Fülle das Formular mit den aktuellen Werten
    form = UserForm(obj=user)

    # 3) Bei Absenden: prüfen, ob der neue Username schon belegt ist,
    #    und ansonsten speichern
    if form.validate_on_submit():
        collision = User.query.filter_by(username=form.username.data).first()
        if collision and collision.id != user.id:
            flash('Ein anderer Benutzer mit diesem Namen existiert bereits.')
        else:
            user.username  = form.username.data
            user.full_name = form.full_name.data
            user.remarks   = form.remarks.data
            db.session.commit()
            flash('Benutzerdaten erfolgreich aktualisiert.')
            return redirect(url_for('manage_users'))

    # 4) GET-Request oder fehlerhafte Eingaben: Formular anzeigen
    return render_template('edit_user.html', form=form, user=user)

@app.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        collision = Project.query.filter_by(name=form.name.data).first()
        if collision and collision.id != project.id:
            flash('Ein anderes Projekt mit diesem Namen existiert bereits.')
        else:
            project.name        = form.name.data
            project.description = form.description.data
            project.remarks     = form.remarks.data
            db.session.commit()
            flash('Projektdaten erfolgreich aktualisiert.')
            return redirect(url_for('manage_projects'))
    return render_template('edit_project.html', form=form, project=project)

@app.route('/maschinen/edit/<int:machine_id>', methods=['GET', 'POST'])
def edit_machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    form = MachineForm(obj=machine)
    if form.validate_on_submit():
        collision = Machine.query.filter_by(name=form.name.data).first()
        if collision and collision.id != machine.id:
            flash('Eine andere Maschine mit diesem Namen existiert bereits.')
        else:
            machine.name        = form.name.data
            machine.description = form.description.data
            machine.remarks     = form.remarks.data
            db.session.commit()
            flash('Maschinendaten erfolgreich aktualisiert.')
            return redirect(url_for('manage_machines'))
    return render_template('edit_machine.html', form=form, machine=machine)

@app.route('/setups/edit/<int:setup_id>', methods=['GET', 'POST'])
def edit_setup(setup_id):
    setup = Setup.query.get_or_404(setup_id)
    form = SetupForm(obj=setup)
    if form.validate_on_submit():
        collision = Setup.query.filter_by(name=form.name.data).first()
        if collision and collision.id != setup.id:
            flash('Eine anderees Setup mit diesem Namen existiert bereits.')
        else:
            benutzer_id  = form.benutzer.data
            projekt_id   = form.projekt.data
            maschine_id  = form.maschine.data
            name         = form.name.data
            bemerkungen  = form.bemerkungen.data
            db.session.commit()
            flash('Setup erfolgreich aktualisiert.')
            return redirect(url_for('manage_setups'))
    return render_template('edit_setup.html', form=form, setup=setup)

@app.route('/setups/<int:setup_id>/delete', methods=['POST'])
def delete_setup(setup_id):
    setup = Setup.query.get_or_404(setup_id)
    db.session.delete(setup)
    db.session.commit()
    flash(f"Setup «{setup.name}» gelöscht.", "success")
    return redirect(url_for('manage_setups'))

if __name__ == '__main__':
    app.run(debug=True)
