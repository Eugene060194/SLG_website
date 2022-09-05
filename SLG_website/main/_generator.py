from random import choice


# Распаковка словарных баз
def preparing_base(base_file):
    """
    Функция подготовки словарных баз(читает txt, убирает пробелы
    и символы новой строки, формирует список).

    :param base_file: Файл в формате txt
    :return: Список, где каждый элемент - слово из базы
    """
    with base_file as opened_file:
        output = opened_file.readlines()
    for i in range(len(output)):  # Проход по списку через индекс
        output[i] = output[i].replace('\r', '')
        output[i] = output[i].replace('\n', '')
    return output


BASE_OF_NOUNS = preparing_base(open('main/baseofwords/nouns.txt', 'r', encoding='UTF-8'))
BASE_OF_VERBS = preparing_base(open('main/baseofwords/verbs.txt', 'r', encoding='UTF-8'))
BASE_OF_PRONOUNS = preparing_base(open('main/baseofwords/pronouns.txt', 'r', encoding='UTF-8'))
BASE_OF_ADJECTIVES = preparing_base(open('main/baseofwords/adjectives.txt', 'r', encoding='UTF-8'))

# Переменная, хранящая правила построения словосочетаний(для куплетов)
PHRASE_OPTIONS = [
    (BASE_OF_VERBS, BASE_OF_NOUNS),
    (BASE_OF_ADJECTIVES, BASE_OF_NOUNS),
    (BASE_OF_PRONOUNS, BASE_OF_VERBS),
    (BASE_OF_PRONOUNS, BASE_OF_ADJECTIVES)
]


class Rhyme:
    """
    Класс, отвечающий за подбор рифмы.
    """
    def __init__(self, base_word):
        """
        При создании экземпляра класса формирует список со всеми
        возможными рифмами из исходных словарных баз.

        :param base_word: Слово, к которому нужно подобрать рифмы
        """
        self.bw = base_word
        self.bw_syllables = Rhyme.__decomposition_into_syllables(self.bw)
        self.amount_bw_syllables = len(self.bw_syllables)
        self.output_rhymes_list = self.__get_all_rhymes()

    @staticmethod
    def __decomposition_into_syllables(word):
        """
        Разложение слова на слоги.

        :param word: Слово, которое необходимо разложить
        :return: Слово по слогам в формате списка
        """
        syllables_list = []
        for i in word:
            # Условие для идентификации гласных в слове
            if i in 'аеёиоуыэюяАЕЁИОУЫЭЮЯ':
                # Добавление гласной новым элементом списка
                syllables_list.append(i)
            # Условие для идентификации согласных в слове
            if i in 'бвгджзклмнпрстфхцчшщйьъБВГДЖЗКЛМНПРСТФХЦЧШЩЙЬЪ':
                if not syllables_list:
                    continue
                else:
                    # Добавление согласной к последнему элементу списка
                    syllables_list[-1] += i
        return syllables_list

    def __compare_1_0(self, cw_syllables):
        """
        Функция для сравнения слов при поиске рифмы.
        Сравнивает по одному последнему слогу.

        :param cw_syllables: Слово, которое нужно сравнить с базовым(разложенное на слоги)
        :return: True/False, рифма/не рифма
        """
        if self.bw_syllables[-1] == cw_syllables[-1]:
            return True

    def __compare_2_0(self, cw_syllables):
        """
        Функция для сравнения слов при поиске рифмы.
        Сравнивает по два последних слога.

        :param cw_syllables: Слово, которое нужно сравнить с базовым(разложенное на слоги)
        :return: True/False, рифма/не рифма
        """
        if self.bw_syllables[-1:-3:-1] == cw_syllables[-1:-3:-1]:
            return True

    def __compare_1_2(self, cw_syllables, i):
        """
        Функция для сравнения слов при поиске рифмы.
        Сравнивает по одному последнему слогу и по две
        предпоследние буквы.

        :param cw_syllables: Слово, которое нужно сравнить с базовым(разложенное на слоги)
        :param i: Слово, которое нужно сравнить с базовым(без разложения на слоги)
        :return: True/False, рифма/не рифма
        """
        if self.bw_syllables[-1] == cw_syllables[-1] and list(self.bw[-2:-4:-1]) == list(i[-2:-4:-1]):
            return True

    def __compare_0_3(self, i):
        """
        Функция для сравнения слов при поиске рифмы.
        Сравнивает по три последние буквы.

        :param i: Слово, которое нужно сравнить с базовым(без разложения на слоги)
        :return: True/False, рифма/не рифма
        """
        if list(self.bw[-1:-4:-1]) == list(i[-1:-4:-1]):
            return True

    def __compare_0_4(self, i):
        """
        Функция для сравнения слов при поиске рифмы.
        Сравнивает по четыре последние буквы.

        :param i: Слово, которое нужно сравнить с базовым(без разложения на слоги)
        :return: True/False, рифма/не рифма
        """
        if list(self.bw[-1:-5:-1]) == list(i[-1:-5:-1]):
            return True

    def __get_all_rhymes(self):
        """
        Функция для нахождения всех вохможных рифм из исходных
        словарных баз.

        :return: Список с рифмами
        """
        output_rhymes_list = []
        # Цикл для перебора всех доступных слов
        for i in (BASE_OF_NOUNS + BASE_OF_VERBS + BASE_OF_PRONOUNS + BASE_OF_ADJECTIVES):
            # Проверка, исключающая попадание введенного пользователем слова в список с рифмами
            if i == self.bw:
                continue
            cw_syllables = Rhyme.__decomposition_into_syllables(i)
            # Блок try/except для перехвата IndexError, возникающего при оценке слишком коротких слов
            try:
                # Проверка кол-ва слогов в базовом слове(для выбора функции сравнения слов)
                if self.amount_bw_syllables == 1:
                    if self.__compare_1_0(cw_syllables):
                        output_rhymes_list.append(i)
                elif self.amount_bw_syllables == 2:
                    if self.__compare_1_2(cw_syllables, i):
                        output_rhymes_list.append(i)
                elif self.amount_bw_syllables == 3 and len(self.bw) <= 5:
                    if self.__compare_2_0(cw_syllables):
                        output_rhymes_list.append(i)
                    else:
                        if self.__compare_1_2(cw_syllables, i):
                            output_rhymes_list.append(i)
                else:
                    if self.__compare_2_0(cw_syllables):
                        output_rhymes_list.append(i)
                    else:
                        if self.__compare_1_2(cw_syllables, i):
                            output_rhymes_list.append(i)
                    # Блок сработает при пустом списке рифм
                    if not output_rhymes_list:
                        if self.__compare_0_4(i):
                            output_rhymes_list.append(i)
                    # Блок сработает при пустом списке рифм
                    if not output_rhymes_list:
                        if self.__compare_0_3(i):
                            output_rhymes_list.append(i)
            except IndexError:
                continue
        # Проверка на пустоту списка рифм
        if not output_rhymes_list:
            output_rhymes_list.append('*НЕТУ РИФМЫ*')
            # Запись слова без рифм с специальный файл(для дальнейшей отладки)
            with open('main/baseofwords/not_rhyme.txt', 'r+', encoding='utf-8') as file:
                if self.bw not in file.readlines():
                    file.write(self.bw)
                    file.write('\n')
        return output_rhymes_list

    def output(self):
        """
        Функция для вывода списка рифм из экземпляра.

        :return: Список с рифмами
        """
        return self.output_rhymes_list


class CompleteText:
    """
    Класс, отвечающий за генерацию текста.
    """
    def __init__(self, size_of_verse, amount_verse, amount_phrase_in_string, size_of_chorus, amount_words_in_string,
                 rhyme_type):
        """
        При создании экземпляра класса формирует готовый текст
        в формате списка.

        :param size_of_verse: Размер куплета(кол-во пар строк)
        :param amount_verse: Кол-во куплетов
        :param amount_phrase_in_string: Кол-во словосочетаний в строке куплета
        :param size_of_chorus: Размер припева(кол-во пар строк)
        :param amount_words_in_string: Кол-во слов в строке припева
        :param rhyme_type: Тип рифмы куплета('consistent' - последовательная, 'cross' - перекрестная)
        """
        self.size_of_verse = size_of_verse
        self.amount_verse = amount_verse
        self.amount_phrase_in_string = amount_phrase_in_string
        self.size_of_chorus = size_of_chorus
        self.amount_words_in_string = amount_words_in_string
        self.rhyme_type = rhyme_type
        self.amount_syllables_verse = 0
        self.amount_syllables_chorus = 0
        self.text = self.__generate_complete_text()

    @staticmethod
    def __generation_random_phrase():
        """
        Функция для создания случайного словосочетания.

        :return: Словосочетание в формате строки
        """
        phrase_type = choice(PHRASE_OPTIONS)
        phrase = choice(phrase_type[0]) + ' ' + choice(phrase_type[1])
        return phrase

    @staticmethod
    def __generation_rhyme_phrase(rhyme):
        """
        Функция для создания рифмованного словосочетания.

        :param rhyme: Второе слово(рифма)
        :return: Словосочетание в формате строки
        """
        phrase_type = choice(PHRASE_OPTIONS)
        phrase = choice(phrase_type[0]) + ' ' + rhyme
        return phrase

    @staticmethod
    def __syllables_counter(string):
        """
        Функция для подсчёта кол-ва слогов в строке.

        :param string: Строка, которую надо посчитать
        :return: Кол-во слогов
        """
        amount_syllables = 0
        for _ in string:
            if _ in 'аеёиоуыэюяАЕЁИОУЫЭЮЯ':
                amount_syllables += 1
        return amount_syllables

    def __generation_first_string_for_verse(self):
        """
        Функция генерации первой строки в куплете.
        Первая строка задает директивный размер для
        последующих.

        :return: Рандомная строка рандомного размера
        """
        output_string = []
        for _ in range(self.amount_phrase_in_string):
            output_string.append(CompleteText.__generation_random_phrase())
        output_string = ' '.join(output_string)
        self.amount_syllables_verse = CompleteText.__syllables_counter(output_string)
        return output_string

    def __generation_not_rhyme_string_for_verse(self):
        """
        Функция генерации нерифмованной строки куплета.

        :return: Рандомная строка необходимого размера
        """
        output_string = []
        # Цикл для подбора строки по директивному размеру
        for _ in range(1000):
            for _ in range(self.amount_phrase_in_string):
                output_string.append(CompleteText.__generation_random_phrase())
            # Сопоставление размеров
            if (self.amount_syllables_verse - 1) <= CompleteText.__syllables_counter(''.join(output_string)) <= \
                    (self.amount_syllables_verse + 1):
                break
            else:
                output_string = []
        else:
            output_string = ['*НЕ УДАЛОСЬ СФОРМИРОВАТЬ СТРОКУ*', ]
        return ' '.join(output_string)

    def __generation_rhyme_string_for_verse(self, rhyme):
        """
        Функция генерации рифмованной строки куплета.

        :param rhyme: Слово, к которому будет рифмоваться строка
        :return: Рандомная рифмованная строка необходимого размера
        """
        # Подбор словосочетания с рифмой(весь список переворачивается при возврате функции)
        output_string = [CompleteText.__generation_rhyme_phrase(choice(Rhyme(rhyme).output()))]
        # Цикл для подбора элементов строки(кроме рифмы) по директивному размеру
        for _ in range(1000):
            for _ in range(self.amount_phrase_in_string - 1):
                output_string.append(CompleteText.__generation_random_phrase())
            # Сопоставление размеров
            if (self.amount_syllables_verse - 1) <= CompleteText.__syllables_counter(''.join(output_string)) <= \
                    (self.amount_syllables_verse + 1):
                break
            else:
                output_string = output_string[:1]
        else:
            output_string = ['*НЕ УДАЛОСЬ СФОРМИРОВАТЬ СТРОКУ*', ]
        return ' '.join(output_string[::-1])

    def __generation_first_string_for_chorus(self):
        """
        Функция генерации первой строки в припеве.
        Первая строка задает директивный размер для
        последующих.

        :return: Рандомная строка рандомного размера
        """
        output_string = []
        for _ in range(self.amount_words_in_string):
            output_string.append(choice(BASE_OF_NOUNS + BASE_OF_VERBS + BASE_OF_PRONOUNS + BASE_OF_ADJECTIVES))
        output_string = ' '.join(output_string)
        self.amount_syllables_chorus = CompleteText.__syllables_counter(output_string)
        return output_string

    def __generation_not_rhyme_string_for_chorus(self):
        """
        Функция генерации нерифмованной строки припева.

        :return: Рандомная строка необходимого размера
        """
        output_string = []
        # Цикл для подбора строки по директивному размеру
        for _ in range(1000):
            for _ in range(self.amount_words_in_string):
                output_string.append(choice(BASE_OF_NOUNS + BASE_OF_VERBS + BASE_OF_PRONOUNS + BASE_OF_ADJECTIVES))
            # Сопоставление размеров
            if (self.amount_syllables_chorus - 1) <= CompleteText.__syllables_counter(''.join(output_string)) <= \
                    (self.amount_syllables_chorus + 1):
                break
            else:
                output_string = []
        else:
            output_string = ['*НЕ УДАЛОСЬ СФОРМИРОВАТЬ СТРОКУ*', ]
        return ' '.join(output_string)

    def __generation_rhyme_string_for_chorus(self, rhyme):
        """
        Функция генерации рифмованной строки припева.

        :param rhyme: Слово, к которому будет рифмоваться строка
        :return: Рандомная рифмованная строка необходимого размера
        """
        # Подбор рифмы(весь список переворачивается при возврате функции)
        output_string = [choice(Rhyme(rhyme).output())]
        # Цикл для подбора элементов строки(кроме рифмы) по директивному размеру
        for _ in range(1000):
            for _ in range(self.amount_words_in_string - 1):
                output_string.append(choice(BASE_OF_NOUNS + BASE_OF_VERBS + BASE_OF_PRONOUNS + BASE_OF_ADJECTIVES))
            # Сопоставление размеров
            if (self.amount_syllables_chorus - 1) <= CompleteText.__syllables_counter(''.join(output_string)) <= \
                    (self.amount_syllables_chorus + 1):
                break
            else:
                output_string = output_string[:1]
        else:
            output_string = ['*НЕ УДАЛОСЬ СФОРМИРОВАТЬ СТРОКУ*', ]
        return ' '.join(output_string[::-1])

    def __generation_verse_consistent_rhyme(self):
        """
        Функция генирации куплета с последовательной рифмой.

        :return: Куплет в формате списка
        """
        if self.amount_syllables_verse == 0:
            verse = [self.__generation_first_string_for_verse()]
        else:
            verse = [self.__generation_not_rhyme_string_for_verse()]
        for _ in range(self.size_of_verse):
            if len(verse) == 1:
                rhyme = verse[-1].split(' ')[-1]
                verse.append(self.__generation_rhyme_string_for_verse(rhyme))
            else:
                verse.append(self.__generation_not_rhyme_string_for_verse())
                rhyme = verse[-1].split(' ')[-1]
                verse.append(self.__generation_rhyme_string_for_verse(rhyme))
        return verse

    def __generation_verse_cross_rhyme(self):
        """
        Функция генирации куплета с перекрёстной рифмой.

        :return: Куплет в формате списка
        """
        if self.amount_syllables_verse == 0:
            verse = [self.__generation_first_string_for_verse()]
        else:
            verse = [self.__generation_not_rhyme_string_for_verse()]
        for _ in range(self.size_of_verse // 2):
            if len(verse) == 1:
                verse.append(self.__generation_not_rhyme_string_for_verse())
                rhyme1 = verse[-2].split(' ')[-1]
                rhyme2 = verse[-1].split(' ')[-1]
                verse.append(self.__generation_rhyme_string_for_verse(rhyme1))
                verse.append(self.__generation_rhyme_string_for_verse(rhyme2))
            else:
                verse.append(self.__generation_not_rhyme_string_for_verse())
                verse.append(self.__generation_not_rhyme_string_for_verse())
                rhyme1 = verse[-2].split(' ')[-1]
                rhyme2 = verse[-1].split(' ')[-1]
                verse.append(self.__generation_rhyme_string_for_verse(rhyme1))
                verse.append(self.__generation_rhyme_string_for_verse(rhyme2))
        return verse

    def __generation_chorus(self):
        """
        Функция генерации припева.

        :return: Припев в формате списка
        """
        chorus = [self.__generation_first_string_for_chorus()]
        for _ in range(self.size_of_chorus):
            if len(chorus) == 1:
                rhyme = chorus[-1].split(' ')[-1]
                chorus.append(self.__generation_rhyme_string_for_chorus(rhyme))
            else:
                chorus.append(self.__generation_not_rhyme_string_for_chorus())
                rhyme = chorus[-1].split(' ')[-1]
                chorus.append(self.__generation_rhyme_string_for_chorus(rhyme))
        return chorus

    def __generate_complete_text(self):
        """
        Функция генерации готового текста.

        :return: Текст в формате списка
        """
        output_text = []
        number_of_verse = 0
        for _ in range(self.amount_verse):
            number_of_verse += 1
            output_text.append(['Куплет {}:'.format(number_of_verse), ])
            if self.rhyme_type == 'consistent':
                output_text.append(self.__generation_verse_consistent_rhyme())
            elif self.rhyme_type == 'cross':
                output_text.append(self.__generation_verse_cross_rhyme())
            output_text.append(['', ])
        output_text.append(['Припев:', ])
        output_text.append(self.__generation_chorus())
        return output_text

    def output(self):
        """
        Функция для вывода текста

        :return: Текст в формате списка
        """
        return self.text
