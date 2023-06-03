from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, SignupForm, ChangePwdForm
from .models import db, User, Theme, Answer, UserProgress


def index_page():
	#query = db.select(Theme)
	themes = db.session.query(Theme).all() #db.session.execute(query).scalars()
	completed = []
	themes_len = db.session.query(Theme).count()
	if current_user.is_authenticated:
		completed = [up.theme.id for up in UserProgress.query.filter_by(user_id=current_user.id, is_complete=True)]
	progress = int(100*len(completed)/themes_len) if themes_len > 0 else 0
	return render_template("index.html", themes=themes, completed=completed, progress=progress)

def theme_page(theme_id):
	print(current_user.is_authenticated)
	if not current_user.is_authenticated:
		flash('Материалы доступны только для зарегистрированных пользователей!')
		return redirect(url_for('index_page'))
	theme = Theme.query.get_or_404(theme_id)
	if request.method == "POST":
		count = 0
		for question in theme.questions:
			if str(question.id) in request.form:
				if question.question_type.name == 'Выбор':
					answer = Answer.query.get(request.form[str(question.id)])
					count += int(answer.is_correct)
				else:
					answer = Answer.query.filter_by(question_id=question.id).first()
					count += int(answer.text == request.form[str(question.id)])
		progress = UserProgress.query.filter_by(user_id=current_user.id, theme_id=theme.id).first()
		if progress == None:
			progress = UserProgress()
			progress.user_id = current_user.id
			progress.theme_id = theme.id
			progress.is_complete = count >= theme.pass_criteria
			db.session.add(progress)
		else:
			progress.is_complete = count >= theme.pass_criteria
		db.session.commit()
		message = "Поздравляем! Вы успешно справились и тестом. Можете перейти к следующей теме!" if count >= theme.pass_criteria else "Повторите материал и попробуйте еще раз."
		return render_template(theme.page, theme=theme, count=count, message=message)

	return render_template(theme.page, theme=theme)

def add_theme():
	form = None
	if request.method == "POST":
		return redirect(url_for("index_page"))
	return render_template("add_theme.html", form=form)

def profile():
	if not current_user.is_authenticated:
		flash('Вы не авторизованы!')
		return redirect(url_for('index_page'))
	message = None
	query = db.session.query(UserProgress.theme_id).filter(UserProgress.user_id==current_user.id, UserProgress.is_complete==True)
	completed_ids = list(db.session.execute(query).scalars())
	query = db.session.query(Theme).filter(Theme.id.in_(completed_ids))
	completed = db.session.execute(query).scalars()
	query = db.session.query(Theme).filter(Theme.id.notin_(completed_ids))
	notcompleted = db.session.execute(query).scalars()
	form = ChangePwdForm()
	if request.method == "POST":
		if form.validate_on_submit():
			if form.password.data == form.confirmation.data:
				current_user.pwd = form.password.data
				db.session.commit()
				flash('Пароль был успешно изменен!')
				return redirect(url_for('profile'))
	return render_template("profile.html", completed=completed, notcompleted=notcompleted, form=form, message=message)

def signup():
	form=SignupForm()
	if request.method == "POST":
		if form.validate_on_submit():
			if form.password.data == form.confirmation.data:
				new_user = User()
				new_user.fio = form.fio.data
				new_user.username = form.username.data
				new_user.pwd = form.password.data
				new_user.email = form.email.data
				db.session.add(new_user)
				db.session.commit()
				login_user(new_user)
				return redirect(url_for("index_page"))
			else:
				flash("Пароли не совпадают!")
	return render_template("sign_up.html", form=form)


def login_page():
	form = LoginForm()
	if request.method == "POST":
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()
			if user is not None and user.pwd == form.password.data:
				login_user(user)
				next = request.args.get("next")
				return redirect(url_for("index_page"))
			else:
				flash('Логин или пароль не верен!')
				return redirect(url_for('login_page'))

	return render_template("login.html", form=form)

def logout():
	logout_user()
	return redirect(url_for("index_page"))
