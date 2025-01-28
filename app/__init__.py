from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    db.init_app(app)

    with app.app_context():

        from .models import Student, Team 

        db.create_all()

        if not Student.query.first(): 
            students = [
                {"first_name": "Maxime", "last_name": "SEMARD", "student_number": "40001105", "school": "ESIROI", "email": "m.semard@rt-iut.re"},
                {"first_name": "Gabriele", "last_name": "PIANA", "student_number": "41001145", "school": "ESIROI", "email": "gabrielepiana03@gmail.com"},
                {"first_name": "Joé", "last_name": "PAYET", "student_number": "42001022", "school": "ESIROI", "email": "payet.joe.teo@gmail.com"},
                {"first_name": "Logan", "last_name": "GRONDIN", "student_number": "42000882", "school": "ESIROI", "email": "logan.grondin@esiroi.re"},
                {"first_name": "Eric", "last_name": "FORSTER", "student_number": "42002932", "school": "ESIROI", "email": "eric.forster@esiroi.re"},
                {"first_name": "Lukas", "last_name": "DAMOUR", "student_number": "42001314", "school": "ESIROI", "email": "lukas.damour@esiroi.re"},
                {"first_name": "Raphael", "last_name": "SOUPAYA VALLIAMA", "student_number": "41006093", "school": "ESIROI", "email": "raphael.soupayavalliama@gmail.com"},
                {"first_name": "Mohammad Youssouf", "last_name": "ONIAN", "student_number": "42001046", "school": "ESIROI", "email": "youssoufonian@gmail.com"},
                {"first_name": "Jade Pearl", "last_name": "GONTHIER", "student_number": "42000784", "school": "ESIROI", "email": "jade.gonthier@esiroi.re"},
                {"first_name": "Sylvain", "last_name": "FONTAINE", "student_number": "43000048", "school": "ESIROI", "email": "sylvain.fontaine@esiroi.re"},
                {"first_name": "Vincent", "last_name": "POUDROUX", "student_number": "41002413", "school": "ESIROI", "email": "Vincentpoudroux2@gmail.com"},
                {"first_name": "Loïc", "last_name": "FONTAINE", "student_number": "41004199", "school": "ESIROI", "email": "loicfo73@gmail.com"},
                {"first_name": "Maeva", "last_name": "MAMPIONO", "student_number": "42000158", "school": "ESIROI", "email": "maeva.mampiono@esiroi.re"},
                {"first_name": "Mathias", "last_name": "ALY-BERIL", "student_number": "42000737", "school": "ESIROI", "email": "alyderil.mathias@gmail.com"},
                {"first_name": "Lise", "last_name": "ROCHAT (Gardien de la nuit)", "student_number": "43007365", "school": "ESIROI", "email": "rochatlise17@gmail.com"},
                {"first_name": "Davidra", "last_name": "ANDRIAMISAINA (Gardien de la nuit)", "student_number": "43007563", "school": "ESIROI", "email": "afantarina@gmail.com"},
                {"first_name": "Alexia", "last_name": "GAIDO--AMOROS", "student_number": "41004795", "school": "ESIROI", "email": "41004795@co.univ-reunion.fr"},
                {"first_name": "Matéo", "last_name": "VITRY", "student_number": "42001007", "school": "ESIROI", "email": "mateo.vitry@esiroi.re"},
                {"first_name": "Benjamin", "last_name": "VITRY", "student_number": "44000559", "school": "ESIROI", "email": "vitry.benjamin11@gmail.com"},
                {"first_name": "Toan", "last_name": "METAS", "student_number": "42002609", "school": "ESIROI", "email": "metastoan@gmail.com"},
                {"first_name": "Roxane", "last_name": "COULON--PARAME", "student_number": "44003980", "school": "ESIROI", "email": "sibairattack@gmail.com"},
                {"first_name": "Roger Marius", "last_name": "RAZAFINDRABETANY", "student_number": "44006134", "school": "ESIROI", "email": "rrazafindrabetany@esiroi.re"},
                {"first_name": "Corentin", "last_name": "RASDA", "student_number": "36000793", "school": "FAC ST Denis", "email": "rasdacorentin@gmail.com"},
                {"first_name": "Tahiry", "last_name": "NOURDINE", "student_number": "39005886", "school": "FAC ST Denis", "email": "nourdine.tahiry@gmail.com"},
                {"first_name": "Mahé", "last_name": "BEGNIS", "student_number": "43005970", "school": "ESIROI", "email": "mahe.begnis@esiroi.re"},
            ]
            for student in students:
                new_student = Student(
                    first_name=student["first_name"],
                    last_name=student["last_name"],
                    student_number=student["student_number"],
                    school=student["school"],
                    email=student["email"],
                    team_id=None  
                )
                db.session.add(new_student)
            db.session.commit()

    # Enregistre le Blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
