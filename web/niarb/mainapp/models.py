from django.db import models


class UserNote(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    username = models.CharField(max_length=32)
    category = models.CharField(max_length=16)
    status = models.CharField(max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_notes'
