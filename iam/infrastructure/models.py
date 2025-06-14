from peewee import CharField, DateTimeField, Model
from shared.infrastructure.database import db
from datetime import datetime

class Device(Model):
    rfid_code = CharField(unique=True)    # Generado automáticamente
    api_key = CharField(unique=True)      # Token de autenticación
    student_name = CharField(null=True)
    registered_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
