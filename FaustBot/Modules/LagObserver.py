from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Modules.PongObserverPrototype import PongObserverPrototype
from time import time, sleep
from FaustBot import logger
import _thread


class LagObserver(PrivMsgObserverPrototype, PongObserverPrototype):
    ping_time = 0
    last_periodic_ping = time()

    def __init__(self, _connection):
        super().__init__()
        self._connection = _connection
        _thread.start_new_thread(self.setup_timer, ())

    @staticmethod
    def cmd():
        return [".lag"]

    @staticmethod
    def help():
        return ".lag - zeige den aktuellen Lag vom Bot zum IRC-Server an"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if (
            data["message"].startswith(".lag")
            and data["nick"] in self._config.mods
            and connection.is_idented(data["nick"])
        ):
            sleep(1.2345)
            self.ping_time = time()
            connection.raw_send("PING :lag.check")

    def update_on_pong(self, data: dict, connection: Connection):
        if data["message"] == ":lag.check":
            pong_time = time()
            delta_time = (pong_time - self.ping_time) * 100000
            connection.send_channel(f"Current-Lag: {int(delta_time) / 100}ms")
        elif data["message"] == ":periodic.ping":
            logger.debug("Got Periodic Pong")
        else:
            logger.debug(f"Received an unknown Pong ({data['message']})")

    def periodic_ping(self):
        self._connection.raw_send("PING :periodic.ping")
        logger.debug("Sent Periodic Ping")

    def setup_timer(self):
        _interval = 55
        while True:
            # logger.error(f"Running Anti-Lag Timer with Interval {_interval}")
            sleep(_interval)
            try:
                self.periodic_ping()
            except Exception as e:
                logger.error(e)
