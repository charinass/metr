from django.test import TestCase
import requests


test_data = """
{
  "data":[
     {
        "value":"2021-10-12T00:00:00.000000",
        "tariff":0,
        "subunit":0,
        "dimension":"Time Point (time & date)",
        "storagenr":0
     },
     {
        "value":29600,
        "tariff":0,
        "subunit":0,
        "dimension":"Energy (kWh)",
        "storagenr":0
     },
     {
        "value":"2021-10-30T00:00:00.000000",
        "tariff":0,
        "subunit":0,
        "dimension":"Time Point (date)",
        "storagenr":1
     },
     {
        "value":16274,
        "tariff":0,
        "subunit":0,
        "dimension":"Energy (kWh)",
        "storagenr":1
     }
  ],
  "device":{
     "type":4,
     "status":0,
     "identnr":80337,
     "version":0,
     "accessnr":150,
     "manufacturer":5317
  }
}
"""


class ViewsTestCase(TestCase):
    # Test case for "commit"
    def test_commit_api_loads_properly(self):
        url = "http://localhost:8000/commit"
        session = requests.session()

        headers = {'Content-type': 'application/json'}
        result = session.post(url, data=test_data, headers=headers)

        print(str(result.status_code) + ":" + result.text)

        self.assertEqual(result.status_code, 200)

    # Test case for "export"
    def test_export_api_loads_properly(self):
        url = "http://127.0.0.1:8000/export"
        session = requests.session()

        result = session.get(url)

        print(result.text)

        self.assertEqual(result.status_code, 200)