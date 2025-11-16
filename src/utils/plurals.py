def plural_day(number):
    if 11 <= number % 100 <= 14:
        return f"{number} дней"
    elif number % 10 == 1:
        return f"{number} день"
    elif 2 <= number % 10 <= 4:
        return f"{number} дня"
    else:
        return f"{number} дней"


def plural_count(number):
    if 11 <= number % 100 <= 14:
        return f"{number} раз"
    elif number % 10 == 1:
        return f"{number} раз"
    elif 2 <= number % 10 <= 4:
        return f"{number} раза"
    else:
        return f"{number} раз"