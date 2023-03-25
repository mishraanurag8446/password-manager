import random
import string


def generatePassword(type='nsp', length=12):
    if type == 'n':
        return ''.join([random.choice(string.digits) for n in range(length)])
    elif type == 's':
        return ''.join([random.choice(string.ascii_letters) for n in range(length)])
    elif type == 'ns':
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(length)])
