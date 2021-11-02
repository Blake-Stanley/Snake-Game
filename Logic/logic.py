import random




# gets the current high score
def getHighScore():
    current_high_score_obj = open('Logic/highScore.txt',
                                  'r')  # note that this creates an object
    return current_high_score_obj.read()


# sets high score to the player's score
def setHighScore(score):
    current_high_score = int(getHighScore())
    if current_high_score < score:
        current_high_score_obj = open(
            'Logic/highScore.txt', 'w')  # w mode allows writing vs r reading
        current_score = "" + str(score)
        current_high_score_obj.write(current_score)



# sets high score back to 0
def clearHighScore():
    current_high_score_obj = open('Logic/highScore.txt', 'w')
    current_high_score_obj.write("0")

    