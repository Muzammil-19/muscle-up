import datetime

from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://pvyjcmwrytnrho:bd8af00d8230687db210eeb7cc6dde5333d66d7c0817c447e78a0701e32d8530@ec2-23-20-140-229.compute-1.amazonaws.com:5432/d1cdo565mmcu59"
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    phoneno = db.Column(db.Integer)
    email = db.Column(db.String(30))
    joindate = db.Column(db.String(11))
    startdate = db.Column(db.String(11))
    enddate = db.Column(db.String(11))
    address = db.Column(db.String(100))
    status = db.Column(db.String(10))
    training = db.Column(db.String(10))
    amount = db.Column(db.Integer)


class Users(db.Model):
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = Users(name=name, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("New User Created")
        return redirect("/")

    return render_template('register.html')


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     try:
#         if "username" in session:
#             # flash("You have already logged in")
#             return redirect('/')
#         else:
#             if request.method == "POST":
#                 username = request.form['username'].strip()
#                 password = request.form['password'].strip()
#                 data = Users.query.filter_by(username=username).first()
#                 if username == "admin" and password == "admin":
#                     session["username"] = "admin"
#                     return redirect("/")
#                 elif username == data.username and password == data.password:
#                     session["username"] = data.username
#                     return redirect("/")
#                 else:
#                     flash("invalid username/password")
#                     return redirect("/login")
#     except:
#         flash("invalid username/password")
#         return redirect("/login")
#     return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if "username" in session:
        # flash("You have already logged in")
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            data = Users.query.filter_by(username=username).first()
            if username == "admin" and password == "admin":
                session["username"] = "admin"
                return redirect("/")
            elif username == data.username and password == data.password:
                session["username"] = data.username
                return redirect("/")
            else:
                flash("invalid username/password")
                return redirect("/login")
    return render_template("login.html")

@app.route('/logout')
def logout():
    try:
        session.pop('username', None)
        # flash("successfully Logout!","logout")
        return redirect("/")
    except:
        flash("Something went wrong", "error")
        return make_response("something went wrong")


@app.route("/")
def index():
    if "username" not in session:
        # flash("Please log in")
        return render_template("login.html")
    return render_template("index.html")


@app.route("/home")
def home():
    try:
        if "username" not in session:
            flash("Please log in first")
            return redirect('/login')
        return redirect("/")
    except:
        flash("Please login first")
        return render_template("login.html")


@app.route("/table")
def table():

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")

    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    member = Members.query.order_by(Members.id).paginate(page=page, per_page=9)
    total_rows = Members.query.count()
    button_name = "Show All Records"
    path = "/table1"

    return render_template("table.html", member=member, total_rows=total_rows, button_name=button_name, path=path)



@app.route("/table1")
def table1():
    try:
        if "username" not in session:
            flash("Please log in first")
            return render_template("login.html")

        total_rows = Members.query.count()
        # Set the pagination configuration
        page = request.args.get('page', 1, type=int)
        member = Members.query.order_by(Members.id).paginate(page=page, per_page=total_rows)
        button_name = "Show Less Records"
        path = "/table"

        return render_template("table.html", member=member, total_rows=total_rows, button_name=button_name, path=path)
    except:
        return make_response("can't access the table page")


@app.route("/form", methods=['POST', 'GET'])
def form():

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")

    if request.method == 'POST':
        'add entry to db'

        id = request.form.get('id')
        firstname = request.form.get('firstname').strip()
        lastname = request.form.get('lastname').strip()
        phoneno = request.form.get('phoneno').strip()
        email = request.form.get('email').strip()

        # dates
        joindate = request.form.get('joindate')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')

        address = request.form.get('address').strip()
        status = request.form.get('status')
        training = request.form.get('training')
        amount = request.form.get('amount').strip()

        entry = Members(id=id, firstname=firstname, lastname=lastname, phoneno=phoneno, email=email,
                        joindate=joindate, startdate=startdate, enddate=enddate, address=address, status=status,
                        training=training, amount=amount)
        # entry=Members(id=id,firstname=firstname,lastname=lastname,phoneno=phoneno,email=email,
        #               joindate=joindate)
        db.session.add(entry)
        db.session.commit()
        flash(" Member Inserted Successfully ")

    member = Members.query.all()
    return render_template("form.html", member=member[-1])



@app.route("/edit/<int:id>/", methods=['GET', 'POST'])
def edit(id):

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")

    entry = Members.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entry:
            'delete the previous member entry without id'
            db.session.delete(entry)
            db.session.commit()

            'updating the whole record'
            id = request.form.get('id')
            firstname = request.form.get('firstname').strip()
            lastname = request.form.get('lastname').strip()
            phoneno = request.form.get('phoneno').strip()
            email = request.form.get('email').strip()
            joindate = request.form.get('joindate')
            startdate = request.form.get('startdate')
            enddate = request.form.get('enddate')
            address = request.form.get('address').strip()
            status = request.form.get('status')
            training = request.form.get('training')
            amount = request.form.get('amount').strip()

            entry = Members(id=id, firstname=firstname, lastname=lastname, phoneno=phoneno, email=email,
                            joindate=joindate, startdate=startdate, enddate=enddate, address=address, status=status,
                            training=training, amount=amount)


            db.session.add(entry)
            db.session.commit()

            flash("Member Updated Successfully")
            # member = Members.query.all()
            return redirect(url_for('table'))
        return "Id does not exist"

    return render_template("update.html", entry=entry, path="edit", back="table")



@app.route("/delete/<int:id>/", methods=['GET', 'POST'])
def delete(id):

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")

    my_data = Members.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Member Deleted Successfully")

    return redirect(url_for('table'))



@app.route("/expiryTable")
def expiry_table():

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")
    today = datetime.datetime.now().date()
    expire = today + datetime.timedelta(days=2)
    # member = Members.query.filter(Members.enddate <= expire).all()
    total_rows = Members.query.filter(Members.enddate <= expire).count()
    member = Members.query.filter(Members.enddate <= expire).order_by(Members.enddate.desc()).all()
    return render_template('expiryTable.html', member=member, total_rows=total_rows)



@app.route("/editExpiry/<int:id>/", methods=['GET', 'POST'])
def edit_expiry(id):

    if "username" not in session:
        flash("Please log in first")
        return render_template("login.html")

    entry = Members.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entry:
            'delete the previous member entry without id'
            db.session.delete(entry)
            db.session.commit()

            'updating the whole record'
            id = request.form.get('id')
            firstname = request.form.get('firstname').strip()
            lastname = request.form.get('lastname').strip()
            phoneno = request.form.get('phoneno').strip()
            email = request.form.get('email').strip()
            joindate = request.form.get('joindate')
            startdate = request.form.get('startdate')
            enddate = request.form.get('enddate')
            address = request.form.get('address').strip()
            status = request.form.get('status')
            training = request.form.get('training')
            amount = request.form.get('amount').strip()

            entry = Members(id=id, firstname=firstname, lastname=lastname, phoneno=phoneno, email=email,
                            joindate=joindate, startdate=startdate, enddate=enddate, address=address, status=status,
                            training=training, amount=amount)



            db.session.add(entry)
            db.session.commit()

            flash("Member Updated Successfully")

            return redirect(url_for('expiry_table'))
        return "Id does not exist"

    return render_template("update.html", entry=entry, path="editExpiry", back="expiryTable")



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
