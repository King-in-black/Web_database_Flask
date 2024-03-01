from flask import Blueprint, request, jsonify,redirect,render_template,url_for
from flask import flash
from ..models import Player,Trainer,Data
from ..schemas import Player_Schema,Trainer_Schema,Data_Schema

webpage_bp = Blueprint("webpage", __name__)
@webpage_bp.route('/homepage', methods=['GET', 'POST'])
# a homepage for the webapp
def homepage():
    '''
    when the user starts, they would like to starts from here to choose whether to login or register
    :return: the html which responsible for the homepage
    '''
    if request.method == 'POST':
        action = request.form.get('action')
        # according to the value of action, the page will redirect to another page.
        if action == 'login':
            # if the use types the button for login; they will jump to login page
            return redirect(url_for('login'))
        elif action == 'register':
            # or they will jump to register page
            return redirect(url_for('register'))
        else:
            jsonify('Invalid action', 400)
    return render_template('homepage.html')

@webpage_bp.route('/register', methods=['GET', 'POST'])
def register():
    '''
    allow people to register account in player identification or a trainer identification
    :return:
    if the user registers successfully, the user will jump into the login page;
    or they will return a 404 error
    '''
    if request.method == 'POST':
        player_id = request.form['Player_ID']
        trainer_id = request.form['Trainer_ID']
        password = request.form['password']
        role = request.form['role']

        if role == 'player':
            # the db will be asked to check whether there is a player ID
            existing_user = Player.query.filter_by(Player_ID=player_id).first()
            if existing_user:
            # if the player exists, the 404 error will return
                abort(404, description="Player already exists.")
            # or a Player instance will be asked to create in the database
            new_user = Player(Player_ID=player_id, password=password, Trainer_ID=trainer_id)
            db.session.add(new_user)
        elif role == 'trainer':
            # Check whether there is a player exists or not
            existing_user = Trainer.query.filter_by(Trainer_ID=trainer_id).first()
            if existing_user:
            # if the trainer exists, the 404 error will return
                abort(404, description="Trainer already exists.")
            # or a Trainer instance will be asked to create in the database
            new_user = Trainer(Trainer_ID=trainer_id, password=password)
            db.session.add(new_user)
        else:
            flash('Please select a valid role', 'error')
            return render_template('register.html')

        db.session.commit()  # submit the changes in the database
        # jump to login page if a user register successfully
        return redirect(url_for('login'))

    return render_template('register.html')


@webpage_bp.route('/login',methods=['GET', 'POST'])
def login():
    '''
    the login page allows users to check records of existing players and trainers.
    if the password and ID are correct, they could access the following applications
    :returns: the following pages have not completed.
    '''
    if request.method == 'POST':
        # extract the information of the players or the trainers
        role = request.form['role']
        user_id = request.form.get('user_id')
        password = request.form['password']

        if role == 'player':
            # if the user is player, the database will be asked for certain records of the player
            # if the password and the ID of the form requested match with records in the database
            # login page passed
            user = Player.query.filter_by(Player_ID=user_id, password=password).scalarone()
            if user:
                # when the player login successfully, the following steps will be inplemented
                flash('Player login successful!', 'success')
                return redirect(url_for('player_dashboard'))  # incomplete player page for prediction the result
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Player ID or password', 'error')

        elif role == 'trainer':
            # when the trainer login successfully, the following steps will be inplemented
            user = Trainer.query.filter_by(Trainer_ID=user_id, password=password).scalarone()
            if user:
                # when the trainer login successfully, the following steps will be inplemented
                flash('Trainer login successful!', 'success')
                return redirect(url_for('trainer_dashboard'))  # incomplete trainer page for upload the results
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Trainer ID or password', 'error')

    return render_template('login.html')
