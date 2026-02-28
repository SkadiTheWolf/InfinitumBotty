import sqlite3

class GoodQuotesProvider(object):
    _CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS quotes (votes INTEGER, quote TEXT)'
    _GET_TOP_QUOTE = 'SELECT MAX(votes), * FROM quotes'
    _GET_QUOTE = 'SELECT * FROM quotes WHERE quote = ?'
    _GET_VOTES = 'SELECT votes, quote FROM quotes WHERE quote = ?'
    _SAVE_OR_OVERWRITE = 'REPLACE INTO quotes (votes, quote) VALUES (?, ?)'
    _UPDATE_VOTES = 'UPDATE quotes SET votes = ? WHERE quote = ?'


    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(GoodQuotesProvider._CREATE_TABLE)
        self._database_connection.commit()

    def get_top_quote(self):
        """
        Get Quote with most Votes in Table. Return votes and quotes if it exists, None if not
        """
        cursor = self._database_connection.cursor()
        cursor.execute(GoodQuotesProvider._GET_TOP_QUOTE, ())
        entry = cursor.fetchone()
        try:
            votes = entry[0]
            quote = entry[2]
        except TypeError:
            return None
        return votes, quote

    def get_quote(self, quote):
        """
        Get a specific Quote, see if it exists in the Table
        """
        cursor = self._database_connection.cursor()
        cursor.execute(GoodQuotesProvider._GET_QUOTE, (quote,))
        quote = cursor.fetchone()
        if quote is not None:
            return True
        else:
            return False

    def get_votes(self, quote: str):
        """
        Get number of votes of Specific Quote
        """
        cursor = self._database_connection.cursor()
        cursor.execute(GoodQuotesProvider._GET_VOTES, (quote,))
        existing = cursor.fetchone()
        if existing is None:
            votes = 1
        else:
            votes = (existing[0])
        return votes

    def save_or_replace(self, quote: str, votes: int):
        """
        Safe Quote with votes and Quote if not existing
        """
        existing = self.get_quote(quote)
        data = (votes, quote)
        cursor = self._database_connection.cursor()
        if existing:
            cursor.execute(GoodQuotesProvider._SAVE_OR_OVERWRITE,data)
            self._database_connection.commit()
            return True
        else:
            cursor.execute(GoodQuotesProvider._SAVE_OR_OVERWRITE, data)
            self._database_connection.commit()
            return None

    def update_votes(self, quote: str):
        """
        Update votes if existing
        """
        cursor = self._database_connection.cursor()
        votes = self.get_votes(quote) + 1
        cursor.execute(GoodQuotesProvider._UPDATE_VOTES, (votes, quote))
        self._database_connection.commit()
        return

    def __exit__(self):
        self._database_connection.close()