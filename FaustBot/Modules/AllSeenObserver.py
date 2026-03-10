import datetime
import time
from collections import defaultdict
from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Modules.UserList import UserList
from FaustBot import logger


class AllSeenObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".allseen"]

    @staticmethod
    def help():
        return ".allseen - um abzufragen, wann alle im Channel zuletzt aktiv waren (Nur von Moderatoren nutzbar)"

    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".allseen") and self._is_idented_mod(
            data, connection
        ):
            User_afk = defaultdict(int)
            for who in self.user_list.userList.keys():
                user_provider = UserProvider()
                activity = user_provider.get_activity(who)
                delta = time.time() - activity
                User_afk[who] = delta
                logger.info(f"{who} - {delta}")
            for afk_user in sorted(User_afk, key=User_afk.get):
                output = (
                    f"{afk_user}: {str(datetime.timedelta(seconds=User_afk[afk_user]))}"
                )
                connection.send_back(output, data)

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data["nick"] in self._config.mods and connection.is_idented(data["nick"])
