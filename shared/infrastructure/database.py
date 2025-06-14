from peewee import SqliteDatabase

db = SqliteDatabase('rfid_events.db')  # Ruta relativa o absoluta

def init_db():
    from iam.infrastructure.models import RFIDEventModel
    db.connect()
    db.create_tables([RFIDEventModel], safe=True)
