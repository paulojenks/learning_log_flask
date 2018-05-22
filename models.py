from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=100)
    date = DateField()
    time_spent = CharField(max_length=255)
    what_i_learned = CharField(max_length=1000)
    resources_to_remember = CharField(max_length=1000)

    class Meta:
        database = DATABASE
        order_by = ('-date',)

    @classmethod
    def create_entry(cls, title, date, time_spent, what_i_learned, resources_to_remember):
        cls.create(
            title=title,
            date=date,
            time_spent=time_spent,
            what_i_learned=what_i_learned,
            resources_to_remember=resources_to_remember
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()