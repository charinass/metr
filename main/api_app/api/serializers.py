from rest_framework import serializers
from api_app.models import DeviceModel


class DeviceSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()                      # Device ID (Integer)
    device_manufacturer = serializers.CharField()               # Device manufacturer (Char)
    device_type = serializers.CharField()                       # Device type (Char)
    device_version = serializers.CharField()                    # Device version (Char)
    message_date_time = serializers.CharField()                 # Date and time of the message (Char)
    measurement_dimension = serializers.CharField()             # The dimension of the measurement (Char)
    value_new_measurement = serializers.CharField()             # Value of new measurement (Char)
    value_measurement_in_duedate = serializers.CharField()      # Value of the measurement in the due date (Char)
    due_date = serializers.CharField()                          # Date of the due date (Char)
    
    def create(self, validated_data):
        return DeviceModel.objects.create(**validated_data)