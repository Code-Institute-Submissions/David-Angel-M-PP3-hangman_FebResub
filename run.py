import random
import requests
import os


class GameVisuals:
    def __init__(self, word):
        self.word = word
        self.guessed_letters = [None] * len(word)
        self.played_letters = []

    def getGameTitle(self):
        print("++++++++++++Welcome to hangman+++++++++++++")
        print("+++++++++++You are ready to play+++++++++++")
        print("You have 7 attemps to guess the hidden word")
        print("Numbers and symbols would be consider as\nfailed attemp")
        
    def getGameWord(self):
        for x in range(len(self.word)):
            if self.word[x] == self.guessed_letters[x]:
                print(self.word[x], end=" ")
            else:
                print("_", end=" ")
        print("")
        print("")

    def compareWordLetter(self, user_input):
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

    def getPlayedLetters(self):
        for letter in self.played_letters:
            print(letter, end=" ")

    def clearConsole(self):
        os.system("clear")


class Words:
    """
    Words manager
    """

    def __init__(self):
        self.words = []

    def getWordList(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site, timeout=10)
        wordsInBytes = response.content.splitlines()
        self.convertBytesIntoString(wordsInBytes)
        self.filterWordList()

    def convertBytesIntoString(self, wordsInBytes):
        for word in wordsInBytes:
            self.words.append(word.decode("utf-8"))

    def filterWordList(self):
        for word in self.words:
            if len(word) < 4:
                self.words.remove(word)

    def getRandomWord(self):
        index = random.randint(0, len(self.words) - 1)
        return self.words[index]


if __name__ == "__main__":
    # Init
    w1 = Words()
    fails = 0
    hits = 0

    w1.getWordList()
    gameWord = w1.getRandomWord()
    word_length = len(gameWord)
    visuals = GameVisuals(gameWord)

    visuals.getGameTitle()
    visuals.getGameWord()

    while fails < 7 and hits < word_length:
        user_input = input("Please enter a letter:\n ")
        visuals.clearConsole()
        letter_found_count = visuals.compareWordLetter(user_input)
        if letter_found_count == 0:
            fails = fails + 1
        elif letter_found_count > 0:
            hits = hits + letter_found_count
        visuals.getGameTitle()
        visuals.getGameWord()
        print("Letters played...")
        visuals.getPlayedLetters()
        print("")
        print(f"Fails: {fails}")

    if hits == word_length:
        print("!!!!!CONGRATULATIONS YOU WON!!!!!!")
    else:
        print("SORRY YOU LOSE")
        print("The word was: " + gameWord)
