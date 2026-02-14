import sqlite3

class CommandsProvider(object):
    _CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY, \
                    command TEXT, reaction TEXT)'
    _GET_REACTION = 'SELECT id, reaction FROM commands WHERE command = ?'
    _SAFE_OR_OVERWRITE = 'REPLACE INTO commands (id, command, reaction) VALUES (?, ?, ?)'
    _DELETE_COMMAND = 'DELETE FROM commands WHERE command = ?'

    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(CommandsProvider._CREATE_TABLE)
        self._database_connection.commit()

    def get_command(self, command: str):
        cursor = self._database_connection.cursor()
        cursor.execute(CommandsProvider._GET_REACTION, (command.lower(),))
        return cursor.fetchone()

    def save_or_replace(self, command: str, reaction: str):
        existing = self.get_command(command)
        id = existing[0] if existing is not None else None
        data = (id, command.lower(), reaction)
        cursor = self._database_connection.cursor()
        cursor.execute(CommandsProvider._SAFE_OR_OVERWRITE, data)
        self._database_connection.commit()

    def delete_command(self, command: str):
        cursor = self._database_connection.cursor()
        cursor.execute(CommandsProvider._DELETE_COMMAND, (command.lower(),))

    def __exit__(self):
        self._database_connection.close()