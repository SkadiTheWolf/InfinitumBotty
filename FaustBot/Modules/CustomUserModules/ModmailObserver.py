from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot import logger


class ModmailObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".modmail"]

    @staticmethod
    def help():
        return ".modmail <msg> - Sendet allen Moderatoren <msg> per PN"

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".modmail"):
            mods = connection.details.get_mods()
            logger.info(f"mods: {mods}")
            message = data["message"].split(".modmail ")[1]
            for mod in mods:
                connection.send_to_user(mod, f"{data['nick']} meldet: {message}")
