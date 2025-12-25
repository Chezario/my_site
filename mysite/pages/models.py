from django.db import models


class Room(models.Model):
    room_number = models.IntegerField(default=0)
    describe = models.CharField(max_length=30)


class Printers(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    printer_manufacturer = models.CharField(max_length=20)
    printer_model = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')