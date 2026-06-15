from flask import Flask, render_template, request, session
import random

app = Flask(__name__)

app.secret_key = "hangman_secret"

WORDS = {

    "Easy": [
        "cat",
        "dog",
        "apple",
        "book",
        "fish"
    ],

    "Medium": [
        "camel",
        "rocket",
        "python",
        "tiger",
        "orange"
    ],

    "Hard": [
        "computer",
        "developer",
        "elephant",
        "artificial",
        "database"
    ]
}


@app.route("/", methods=["GET", "POST"])
def home():

    if "player_name" not in session:
        session["player_name"] = ""

    if "difficulty" not in session:
        session["difficulty"] = "Easy"

    if "word" not in session:

        session["word"] = random.choice(
            WORDS[session["difficulty"]]
        )

    if "correct" not in session:
        session["correct"] = []

    if "wrong" not in session:
        session["wrong"] = []

    if "lives" not in session:
        session["lives"] = 6

    if "score" not in session:
        session["score"] = 0

    message = ""

    if request.method == "POST":

        action = request.form.get("action")

        if action == "restart":

            difficulty = session["difficulty"]

            session.clear()

            session["difficulty"] = difficulty

            session["word"] = random.choice(
                WORDS[difficulty]
            )

            session["correct"] = []

            session["wrong"] = []

            session["lives"] = 6

            session["score"] = 0

            return home()

        elif action == "difficulty":

            difficulty = request.form.get(
                "difficulty"
            )

            session["difficulty"] = difficulty

            session["word"] = random.choice(
                WORDS[difficulty]
            )

            session["correct"] = []

            session["wrong"] = []

            session["lives"] = 6

            session["score"] = 0

        else:

            session["player_name"] = request.form.get(
                "player_name",
                session["player_name"]
            )

            guess = request.form.get(
                "guess",
                ""
            ).lower()

            if len(guess) == 1:

                if guess in session["word"]:

                    if guess not in session["correct"]:

                        session["correct"].append(
                            guess
                        )

                        session["score"] += 10

                else:

                    if guess not in session["wrong"]:

                        session["wrong"].append(
                            guess
                        )

                        session["lives"] -= 1

    display = ""

    for letter in session["word"]:

        if letter in session["correct"]:

            display += letter + " "

        else:

            display += "_ "

    unique_letters = len(
        set(session["word"])
    )

    found_letters = len(
        set(session["correct"])
    )

    progress = int(
        (found_letters / unique_letters) * 100
    )

    if "_" not in display:

        message = "🏆 YOU WIN"

    if session["lives"] == 0:

        message = (
            "💀 YOU LOSE | Word: "
            + session["word"]
        )

    return render_template(

        "index.html",

        player_name=session["player_name"],

        display=display,

        score=session["score"],

        lives=session["lives"],

        wrong=session["wrong"],

        progress=progress,

        message=message
    )


if __name__ == "__main__":

    app.run(debug=True)