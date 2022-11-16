import random
import requests
import os


class GameVisuals:
    def __init__(self, word):
        self.word = word
        self.guessed_letters = [None] * len(word)
        self.played_letters = []

    def get_game_title(self):
        print("++++++++++++Welcome to hangman+++++++++++++")
        print("+++++++++++You are ready to play+++++++++++")
        print("You have 7 attemps to guess the hidden word")
        print("Numbers and symbols would be consider as\nfailed attemp")

    def get_game_word(self):
        for x in range(len(self.word)):
            if self.word[x] == self.guessed_letters[x]:
                print(self.word[x], end=" ")
            else:
                print("_", end=" ")
        print("")
        print("")

    def compare_word_letter(self, user_input):
        index = 0
        letter_found_count = 0
        user_input_lenght = len(user_input)

        for guess_letter in self.played_letters:
            if guess_letter == user_input:
                letter_found_count = -1

        if user_input_lenght != 1:
            letter_found_count = -1

        if letter_found_count != -1:
            for letter in self.word:
                if letter == user_input:
                    self.guessed_letters[index] = user_input
                    letter_found_count = letter_found_count + 1
                index = index + 1
            self.played_letters.append(user_input)

        return letter_found_count

    def get_played_letters(self):
        for letter in self.played_letters:
            print(letter, end=" ")

    def clear_console(self):
        os.system("clear")


class Words:
    """
    Words manager
    """

    def __init__(self):
        self.words = []

    def get_word_list(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site, timeout=10)
        words_in_bytes = response.content.splitlines()
        self.convert_bytes_into_string(words_in_bytes)
        self.filter_word_list()

    def convert_bytes_into_string(self, words_in_bytes):
        for word in words_in_bytes:
            self.words.append(word.decode("utf-8"))

    def filter_word_list(self):
        for word in self.words:
            if len(word) < 4:
                self.words.remove(word)

    def get_random_word(self):
        index = random.randint(0, len(self.words) - 1)
        return self.words[index]


if __name__ == "__main__":
    # Init
    w1 = Words()
    fails = 0
    hits = 0

    w1.get_word_list()
    game_word = w1.get_random_word()
    word_length = len(game_word)
    visuals = GameVisuals(game_word)

    visuals.get_game_title()
    visuals.get_game_word()

    while fails < 7 and hits < word_length:
        user_input = input("Please enter a letter:\n ")
        visuals.clear_console()
        letter_found_count = visuals.compare_word_letter(user_input)
        if letter_found_count == 0:
            fails = fails + 1
        elif letter_found_count > 0:
            hits = hits + letter_found_count
        visuals.get_game_title()
        visuals.get_game_word()
        print("Letters played...")
        visuals.get_played_letters()
        print("")
        print(f"Fails: {fails}")

    if hits == word_length:
        print("!!!!!CONGRATULATIONS YOU WON!!!!!!")
    else:
        print("SORRY YOU LOSE")
        print("The word was: " + game_word)
