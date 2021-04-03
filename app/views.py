import logging
import os

import chess
from flask import render_template, send_from_directory, request
from flask.json import jsonify

from app import app


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
