import datetime
import json
import random
from flask import Flask, jsonify, request, Response
import mysql.connector

app = Flask(__name__)
# app.json.sort_keys = False
app.config['JSON_SORT_KEYS'] = False

myDB = mysql.connector.connect(
    host='localhost',
    database='bullsandcowsschema',
    user='root',
    password='Mk$#032375'
)


class BullsAndCowsService:
    @staticmethod
    def generate_answer() -> str:
        digits = list("0123456789")
        random.shuffle(digits)
        return "".join(digits[:4])

    @staticmethod
    def calculate_result(guess: str, answer: str) -> str:
        exact = 0
        partial = 0
        for i in range(4):
            if guess[i] == answer[i]:
                exact += 1
            elif guess[i] in answer:
                partial += 1
        return f"e:{exact}:p:{partial}"


@app.route("/begin", methods=["POST"])
def begin_game():
    answer = BullsAndCowsService.generate_answer()
    status = "In Progress"

    myCursor = myDB.cursor()
    sql = "INSERT INTO game (answer, status) VALUES (%s, %s)"
    vals = (answer, status)
    myCursor.execute(sql, vals)
    myDB.commit()

    new_id = myCursor.lastrowid
    myCursor.close()

    return jsonify({"gameId": new_id, "message": "Game started successfully."}), 201


@app.route("/guess", methods=["POST"])
def make_guess():
    data = request.get_json() or {}
    guess = data.get("guess")
    game_id = data.get("gameId")

    if not guess or not game_id:
        return jsonify({"error": "Missing 'guess' or 'gameId' in JSON body."}), 400

    myCursor = myDB.cursor(dictionary=True)

    myCursor.execute("SELECT * FROM game WHERE gameId = %s", (game_id,))
    game = myCursor.fetchone()

    if not game:
        myCursor.close()
        return jsonify({"error": "Game not found."}), 404

    if game["status"] == "Finished":
        myCursor.close()
        return jsonify({"error": "This game is already finished."}), 400

    result = BullsAndCowsService.calculate_result(guess, game["answer"])
    current_time = datetime.datetime.now().isoformat()

    sql_round = "INSERT INTO rounds (gameId, guess, time, result) VALUES (%s, %s, %s, %s)"
    vals_round = (game_id, guess, current_time, result)
    myCursor.execute(sql_round, vals_round)

    if result == "e:4:p:0":
        myCursor.execute(
            "UPDATE game SET status = 'Finished' WHERE gameId = %s", (game_id,))

    myDB.commit()
    myCursor.close()

    new_round = {
        "guess": guess,
        "time": current_time,
        "result": result
    }
    return jsonify(new_round), 200


@app.route("/game", methods=["GET"])
def get_all_games():
    games = []
    myCursor = myDB.cursor(dictionary=True)
    myCursor.execute("SELECT * FROM game")

    for row in myCursor:
        if row["status"] == "In Progress":
            row["answer"] = "HIDDEN"
        games.append(row)

    myCursor.close()
    return Response(
        json.dumps(games, sort_keys=False),
        mimetype='application/json'
    ), 200


@app.route("/game/<int:game_id>", methods=["GET"])
def get_game_by_id(game_id):
    myCursor = myDB.cursor(dictionary=True)
    myCursor.execute("SELECT * FROM game WHERE gameId = %s", (game_id,))
    game = myCursor.fetchone()
    myCursor.close()

    if not game:
        return jsonify({"error": "Game not found."}), 404

    if game["status"] == "In Progress":
        game["answer"] = "HIDDEN"

    return jsonify(game), 200


@app.route("/rounds/<int:game_id>", methods=["GET"])
def get_rounds_for_game(game_id):
    rounds = []
    myCursor = myDB.cursor(dictionary=True)

    myCursor.execute(
        "SELECT guess, time, result FROM rounds WHERE gameId = %s ORDER BY time ASC", (game_id,))

    for row in myCursor:
        rounds.append(row)

    myCursor.close()

    if not rounds:
        return jsonify({"message": "No rounds found for this game or game does not exist."}), 200

    return jsonify(rounds), 200


if __name__ == '__main__':
    app.run(debug=True)
