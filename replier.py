import logging
from utils import Command, CommType, wrap_t


class Replier:
    def __init__(self, bot, default, *actions):
        about = Command(pattern='/help', help='/help - помощь', action=self._about, type=CommType.text)
        trigger = Command(pattern='/trigger', help='/trigger - включает или выключает бот', action=self._trigger,
                        type=CommType.text)

        self._bot = bot
        self._default = default
        self._commands = [about, default] + list(actions) + [trigger]

        self._log = logging.getLogger('messages')
        hdlr = logging.FileHandler('log/messages.log')
        hdlr.setFormatter(logging.Formatter('%(asctime)s:  %(message)s'))
        self._log.addHandler(hdlr)
        self._log.setLevel(logging.INFO)
        self._active = True

    def _trigger(self, message):
        self._active = not self._active
        return wrap_t('ЩА ОБОРУ ТЕБЯ' if self._active else 'Бот выключен')

    def _about(self, message):
        return wrap_t('Орущий бот\n' + '\n'.join([c.help for c in self._commands]))

    def reply(self, update):
        chat_id = update.message.chat_id
        message = update.message.text

        if message:
            msg = message.lower()
            for i in self._commands:
                if i.pattern in msg:
                    command = i
                    break
            else:
                command = self._default

            msg = command.action(msg)

            if self._active and msg:
                if command.type == CommType.text:
                    self._bot.sendMessage(chat_id, **msg)
                elif command.type == CommType.voice:
                    self._bot.sendVoice(chat_id, **msg)

                self._log.info(message+': '+str(msg))
            return update.update_id + 1