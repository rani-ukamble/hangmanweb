from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'hangman_secret_key'

# Predefined list of words
words = ['python', 'flask', 'hangman', 'coding', 'program', 'developer', 'iamrani', 'gaming', 'night', 'letter']

# Hangman stages as diagrams
stages = [
    """
     +---+
         |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     O   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     O   |
     |   |
         |
         |
         |
    =========
    """,
    """
     +---+
     O   |
    /|   |
         |
         |
         |
    =========
    """,
    """
     +---+
     O   |
    /|\\  |
         |
         |
         |
    =========
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
         |
         |
    =========
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
         |
         |
    =========
    """
]

def reset_game():
    session['codeword'] = random.choice(words)
    session['answer'] = ['_'] * len(session['codeword'])
    session['incorrect'] = []
    session['misses'] = 0
    session['max_misses'] = len(stages) - 1  # Maximum chances
    session['message'] = ''  # Clear any previous message

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'codeword' not in session:
        reset_game()

    if request.method == 'POST':
        if 'letter' in request.form:
            letter = request.form.get('letter').lower()
            guess = False

            for i, char in enumerate(session['codeword']):
                if letter == char:
                    session['answer'][i] = letter
                    guess = True

            if guess:
                session['message'] = "Correct!"
            else:
                session['message'] = "Incorrect! Another portion of the person has been drawn."
                session['incorrect'].append(letter)
                session['misses'] += 1

            # Check if game has ended
            if ''.join(session['answer']) == session['codeword']:
                session['message'] = "Hooray! You saved the person from being hanged and earned a medal of honor! Congratulations!"
                return redirect(url_for('end_game', result='win'))
            elif session['misses'] >= session['max_misses']:
                session['message'] = f"Oh no! The person was hanged. The word was '{session['codeword']}'."
                return redirect(url_for('end_game', result='lose'))

    # Ensure misses are within the valid range for stages
    stage_index = min(session['misses'], len(stages) - 1)
    return render_template('index.html', stage=stages[stage_index])

@app.route('/end_game/<result>', methods=['GET', 'POST'])
def end_game(result):
    if request.method == 'POST':
        if 'new_game' in request.form:
            reset_game()
            return redirect(url_for('index'))
        elif 'exit' in request.form:
            return "Thank you for playing! Goodbye!"

    # Ensure misses are within the valid range for stages
    stage_index = min(session['misses'], len(stages) - 1)
    return render_template('end_game.html', result=result, stage=stages[stage_index])

if __name__ == '__main__':
    app.run(debug=True)
