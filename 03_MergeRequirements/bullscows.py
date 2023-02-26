from random import choice

def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for i in range(min(len(guess), len(secret))):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    if valid:
        while not word in valid:
            print('Невалидное слово, попробуйте снова')
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
    