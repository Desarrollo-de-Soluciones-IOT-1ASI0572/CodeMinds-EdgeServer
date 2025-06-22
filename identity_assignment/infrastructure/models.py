from peewee import Model, AutoField, CharField, ForeignKeyField, DateTimeField
from shared.infrastructure.database import db

class StudentModel(Model):
    """ORM model for the 'students' table."""

    id = AutoField()
    name = CharField()
    last_name = CharField()
    home_address = CharField()
    school_address = CharField()
    student_photo_url = CharField()
    parent_profile_id = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'students'


class WristbandModel(Model):
    """ORM model for the 'wristbands' table."""

    id = AutoField()
    rfid_code = CharField(unique=True)
    wristband_status = CharField()  # E.g., 'ACTIVE', 'INACTIVE'
    student = ForeignKeyField(StudentModel, backref='wristbands')
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'wristbands'
