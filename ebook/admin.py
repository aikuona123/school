from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from . import models

class Controller(ModelView):

	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def not_auth(self):
		return "Access denied!"


class ThemeView(Controller):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('id', 'name', 'page', 'sub_themes', 'questions', 'pass_criteria')

class QuestionView(Controller):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('id', 'text', 'page', 'question_type', 'theme', 'answers')

class AnswerView(Controller):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('id', 'question', 'text', 'is_correct')

class UserProgressView(Controller):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('id', 'user', 'theme', 'is_complete')

session = models.db.session

admin = Admin()
admin.add_view(Controller(models.User, session))
admin.add_view(ThemeView(models.Theme, session))
admin.add_view(Controller(models.QuestionType, session))
admin.add_view(QuestionView(models.Question, session))
admin.add_view(AnswerView(models.Answer, session))
admin.add_view(UserProgressView(models.UserProgress, session))
