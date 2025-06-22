from peewee import Model, AutoField, CharField, ForeignKeyField, DateTimeField
from shared.infrastructure.database import db

class StudentModel(Model):
    """ORM model for the students table."""
    id = AutoField()
    name = CharField()
    last_name = CharField()
    home_address = CharField()
    school_address = CharField()
    student_photo_url = CharField()

    parent_profile_id = CharField()  # Aquí usas el parent_profile_id

    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'students'  # Definimos el nombre de la tabla en la base de datos

class WristbandModel(Model):
    """ORM model for the wristbands table."""
    id = AutoField()
    rfid_code = CharField(unique=True)
    wristband_status = CharField()  # E.g., ACTIVE, INACTIVE
    student = ForeignKeyField(StudentModel, backref='wristbands')  # Asociamos con el estudiante

    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'wristbands'  # Definimos el nombre de la tabla en la base de datos

