import logging
import random
import re
from collections import namedtuple
from enum import Enum


def chance(ch):
    ret = random.randint(1, 100)
    logging.getLogger('messages').info('chance: ' + str(ret))
    return ret <= ch


class CommType(Enum):
    text = 't'
    voice = 'v'


def _len(message, *patterns):
    res = 0
    for i in patterns:
        ret = re.search(i, message)
        res += ret.span()[1] - ret.span()[0] if ret else 0
    return res


Command = namedtuple('Command', ['pattern', 'help', 'action', 'type'])


def wrap_t(value):
    return {'text': value}


def wrap_v(value):
    return {'voice': value}