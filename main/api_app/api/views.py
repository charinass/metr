from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import io
import csv
from api_app.models import DeviceModel
from api_app.api.serializers import DeviceSerializer


############################################
# Name: commit
# Operations: POST
# Parameters: JSON formatted OMS-Data from metr gateway described in the following URL
#               https://metr.slite.com/p/note/2t5tiXMp5un9wVEY7PXjeu
# Function description: Save data to sqlite database
############################################
@api_view(['POST'])
def commit(request):
    if request.method == 'POST':

        # Retrieve the POSTed data
        data = request.data

        data_dict = {}

        # Parse the incoming JSON data
        try:
            data_dict["device_id"] = data["device"]["identnr"]
            data_dict["device_manufacturer"] = str(data["device"]["manufacturer"])
            data_dict["device_type"] = str(data["device"]["type"])
            data_dict["device_version"] = str(data["device"]["version"])
            data_dict["measurement_dimension"] = str(data["data"][1]["dimension"])
            data_dict["value_new_measurement"] = str(data["data"][1]["value"])
            data_dict["value_measurement_in_duedate"] = str(data["data"][3]["value"])

            # Convert "Date of the due date" to human-readable format "YYYY.MM.DD"
            data_dict["due_date"] = str(data["data"][2]["value"]).split('T')[0].replace("-",".")

            # Convert "Date and time of the message" to human-readable format "YYYY.MM.DD hh:mm:ss.ssssss"
            data_dict["message_date_time"] = str(data["data"][0]["value"]).split('T')[0].replace("-",".") + " " + str(data["data"][0]["value"]).split('T')[1]

        except KeyError:
            # Exception for invalid JSON
            return Response("Invalid JSON format.")

        # Convert the parsed data in a model
        serializer = DeviceSerializer(data=data_dict)

        if serializer.is_valid():
            # Save the model if validation check is passed
            serializer.save()
            return Response("Committed to database.")
        else:
            return Response("Invalid JSON format.")


############################################
# Name: export
# Operations: GET
# Parameters: None
# Function description: Download a CSV file with the last message for each device
############################################
@api_view(['GET'])
def export(request):
    serializer = []

    # ---
    # Another way to filter the latest entry for each device using raw SQL query
    # Not sure which way is better without testing with actual data
    # ---
    #
    # devices = DeviceModel.objects.raw('''SELECT main.* FROM api_app_devicemodel AS main WHERE message_date_time = (
    # SELECT MAX(message_date_time) FROM api_app_devicemodel AS sub WHERE main.device_id = sub.device_id
    # );
    # ''')

    # Get the latest entry for each device
    for each_device in DeviceModel.objects.values('device_id').distinct():
        # print(each_device['device_id'])
        device = DeviceModel.objects.filter(device_id=each_device['device_id']).latest('message_date_time')
        serializer.append(DeviceSerializer(device))

    # Convert to JSON string
    json_data = [serializer[i].data for i in range(len(serializer))]

    # CSV header definition
    csv_header = ['Device ID', 'Device manufacturer', 'Device type', 'Device version', 'Message date time',
                  'Measurement dimension', 'Value new measurement', 'Value measurement in due date', 'Due date']

    csv_data = io.StringIO()
    wr = csv.writer(csv_data, delimiter=',')

    # Write the csv header
    wr.writerow(csv_header)

    # Write the csv data
    for item in json_data:
        wr.writerow([item['device_id'], item['device_manufacturer'], item['device_type'], item['device_version'], item['message_date_time'],
                     item['measurement_dimension'], item['value_new_measurement'],
                     item['value_measurement_in_duedate'], item['due_date']])

    # Move back the pointer to 0
    csv_data.seek(0)

    # CSV file name definition
    csv_file_name = 'OMS-Data.csv'

    # Trigger file download
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={csv_file_name}'

    return response