from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from .models import Student, Team
from . import db
import io

# Crée un Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'POST':
        action = request.form.get('action') 

        # Création d'une équipe
        if action == 'create':
            # Vérifie le nombre d'équipes existantes
            if Team.query.count() >= 3:
                flash('Le nombre maximum de trois équipes a été atteint.')
                return redirect(url_for('main.teams'))

            team_name = request.form.get('team_name')
            leader_id = request.form.get('leader_id')

            # Vérifie que le nom de l'équipe est unique
            if Team.query.filter_by(name=team_name).first():
                flash('Ce nom d’équipe est déjà pris.')
                return redirect(url_for('main.teams'))

            # Vérifie que l'étudiant sélectionné n'est pas déjà dans une équipe
            leader = Student.query.get(leader_id)
            if not leader or leader.team_id is not None:
                flash('Cet étudiant est déjà assigné à une équipe.')
                return redirect(url_for('main.teams'))

            # Crée l'équipe
            team = Team(name=team_name, leader_id=leader.id)
            db.session.add(team)

            # Marque l'étudiant comme chef de l'équipe
            leader.team_id = team.id
            db.session.commit()

            flash(f"Équipe '{team_name}' créée avec succès !")
            return redirect(url_for('main.teams'))

        # Ajouter un étudiant à une équipe
        elif action == 'join':
            team_id = request.form.get('team_id')
            student_id = request.form.get('student_id')

            # Vérifie que l'équipe existe
            team = Team.query.get(team_id)
            if not team:
                flash("Équipe non trouvée.")
                return redirect(url_for('main.teams'))

            # Vérifie que l'équipe n'a pas atteint 20 membres
            if len(team.members) >= 20:
                flash("Cette équipe a atteint la limite maximale de 20 membres.")
                return redirect(url_for('main.teams'))

            # Vérifie que l'étudiant n'est pas déjà assigné à une équipe
            student = Student.query.get(student_id)
            if not student or student.team_id is not None:
                flash('Cet étudiant est déjà assigné à une équipe.')
                return redirect(url_for('main.teams'))

            # Ajoute l'étudiant à l'équipe
            student.team_id = team.id
            db.session.commit()

            flash(f"{student.first_name} a rejoint l’équipe {team.name} !")
            return redirect(url_for('main.teams'))

    # Récupère les IDs des chefs d'équipe
    leaders_ids = [team.leader_id for team in Team.query.all()]

    # Récupère uniquement les étudiants sans équipe ET qui ne sont pas chefs
    available_students = Student.query.filter(
        (Student.team_id == None) & ~Student.id.in_(leaders_ids)
    ).all()

    # Récupère toutes les équipes pour affichage
    all_teams = Team.query.all()

    return render_template('teams.html', teams=all_teams, students=available_students)

@main.route('/program')
def program():
    return render_template('program.html')

@main.route('/download_teams')
def download_teams():
    # Collecte des données des équipes et des étudiants
    teams = Team.query.all()
    output = io.StringIO()
    
    for team in teams:
        output.write(f"Équipe : {team.name}\n")
        output.write(f"Chef d'équipe : {team.leader.first_name} {team.leader.last_name} {team.leader.student_number} {team.leader.school} {team.leader.email}\n")
        output.write("Membres :\n")
        
        for member in team.members:
            output.write(
                f"- Nom : {member.first_name} {member.last_name}, "
                f"Numéro étudiant : {member.student_number}, "
                f"École : {member.school}, "
                f"Email : {member.email}\n"
            )
        
        output.write("\n") 
    
    # Prépare la réponse Flask pour le téléchargement
    response = Response(output.getvalue(), mimetype="text/plain")
    response.headers["Content-Disposition"] = "attachment; filename=teams_info.txt"
    return response
