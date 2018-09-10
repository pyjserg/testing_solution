import sqlite3
from typing import Tuple, Union
from contextlib import closing


# noinspection SqlResolve
class DataBaseLibrary(object):
    """
    A test library providing keywords for SQLite database operations.

    ``DataBaseLibrary`` is Robot Framework's custom library that provides a
    set of keywords for working with SQLite database of the specific test application.

    The library contains following keywords:

    | = Keyword Name =                                              | = Comment = |
    | `Connect To The Database                                      | Creates a connection to specific database
    | `Close Database Connection`                                   | Closes opened connection
    | `Get Id And Balance of Client With Positive Balance`          | Returns ID and balance of the client with positive
                                                                    | balance if the client exists, creates the client
                                                                    | with positive balance and returns one's ID and
                                                                    | balance otherwise.

    | `Get Id And Balance of Existed Client With Positive Balance`  | Returns ID and balance of the client if the client
                                                                    | with positive balance exists, None otherwise.

    | `Add New Client`                                              | Inserts into the database new entries with the
                                                                    | client name and one's balance and returns client
                                                                    | ID and balance value.

    | `Get The Client Balance`                                      | Returns balance value of the client with specific
                                                                    | ID.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def connect_to_the_database(self, db_file_name: str) -> None:
        """
        The method creates a connection to the  sqlite database file.
        :param db_file_name: str, should contain full or relative file path
        :return: None
        """
        self.connection = sqlite3.connect(database=db_file_name)
        self.cursor = self.connection.cursor()

    def close_database_connection(self):
        """
        Teardown method which closes opened connection to database.
        :return: None
        """
        with closing(self.connection):
            pass

    def get_id_and_balance_of_client_with_positive_balance(self) -> Union[Tuple, None]:
        """
        The method returns ID and balance value of the client with positive balance. If client with positive
        balance doesn't exist the corresponding entry will be created.
        :return: tuple (client_id, balance_value) or None
        """

        data = self.get_id_and_balance_of_existed_client_with_positive_balance()
        return data if data else self.add_new_client('John Doe', 10)

    def get_id_and_balance_of_existed_client_with_positive_balance(self) -> Union[Tuple, None]:
        """
        The method returns ID and balance value of the client with positive balance if the corresponding entries exist,
        None otherwise.
        :return: tuple (client_id, balance_value) or None
        """
        response = self.cursor.execute('SELECT CLIENTS_CLIENT_ID, BALANCE FROM BALANCES WHERE BALANCE > 0 LIMIT 1')
        data = response.fetchall()
        return data[0] if data else None

    def add_new_client(self, client_name: str, client_balance: int) -> Tuple:
        """
        The method creates new entries in the database with the client name and balance value and checks
        inserted data for existence.
        :param client_name: str
        :param client_balance: int
        :return: tuple
        """
        self.cursor.execute(f"INSERT INTO CLIENTS (CLIENT_NAME) VALUES ('{client_name}')")
        self.cursor.execute(f'INSERT INTO BALANCES (BALANCE) VALUES ({client_balance})')
        self.connection.commit()

        response = self.cursor.execute(
            f"""
            SELECT C.CLIENT_ID, B.BALANCE
            FROM CLIENTS C JOIN BALANCES B
            WHERE C.CLIENT_NAME = '{client_name}' AND B.BALANCE = {client_balance}
            """
        )
        data = response.fetchall()
        if data:
            return data[0]
        else:
            raise ValueError("Couldn't get ID and BALANCE of a new client. Something went wrong during inserting data"
                             " into the database.")

    def get_the_client_balance(self, client_id: int) -> int:
        """
        The method returns balance value of the client with specific ID. Raises Lookup error if the wanted entry
        doesn't exist.
        :param client_id: int
        :return: int
        """
        response = self.cursor.execute(f'SELECT BALANCE FROM BALANCES WHERE CLIENTS_CLIENT_ID={client_id}')
        data = response.fetchall()
        if data:
            return data[0][0]
        else:
            raise LookupError(f"Couldn't get balance of the client with ID={client_id}. No such entry.")
