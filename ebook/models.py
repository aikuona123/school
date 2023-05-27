from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(250), nullable=False, default="", server_default="")
    username = db.Column(db.String(25), nullable=False, unique=True)
    pwd = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(150), nullable=False, server_default="", default="")
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    themes_complete = db.relationship("UserProgress", back_populates="user")

    def __str__(self):
        return self.username


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    page = db.Column(db.String(150), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("theme.id", name="Theme"))
    sub_themes = db.relationship("Theme")
    questions = db.relationship("Question", back_populates="theme")
    pass_criteria = db.Column(db.Integer, nullable=False, default=0, server_default='0')

    def __str__(self):
        return self.name


class QuestionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type_id = db.Column(db.Integer, db.ForeignKey("question_type.id", name="QuestionType"))
    question_type = db.relationship("QuestionType")
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id", name="Theme"))
    theme = db.relationship("Theme", back_populates="questions")
    text = db.Column(db.Text)
    answers = db.relationship("Answer", back_populates="question")
    
    def __str__(self):
        return self.text[:25]


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", name="Question"))
    question = db.relationship("Question", back_populates="answers")
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=True)

    def __str__(self):
        return self.text


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="User"))
    user = db.relationship("User", back_populates="themes_complete")
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id", name="Theme"))
    theme = db.relationship("Theme")
    is_complete = db.Column(db.Boolean, nullable=False, default=True)

    def __str__(self):
        return f"{self.id}: {self.user_id} - {self.theme_id}"
