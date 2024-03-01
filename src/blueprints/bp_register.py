from flask import Blueprint, jsonify

register_bp = Blueprint("get", __name__)
from ..models import Player, Trainer, Data
from ..schemas import Player_Schema, Trainer_Schema, Data_Schema
from ..extension import db





