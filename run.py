"""
This module contains the implementation of the hangman game
"""

import random
import os
import re
import requests


class GameVisuals:
    """
    Class contains all methods required
    in the game logic after a word is given
    """

    def __init__(self, word):
        self.word = word
        self.guessed_letters = [None] * len(word)
        self.played_letters = []

    def get_game_title(self):
        """
        Welcoming message for user
        """
        print("++++++++++++Welcome to hangman+++++++++++++")
        print("+++++++++++You are ready to play+++++++++++")
        print("You have 7 attempts to guess the hidden word")

    def get_game_hidden_word(self):
        """
        Method shows dashes in the place where letter should be,
        if user gets a letter the letter shows
        """
        for x_value in range(len(self.word)):
            if self.word[x_value] == self.guessed_letters[x_value]:
                print(self.word[x_value], end=" ")
            else:
                print("_", end=" ")
        print("")
        print("")

    def compare_word_letter(self, user_input) -> int:
        """
        Verifies if the user input is a letter of the hidden word
        """
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
        """
        Shows all the letters that the player has typed
        """
        for letter in self.played_letters:
            print(letter, end=" ")

    def clear_console(self):
        """
        Clears the console for new game
        """
        os.system("clear")

    def user_input_validator(self) -> str:
        """
        Validate user input
        """
        while True:
            user_input = input("Please enter a letter: ").strip()
            if (re.match(r'^\s*$', user_input)):
                print("You have typed only spaces, please try again...")
            elif (len(user_input) == 0):
                print("You haven't typed a letter, please try again...")
            elif (not re.search(r'^[a-zA-Z]+$', user_input)):
                print("The character " + user_input +
                      " in not a letter, please try again...")
            elif (len(user_input) > 1):
                print("You typed more than one character, please try again...")
            else:
                return user_input.lower()


class Words:
    """
    Class used to get a list of words and return a random word
    """

    def __init__(self):
        self.words = []

    def get_word_list(self):
        """
        Get a list of words from an online resource
        """
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site, timeout=10)
        words_in_bytes = response.content.splitlines()
        self.convert_bytes_into_string(words_in_bytes)
        self.filter_word_list()

    def convert_bytes_into_string(self, words_in_bytes):
        """
        Convert a list of byte sequences into a list of strings
        """
        for word in words_in_bytes:
            self.words.append(word.decode("utf-8"))

    def filter_word_list(self):
        """
        Filter the list of words by removing all words with length less than 4
        """
        for word in self.words:
            if len(word) < 4:
                self.words.remove(word)

    def get_random_word(self) -> str:
        """
        Get random word to start a new game
        """
        index = random.randint(0, len(self.words) - 1)
        return self.words[index]


if __name__ == "__main__":
    w1 = Words()
    FAILS = 0
    HITS = 0

    w1.get_word_list()
    game_word = w1.get_random_word()
    word_length = len(game_word)
    visuals = GameVisuals(game_word)

    visuals.clear_console()
    visuals.get_game_title()
    visuals.get_game_hidden_word()

    while FAILS < 7 and HITS < word_length:
        user_input = visuals.user_input_validator()
        visuals.clear_console()
        letter_found_count = visuals.compare_word_letter(user_input)
        if letter_found_count == 0:
            FAILS = FAILS + 1
        elif letter_found_count > 0:
            HITS = HITS + letter_found_count
        visuals.get_game_title()
        visuals.get_game_hidden_word()
        print("Letters played...")
        visuals.get_played_letters()
        print("")
        print(f"FAILS: {FAILS}")

    if HITS == word_length:
        print("!!!!!CONGRATULATIONS YOU WON!!!!!!")
    else:
        print("SORRY YOU LOSE")
        print("The word was: " + game_word)
