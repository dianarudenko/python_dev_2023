def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for i in range(min(len(guess), len(secret))):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1
    return bulls, cows