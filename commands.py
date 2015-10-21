from utils import Command, CommType, wrap_t, wrap_v, chance, _len
from collections import namedtuple
import random
import json
import re


Trigger = namedtuple('Trigger', ['patterns', 'probability', 'answer'])


class ScreamCommand:
    def __init__(self, screams, prob, triggers, other_commands):
        self._screams = screams
        self._probability = prob
        self._triggers = triggers
        self._other_commands = [c for c in other_commands if c.type == CommType.text]

        self.pattern = '/scream'
        self.help = '/scream - просто орёт'
        self.action = lambda m: self.scream(m)
        self.type = CommType.text

    def scream(self, message):
        message = message.lower()
        scrms = [c.action(message)['text'] for c in self._other_commands] + self._screams

        def react():
            for t in self._triggers:
                if any(map(lambda p: re.search(message, p), t.patterns)):
                    return t.probability, t.answer
            return 0, None

        probability, reply = react()

        if self.pattern in message or chance(probability):
            return wrap_t(reply or random.choice(scrms))
        elif chance(self._probability):
            return wrap_t(random.choice(scrms))
        else:
            return None


def load(name):
    def func(c, msg):
        mm = {'msg': msg}
        exec(''.join(c['actions']), globals(), mm)
        return mm['result']

    with open(name, 'r') as f:
        map = json.load(f)

    commands = []
    for c in map['commands']:
        commands.append(Command(c['pattern'], c['help'], lambda msg, item=c: func(item, msg), CommType[c['type']]))


    s = ScreamCommand(map['scream']['screams'], map['scream']['probability'],
                      [Trigger(**t) for t in map['scream']['triggers']], commands)

    return s, commands
