from django.db import models

# Create your models here.


class BlessLimit(models.Model):
    value = models.PositiveIntegerField(null=False, blank=False, default=5)

    class Meta:
        db_table = 'BlessLimit'
