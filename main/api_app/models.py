from django.db import models


# Create your models here.
class DeviceModel(models.Model):
    device_id = models.IntegerField(default=0)                              # Device ID
    device_manufacturer = models.CharField(max_length=20)                   # Device manufacturer
    device_type = models.CharField(max_length=20)                           # Device type
    device_version = models.CharField(max_length=20)                        # Device version
    message_date_time = models.CharField(max_length=26)                     # Date and time of the message
    measurement_dimension = models.CharField(max_length=20)                 # The dimension of the measurement
    value_new_measurement = models.CharField(max_length=20)                 # Value of new measurement
    value_measurement_in_duedate = models.CharField(max_length=10)           # Value of the measurement in the due date
    due_date = models.CharField(max_length=20)                              # Date of the due date

    def __str__(self):
        return str(self.device_id)

