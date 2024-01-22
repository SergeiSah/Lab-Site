from plugins import login_manager
from models import User
from app import create_app
from forms import LoginForm


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def global_variables():
    login_form = LoginForm()
    return dict(login_form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
