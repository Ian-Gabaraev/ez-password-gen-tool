import random
import requests
import re
import unittest
from typing import List
from bs4 import BeautifulSoup


class PasswordTool:

    """
    dictionary_url = Атрибут класса, можно получить по форме
                     PasswordTool.dictionary_url
    """

    dictionary_url = "https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/"

    def __init__(self, **kwargs):
        """
        :param kwargs: принимает неопределенное количество аргументов
        с ключом. Аргументы можно получить по форме kwargs.get("название аргумента")

        self.user_password = kwargs.get("user_password") or None означает:

        Если передан аргумент user_password, то self.user_password равно user_password
        Если не передан, то self.user_password равно None
        """
        self.user_password = kwargs.get("user_password") or None
        self.required_length = kwargs.get("required_length") or None
        self.user_password_length = len(self.user_password) if self.user_password else None

        self.options = None
        self.options_length = None

    @staticmethod
    def get_legit_characters() -> list:

        characters = [chr(character) for character in range(97, 123)]
        extra_characters = [chr(character) for character in [33, 37, 45, 63]]
        digits = [digit for digit in range(0, 10)]

        return characters+extra_characters+digits

    def __make_password(self, length) -> str:

        """
        join объединяет элементы списка через символ, который
        передается в скобках
        :param length:
        :return:
        """

        self.options = PasswordTool.get_legit_characters()
        self.options_length = len(self.options)

        return "".join(
            [str(self.options[random.randint(0, self.options_length)]) for _ in range(0, length)]
        )

    def __generate(self, length) -> str:
        """
        метод пытается создать пароль, который
        не является словом
        :param length:
        :return:
        """
        password = self.__make_password(length)

        while not self.is_good(password):
            password = self.__make_password(length)

        return password

    def main(self) -> str:
        """
        Выбираем действие в зависимости от
        переданных аргументов в __init__()
        :return:
        """
        if self.user_password and not PasswordTool.is_good(self.user_password):
            return self.__generate(self.user_password_length)
        elif self.user_password and self.is_good(self.user_password):
            return self.user_password
        elif not self.user_password and self.required_length:
            return self.__generate(self.required_length)
        else:
            raise ValueError("Nothing to do!")

    @staticmethod
    def make_soup(url) -> "BeautifulSoup":
        response = requests.get(url)
        html = response.content

        return BeautifulSoup(html, features="html.parser")

    @staticmethod
    def get_words(soup: "BeautifulSoup") -> List[str]:
        """
        получаем слова из soup и сохраняем
        в список wordlist
        :param soup:
        :return:
        """

        words = soup.select("div.field-items>div.field-item>p")
        wordlist = []

        for word in words[1]:
            try:
                wordlist.append((re.findall(pattern=r"\w+", string=word.string)[0]))
            except (AttributeError, TypeError):
                pass

        del wordlist[0]

        return wordlist

    @staticmethod
    def is_good(something) -> bool:
        """
        возвращает True если пароль не слово или False
        :param something:
        :return:
        """

        soup = PasswordTool.make_soup(PasswordTool.dictionary_url)
        wordlist = PasswordTool.get_words(soup)

        return not something in wordlist


class TestPasswordTool(unittest.TestCase):

    def test_generate_good_password_for_bad_user_password(self):
        bad_password = "general"

        self.assertNotEqual(bad_password, PasswordTool(user_password=bad_password).main())

    def test_return_user_password_if_user_password_is_good(self):
        good_password = "jn4ju42ji"

        self.assertEqual(good_password, PasswordTool(user_password=good_password).main())

    def test_raise_error_nothing_to_do(self):

        with self.assertRaises(ValueError):

            PasswordTool().main()

    def test_generate_password_on_request(self):
        generated_password = PasswordTool(required_length=10).main()

        self.assertTrue(len(generated_password), 10)
        self.assertTrue(PasswordTool.is_good(generated_password))


unittest.main()
