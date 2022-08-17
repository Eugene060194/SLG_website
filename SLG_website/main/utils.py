import os  # Для создания списка файлов в директории
import json  # Для работы с сохраненными/сохраняемыми текстами
from string import ascii_letters, digits  # Списки символов
from random import sample  # Метод генерации случайной строки


def generate_number():
    """ы
    Функция создания идентификатора сгенерированного текста.

    :return: Случайная число-буквенная строка из 8 символов
    """
    symbols = ascii_letters + digits
    return ''.join(sample(symbols, 8))


def read_saved_text(directory_path):
    """
    Функция для прочтения сохраненного текста.

    :param directory_path: Директория, из которой необходимо прочитать тексты
    :return: Список прочитанных текстов
    """
    read_texts = []
    for filename in os.listdir(directory_path):
        with open('{}/{}'.format(directory_path, filename), 'r') as file:
            read_texts.append(json.load(file))
    return read_texts


def save_text(user, number, text):
    """
    Функция для сохранения текста.

    :param user: Имя пользователя, для сохранения текста в его директорию
    :param number: Номер текста(добавляется в название)
    :param text: Текст в формате списка
    :return: -
    """
    with open('main/savedtexts/{}/usertext_{}.txt'.format(user, number), 'w') as file:
        json.dump(text, file, ensure_ascii=False)
