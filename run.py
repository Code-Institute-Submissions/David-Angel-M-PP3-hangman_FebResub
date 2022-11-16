import random
import requests

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

