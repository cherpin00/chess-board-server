import logging
import os

import chess
from flask import render_template, send_from_directory, request
from flask.json import jsonify

from app import app
import motorControl


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/board')
def redner_board():
    board = chess.Board()
    # TODO: the env is not working
    return render_template('home.html', fen=board.fen().split(" ")[0], host=os.environ.get("host", "127.0.0.1:5000"))


@app.route('/img/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/static/img/', filename)


@app.route('/updateBoard', methods=["POST"])
def update_board():
    ren = request.json
    print(ren)
    return jsonify(success=True), 200

@app.route("/control", methods=["POST", "GET"])
def move():        
    return render_template("control.html")

@app.route("/mouse/position", methods=["POST"])
def mouse_position():
    x, y = int(request.json["x"]), int(request.json["y"])
    if request.args.get("convert") != "false":
        x = x/5 - 93
        y = y/5 - 2
    currPosition = motorControl.myMotor.goTo([x, y])
    print(f"Current Position: {currPosition}")
    return f"position ({currPosition})"


@app.route("/calibrate")
def calibrate():
    motorControl.myMotor.home()
    return jsonify({ "message" : f"Successfully homed arm. Current Posistion : {motorControl.myMotor.currentPosition}"})