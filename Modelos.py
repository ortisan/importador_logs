from peewee import *

db = MySQLDatabase(
    'logs_appgratis',  # Required by Peewee.
    user='root',  # Will be passed directly to psycopg2.
    password='Senha@123!',  # Ditto.
    host='localhost',  # Ditto.
)


class Log(Model):
    ip = CharField()
    data = DateTimeField()
    url = CharField()
    method = CharField()
    status_code = IntegerField()
    dados_device = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    # Connect to our database.
    db.connect()

    # Create the tables.
    db.create_tables([Log])

    #use python Modelos.py
