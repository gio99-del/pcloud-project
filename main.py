from flask import Flask, request, redirect, url_for, render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from google.cloud import firestore
import json
# import secrets    -   print(secrets.token_hex())


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY='847931b776cc93c2d31bd871f5d0fb00d1e431a84165813646f57f521b0308e4'
)

login_manager = LoginManager(app)
# By default, when a user attempts to access a login_required view without being logged in, Flask-Login will flash a
# message and redirect them to the log in view
login_manager.login_view = '/static/login.html'
login_manager.login_message = "Non è stato possibile accedere alla pagina. Effettuare il login."

db = firestore.Client.from_service_account_json('credentials.json', database='pcloud')
coll = 'Denver Crime Data'

userdb = {
    'gio@ab.xy': 'ds'
}


# Callback to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(username):
    if username in userdb:
        return User(username)
    return None


@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('static', filename='index.html'))
    return redirect(url_for('static', filename='login.html'))


@app.route('/client', methods=['GET'])
def client():
    db_len = 0
    # Calling 'db_length' document, the database query is only one.
    # Otherwise is necessary to count every document in the database, so n queries.
    try:
        doc_ref = db.collection(coll).document('db_length')
        doc = doc_ref.get().to_dict()
        db_len = doc['value']
    except:
        print('db_length was not found')
    return str(db_len)


@app.route('/main', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('static', filename='index.html'))


@app.route('/static/index.html', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('static', filename='index.html'))


@app.route('/static/graphs.html', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('static', filename='graphs.html'))


@app.route('/static/maps.html', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('static', filename='maps.html'))


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('static', filename='index.html'))
    username = request.values['email']
    password = request.values['pass']
    if username in userdb and password == userdb[username]:
        login_user(User(username))
        next_page = '/main'
        return redirect(next_page)
    return redirect(url_for('static', filename='login.html'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        r = []
        for entity in db.collection(coll).stream():
            if not entity.id == 'db_length':
                r.append(entity.to_dict())
        return json.dumps(r), 200
    else:
        dct = request.values
        dk = list(dct.keys())

        try:
            doc_ref = db.collection(coll).document('db_length')
            db_len = doc_ref.get().to_dict()['value']
            doc_ref.update({'value': db_len+1})
        except:
            print('db_length was not found')
            db.collection(coll).document('db_length').set({'value': 1})

        i = 0
        for k in dk:
            doc_ref = db.collection(coll).document(dct['incident_id'])
            if i == 0:
                doc_ref.set({k: dct[k]})
            else:
                doc_ref.update({k: dct[k]})
            i += 1
        return 'ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

