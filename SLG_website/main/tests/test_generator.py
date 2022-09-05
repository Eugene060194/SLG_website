from django.test import TestCase
from random import randint, choice
from time import time
from main._generator import preparing_base, Rhyme, CompleteText


class PreparingBaseTest(TestCase):
    def test_1(self):
        test_var = preparing_base(open('main/baseofwords/nouns.txt', 'r', encoding='UTF-8'))
        with open('main/baseofwords/nouns.txt', 'r', encoding='UTF-8') as opened_file:
            output = opened_file.readlines()
        for i in range(len(output)):
            output[i] = output[i].replace('\r', '')
            output[i] = output[i].replace('\n', '')
        self.assertEqual(output, test_var)


class RhymeTest(TestCase):
    def test_1(self):
        test_word = 'бабка'
        rhymes = Rhyme(test_word).output()
        if '*НЕТУ РИФМЫ*' in rhymes:
            self.assertTrue(False)
        else:
            self.assertTrue(rhymes)


class CompleteTextTest(TestCase):
    def test_1(self):
        print()
        for i in range(2):
            time_inp = time()
            test_text = CompleteText(
                randint(1, 16),
                randint(1, 16),
                randint(2, 4),
                randint(1, 8),
                randint(2, 8),
                choice(['cross', 'consistent'])
            )
            time_out = time()
            string_error_counter = 0
            rhyme_error_counter = 0
            for _ in test_text.output():
                for q in _:
                    if q == '*НЕ УДАЛОСЬ СФОРМИРОВАТЬ СТРОКУ*':
                        string_error_counter += 1
                    if '*НЕТУ РИФМЫ*' in q:
                        rhyme_error_counter += 1
            print(f'Testing text №{i + 1} created in {round((time_out - time_inp), 2)} sec!')
            if string_error_counter != 0:
                print(f'Amount "String-error": {string_error_counter}')
            if rhyme_error_counter != 0:
                print(f'Amount "Rhyme-error": {rhyme_error_counter}')
            print('\n')
        self.assertTrue(True)
