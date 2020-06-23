from django.db import models

# Create your models here.
class News(models.Model):
    id = models.TextField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.TextField()
    subtitle = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)  # This field type is a guess.
    img = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NEWS'


class Test(models.Model):
    id = models.TextField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    word = models.TextField(blank=True, null=True)  # This field type is a guess.
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'