# from django.shortcuts import render
# from api_app.models import Device
# from django.http import JsonResponse

# # Create your views here.
# def device_list(request):
#     devices = Device.objects.all()
#     data = {
#         'data': list(devices.values())
#         }
#     return JsonResponse(data)

# def device_details(request, pk):
#     device = Device.objects.get(pk=pk)
#     data = {
#         'device name': device.device_name,
#         'device manufacturer': device.device_mf
#     }
#     return JsonResponse(data)