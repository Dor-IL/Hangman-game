from re import finditer
from random import choice

secret_word = None
old_letters_guessed = []
MAX_TRIES = 6
num_of_tries = 0
HANGMAN_PHOTOS = {0: """    x-------x\n""", 
                  1: """    x-------x
    |
    |
    |
    |
    |\n""", 
    2: """    x-------x
    |       |
    |       0
    |
    |
    |\n""", 
    3: """    x-------x
    |       |
    |       0
    |       |
    |
    |\n""", 
    4: """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |\n""", 
    5: """    x-------x
    |       |
    |       0
    |      /|\\
    |       |
    |\n""", 
    6: """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""}

def openning_screen():
      """this function print the opening screen"""
      print("""Welcome to the game Hangman
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \\ / _' | '_ ' _ \\ / _' | '_ \\
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                        __/ |
                       |___/
max number of tries: 6""")


def check_win(secret_word, old_letters_guessed):
    """this function check if the player guessed every correct letter

    Args:
        secret_word (string): The game secret word
        old_letters_guessed (list): every letter the player guessed

    Returns:
        bool: whether he guessed the right letters or not
    """
    for letter in secret_word:  # every letter that makes up the word
      if letter not in old_letters_guessed:  # still missing at least one letter
        return False
    return True


def right_letters_index(secret_word, old_letters_guessed):
  """this function make a list that hold every letter 
  the player guessed right and her place in the word

  Args:
      secret_word (ste): the game secret word
      old_letters_guessed (list): every letter the player guessed

  Returns:
      list: list that hold tuples made of a letter and her index in the secret word
  """
  right_letters_index = []
  for letter in old_letters_guessed:  # get every letter from the list
    for index in finditer(letter, secret_word):  # get every index a right letter appeared in the word
      right_letters_index.append((letter,index.start()))  # made a list that each value hold the letter and her index
  return right_letters_index


def show_hidden_word(secret_word, old_letters_guessed):
    """The function returns a string consisting of letters and underscores.
      The string shows the letters the player guessed right in their right position,
      and the other letters in the string (which the player has not yet guessed) as underlines.

    Args:
        secret_word (str): the game secret word
        old_letters_guessed (list): every letter the player guessed

    Returns:
        str: secret word with the letter the player didn't guess as underscore
    """
    secret_word_list = []
    for _ in range(len(secret_word)): secret_word_list.append("_") #  create a list made of the word length with '_'
    for letter,index in right_letters_index(secret_word, old_letters_guessed): # get every right letter and her index
      secret_word_list[index] = letter #  add the letters in the index
    return " ".join(secret_word_list) # make the word
      

def check_valid_input(letter_guessed, old_letters_guessed):
    """This function check if the guessed letter is a single letter that the player hasn't guessed yet.

    Args:
        letter_guessed (str_): guessed letter
        old_letters_guessed (str): every letter the player guessed

    Returns:
        bool: the validity of the player guess
    """
    if not letter_guessed.isalpha(): return False # check if the guess isn't a letter 
    elif len(letter_guessed) != 1:  return False  # check if the guess is more than one character long
    elif letter_guessed in old_letters_guessed: return False  # check if the player guessed a new letter
    else: return True 


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """this function add the letter to the old letters list if the input is valid

    Args:
        letter_guessed (str): player guess
        old_letters_guessed (list): every letter the player guessed
    """
    if not check_valid_input(letter_guessed, old_letters_guessed):  # check if the input is valid
      old_letters_guessed.sort()
      new_letters_list = " -> ".join(old_letters_guessed)
      print(f"X\n{new_letters_list}")
    else: # add the letter to the guessed letter list
      old_letters_guessed.append(letter_guessed)


def choose_word(file_path):
    """this function choose a random word for the game from a file

    Args:
        file_path (str): words file

    Returns:
        str:  the secret word, or False if the file is missing/empty
    """
    try:
        with open(file_path, 'r') as words_file:
            words_list = words_file.read().split()  # every whitespace-separated word
    except FileNotFoundError:
        print(f"Could not find the words file: {file_path}")
        return False

    if not words_list:
        print(f"The words file is empty: {file_path}")
        return False

    return choice(words_list).lower()  # pick a random word


def main():
    global num_of_tries

    openning_screen()

    play_again = True
    while play_again:
        # reset the game state for a fresh round
        num_of_tries = 0
        old_letters_guessed.clear()

        secret_word = choose_word("words.txt")
        if secret_word is False:
            return

        print("Let's start!\n" + HANGMAN_PHOTOS[0])
        print(show_hidden_word(secret_word, old_letters_guessed))

        while True:

            if check_win(secret_word, old_letters_guessed):
                print("WIN")
                break

            elif num_of_tries == MAX_TRIES:
                print("LOSE")
                print(f"The word was: {secret_word}")
                break

            guess = input("Enter your guess: ")
            guess = guess.replace(" ", "")
            guess = guess.lower()

            if check_valid_input(guess, old_letters_guessed):
                try_update_letter_guessed(guess, old_letters_guessed)
                if guess not in secret_word:
                    num_of_tries += 1
                    print(":(")
                    print(HANGMAN_PHOTOS[num_of_tries])
                print(show_hidden_word(secret_word, old_letters_guessed))
            else:
                try_update_letter_guessed(guess, old_letters_guessed)

        answer = input("Do you want to play again?(yes/no) ").strip().lower()
        play_again = answer in ("yes", "y")

    print("Thanks for playing!")

        

        
        
          
       


if __name__ == "__main__":
     main()


