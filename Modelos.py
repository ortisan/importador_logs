from peewee import *

# db = MySQLDatabase(
#     'logs_appgratis4',
#     user='root',
#     password='Senha@123!',
#     host='localhost',
#     threadlocals=True
# )

db = MySQLDatabase(
    'logs_appgratis',
    user='root',
    password='Senha@123!',
    host='localhost',
    threadlocals=True
)


class Log(Model):
    id = CharField(primary_key=True)
    ip = CharField()
    data = DateTimeField()
    url = CharField()
    method = CharField()
    status_code = IntegerField()
    dados_device = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Log])

    # use python Modelos.py
