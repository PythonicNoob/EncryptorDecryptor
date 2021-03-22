from django.db import models
import uuid
# Create your models here.

class data(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    data = models.CharField(max_length=526)
    password = models.CharField(max_length=50)
    encrypt = models.BooleanField(editable=False)

    def __str__(self):
        return self.data