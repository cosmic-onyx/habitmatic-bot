import random
import string


digits = list(string.digits)
alphabets = list(string.ascii_letters)
special_chars = list("!@#$%^&*()")


def password_generator(length=8):
    length = int(length)

    password = []
    chars = []
    password_string = ""

    chars += digits
    chars += alphabets
    chars += special_chars

    for i in range(length):
        password.append(random.choice(chars))

    random.shuffle(password)

    for i in password:
        password_string += i

    return password_string