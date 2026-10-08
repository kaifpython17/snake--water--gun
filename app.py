from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)

app.secret_key = "my-game-secret-key"

choices = {
    "s": 0,
    "w": 1,
    "g": 2
}

reverse_choices = {
    0: "Snake",
    1: "Water",
    2: "Gun"
}


@app.route("/", methods=["GET", "POST"])
def home():

    # Starting score
    session.setdefault("user_score", 0)
    session.setdefault("comp_score", 0)

    message = "Choose your move!"
    result_type = "neutral"

    you = ""
    computer = ""

    game_over = False

    # When player clicks a game button
    if request.method == "POST":

        choice = request.form.get("choice")

        # -------------------------
        # RESET MATCH
        # -------------------------

        if choice == "reset":

            session["user_score"] = 0
            session["comp_score"] = 0

            return redirect("/")


        # -------------------------
        # PLAY ROUND
        # -------------------------

        elif choice in choices:

            # Player choice
            you_num = choices[choice]

            # Computer choice
            computer_num = random.choice([0, 1, 2])

            you = reverse_choices[you_num]
            computer = reverse_choices[computer_num]

            # Winner logic
            result = you_num - computer_num


            # DRAW
            if result == 0:

                message = "It's a Draw!"

                result_type = "draw"


            # PLAYER WINS
            elif result == -1 or result == 2:

                message = "You Won This Round!"

                result_type = "win"

                session["user_score"] += 1


            # COMPUTER WINS
            else:

                message = "Computer Won This Round!"

                result_type = "lose"

                session["comp_score"] += 1


            # -------------------------
            # MATCH WINNER
            # -------------------------

            if session["user_score"] == 3:

                message = "🏆 You Won The Match!"

                result_type = "win"

                game_over = True


            elif session["comp_score"] == 3:

                message = "💻 Computer Won The Match!"

                result_type = "lose"

                game_over = True


    return render_template(
        "index.html",

        user_score=session["user_score"],

        comp_score=session["comp_score"],

        message=message,

        result_type=result_type,

        you=you,

        computer=computer,

        game_over=game_over
    )


# -------------------------
# AUTOMATIC NEW MATCH
# -------------------------

@app.route("/auto-reset", methods=["POST"])
def auto_reset():

    session["user_score"] = 0
    session["comp_score"] = 0

    return "", 204


# -------------------------
# START FLASK
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)