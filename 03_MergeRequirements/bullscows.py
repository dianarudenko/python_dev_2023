from random import choice
from argparse import ArgumentParser
import os
from urllib import request

def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for i in range(len(guess)):
        if i < len(secret) and guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    if valid:
        while not word in valid:
            print('Плохое слово, попробуйте снова')
            word = input(prompt)
    else:
        while len(word) != args.length:
            print(f'Слово должно быть длины {args.length}, попробуйте снова')
            word = input(prompt)
    return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
    

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    answer = choice(words)
    bulls = 0
    count = 0
    while bulls != len(answer):
        guess = ask('Введите слово: ')
        bulls, cows = bullscows(guess, answer)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        count += 1
    return count

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dict', type=str, help='Name or URL of file with the dictionary')
    parser.add_argument('length', type=int, nargs='?', default=5)
    args = parser.parse_args()

    dictionary = []
    if os.path.exists(args.dict):
        with open(args.dict) as inp:
            dictionary = inp.read().split()
    else:
        try:
            with request.urlopen(args.dict) as inp:
                dictionary = inp.read().decode('utf-8').split()
        except:
            print('Невалидная URL')
    dictionary = [word for word in dictionary if len(word) == args.length]
    if dictionary == []:
        print('Пустой словарь доступных слов, игра невозможна')
    else:
        attempts = gameplay(ask, inform, dictionary)
        print(f'Победа! Потребовалось попыток: {attempts}')
    