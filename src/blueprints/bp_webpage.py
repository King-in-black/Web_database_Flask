from flask import Blueprint, request, jsonify,redirect,render_template,url_for,abort
from flask import flash
import os
from ..models import Player,Trainer,Data
from ..schemas import Player_Schema,Trainer_Schema,Data_Schema
from ..extension import db
import pickle
import math
import warnings
warnings.filterwarnings("ignore", message="Trying to unpickle estimator", module="sklearn.base")
model_path = os.path.join(os.path.dirname(__file__), '..', 'ML_models', 'random_forest_model.pkl')
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)
webpage_bp = Blueprint("webpage", __name__)
@webpage_bp.route('/', methods=['GET', 'POST'])
def jump_homepage():
    '''
    :return: jump to the homepage url
    '''
    return redirect(url_for('webpage.homepage'))
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
            return redirect(url_for('webpage.login'))
        elif action == 'register':
            # or they will jump to register page
            return redirect(url_for('webpage.register'))
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
        return redirect(url_for('webpage.login'))

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
            user = Player.query.filter_by(Player_ID=user_id, password=password).scalar()
            if user:
                # when the player login successfully, the following steps will be inplemented
                flash('Player login successful!', 'success')
                return  redirect(url_for('webpage.predict'))  # incomplete player page for prediction the result
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Player ID or password', 'error')

        elif role == 'trainer':
            # when the trainer login successfully, the following steps will be inplemented
            user = Trainer.query.filter_by(Trainer_ID=user_id, password=password).scalar()
            if user:
                # when the trainer login successfully, the following steps will be inplemented
                flash('Trainer login successful!', 'success')
                return  redirect(url_for('webpage.predict'))
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Trainer ID or password', 'error')

    return render_template('login.html')

@webpage_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    '''
    allow users to upload the data to ask  whether a person is moving;
    if format is correct, the webpage will direct to predict page.
    return:
          the html template of the prediction page
    '''
    # initialize the prediction
    prediction = None
    Move = None
    Resultant_Acc=None
    Resultant_Gyro=None
    if  request.method == 'POST':
        try:
            accX = float(request.form.get('accX'))
            accY = float(request.form.get('accY'))
            accZ = float(request.form.get('accZ'))
            gyroX = float(request.form.get('gyroX'))
            gyroY = float(request.form.get('gyroY'))
            gyroZ = float(request.form.get('gyroZ'))
        except ValueError:
            return jsonify({"error": "Invalid input. Please ensure all values are numbers."}), 400
        player_id = request.form.get('Player_ID')
        trainer_id = request.form.get('Trainer_ID')
        if not accX or not accY or not accZ or not gyroX or not gyroY or not gyroZ or not player_id or not  trainer_id:
            flash('All forms are required to be filled!')
            # render template again
            return render_template('predict.html',prediction=prediction, Move=Move)
        else:
            # use the model to predict
            prediction = float(model.predict([[accX, accY, accZ, gyroX, gyroY, gyroZ]]))
            Resultant_Acc = math.sqrt(accX ** 2 + accY ** 2 + accZ ** 2)
            Resultant_Gyro = math.sqrt(gyroX ** 2 + gyroY ** 2 + gyroZ ** 2)
            # add a deterministic method to mimic the behaviour of prediction = 0
            if Resultant_Acc and Resultant_Gyro < 0.5:
                prediction = 0
            if prediction < 0.5:
                Activity = 0
                Move = 'Stationary'
            else:
                Activity = 1
                Move = 'Moving'
            # write the data into the database.
            data = Data(Player_ID=player_id, Trainer_ID=trainer_id, accX=accX, accY=accY, accZ=accZ, gyroX=gyroX,
                        gyroY=gyroY, gyroZ=gyroZ, Activity=Activity, Resultant_Acc=Resultant_Acc,
                        Resultant_Gyro=Resultant_Gyro)
            # summit the data row
            db.session.add(data)
        # when activity is labeled as 1 means that the person is moving; the activity is labeled as 0 when the person is
        # stationary

    # provide the prediction result
    return render_template('predict.html', prediction=prediction, Move=Move,
                           Resultant_Gyro=Resultant_Gyro,Resultant_Acc=Resultant_Acc)