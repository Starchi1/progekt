import sqlite3


class DbHelper:
    def __init__(self):
        self.connection = sqlite3.connect('BASDT.db')

    def request(self, request, params=None):
        # Вернёт True, если всё окей, если будут ошибки - вернёт False
        try:
            cursor = self.connection.cursor()
            if not params:
                cursor.execute(request)
            else:
                cursor.execute(request, params)
            self.connection.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def __del__(self):
        # Когда класс перестаёт использоваться, то надо подключение закрыть
        self.connection.close()
