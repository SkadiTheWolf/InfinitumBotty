import _thread

from FaustBot.Communication.Observable import Observable
from FaustBot import logger


class PongObservable(Observable):
    def input(self, raw_data, connection):
        _sender, _command, _server, _message = raw_data.split(" ")
        data = {
            "raw": raw_data,
            "server": _server,
            "sender": _sender,
            "message": _message,
            "command": _command,
        }
        if _command == "PONG":
            data["server"] = raw_data.split("PONG ")[1]
        else:
            return
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        # finde heraus, wer zurückgepingt werden muss, und ob das überhaupt ein ping-request ist oder ein user sich
        # einen spass erlaubt hat
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        # logger.debug(data)
        for observer in self._observers:
            _thread.start_new_thread(
                observer.__class__.update_on_pong, (observer, data, connection)
            )
