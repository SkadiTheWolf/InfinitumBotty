import sqlite3


class DucksProvider(object):
    _CREATE_TABLE = "CREATE TABLE IF NOT EXISTS ducks (id INTEGER PRIMARY KEY, \
        user TEXT, friends INTEGER, dead INTEGER)"
    _GET_DUCKS = "SELECT id, friends, dead FROM ducks WHERE user = ?"
    _SAVE_OR_OVERWRITE = "REPLACE INTO ducks (id, user, friends, dead) VALUES (?, ?, ?,?)"
    _DELETE_DUCKS = "DELETE FROM ducks WHERE user = ?"
    _GET_NICK = "SELECT count(*) FROM ducks WHERE user = ?"

    def __init__(self):
        self._database_connection = sqlite3.connect("faust_bot.db")
        cursor = self._database_connection.cursor()
        cursor.execute(DucksProvider._CREATE_TABLE)
        self._database_connection.commit()

    def get_ducks(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(DucksProvider._GET_DUCKS, (user.lower(),))
        return cursor.fetchone()

    def save_or_replace(self, user: str, friends: int, dead: int):
        existing = self.get_ducks(user)
        _id = existing[0] if existing is not None else None
        data = (_id, user.lower(), friends, dead)
        cursor = self._database_connection.cursor()
        cursor.execute(DucksProvider._SAVE_OR_OVERWRITE, data)
        self._database_connection.commit()

    def delete_score(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(DucksProvider._DELETE_DUCKS, (user.lower(),))
        self._database_connection.commit()

    def get_nick(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(DucksProvider._GET_NICK, (user.lower(),))
        return cursor.fetchone()
    
    def transfer_ducks(self, data, user: str, number, notAll):
        cursor = self._database_connection.cursor()
        toDuckData = self.get_ducks(user)
        fromDuckData = self.get_ducks(data['nick'].lower())

        to_id = toDuckData[0]
        from_id = fromDuckData[0]

        fromNick = data['nick'].lower()
        toFriends = number
        if notAll:
            toDead = fromDuckData[2]
        else:
            toDead = fromDuckData[2] + toDuckData[2]

        # cursor.execute(DucksProvider._DELETE_DUCKS, (user,))
        if notAll:
            cursor.execute(DucksProvider._SAVE_OR_OVERWRITE, (from_id, fromNick, fromDuckData[1]-number, toDead,))
            cursor.execute(DucksProvider._SAVE_OR_OVERWRITE, (to_id, user, toDuckData[1]+number, toDead,))
    
        else: 
            cursor.execute(DucksProvider._SAVE_OR_OVERWRITE, (from_id, fromNick, 0, 0,))
            cursor.execute(DucksProvider._SAVE_OR_OVERWRITE, (to_id, user, number+toDuckData[1] , toDead, ))

        self._database_connection.commit()


    def __exit__(self):
        self._database_connection.close()
