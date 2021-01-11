"""

Соблюдать правила форматирования кода (методы не длиннее 10 строк)
с python type hints
Протестировать код через бибилотеку unittest

"""

import random
import requests
from bs4 import BeautifulSoup
import re
import unittest


def symbols ():
    symbols_a_z = [i for i in range(97, 123)]
    another_symbols = [33, 37, 45, 63]
    numbers = [i for i in range(48,58)]
    all_symbols= symbols_a_z + another_symbols + numbers
    return all_symbols

def password (userlength):
    if userlength > 17:
        raise ValueError
    elif isinstance(userlength, str):
        raise TypeError

    all_symbols = symbols()
    password = ""
    list_length = len(all_symbols) -1

    for i in range(0, userlength):
        randomNumber = random.randint(0, list_length)
        selectnumber = all_symbols[randomNumber]
        selectnumber= chr(selectnumber)
        password += selectnumber

    return password

def wordsearch (something):
    wordscan = requests.get("https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/")
    html = wordscan.content
    soup = BeautifulSoup(html, features="html.parser")
    words = soup.select("div.field-items>div.field-item>p")
    wordlist = []

    for word in words[1]:
        try:
            wordlist.append((re.findall(pattern=r"\w+", string=word.string)[0]))
        except (AttributeError, TypeError):
            pass

    del wordlist[0]
    if something in wordlist:
        return "Wrong Password"
    else:
        return "Good Password"

class TestLogic(unittest.TestCase):

    def test_wrong_password(self):
        wrong_password = "general"
        self.assertEqual(wordsearch(wrong_password),"Wrong Password")

    def test_good_password(self):
        good_password = "4sad?!12"
        self.assertEqual(wordsearch(good_password),"Good Password")

    def test_correct_generate(self):
        self.assertEqual(len(password(5)), 5)

    def test_raises_error(self):
        with self.assertRaises(ValueError):
            password(18)

    def test_fails_on_string(self):
        with self.assertRaises(TypeError):
           password("AAAA")

    def test_wrong_symbol(self):
        sample_password0 = password (10)
        sample_password1 = password (6)
        sample_password2 = password (4)

        self.assertTrue("*" not in sample_password0)
        self.assertTrue("&" not in sample_password1)
        self.assertTrue("(" not in sample_password2)
unittest.main()

#some text
