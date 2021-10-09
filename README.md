
# OMS-Data collector/exporter

This is backend implementation to gather OMS-Data and to export a csv file. This is my solution to the code challenge.


# Development environment
|                    |Name                         |Version
|--------------------|-----------------------------|-----------|
|IDE                 |PyCharm Community Edition    |2021.2.2
|Database manager    |DBeaver Community Edition    |21.2.0
|Programing language |Python                       |3.9
|Database            |SQLite                       |3.0
|Frameworks          |Django                       |3.2.8
|                    |Django REST framework        |3.12.4

# REST API reference

## commit
Save the JSON formatted OMS-Data in database.

    [POST] /commit

### Parameters
|Name                |Type            |In             |Description
|--------------------|----------------|---------------|-----------------------
|OMS-Data            |string          |body           |JSON formatted OMS-Data

The expected JSON format is as follows.

    {
       "data":[
          {
             "value":"2020-06-26T06:49:00.000000",
             "tariff":0,
             "subunit":0,
             "dimension":"Time Point (time & date)",
             "storagenr":0
          },
          {
             "value":29690,
             "tariff":0,
             "subunit":0,
             "dimension":"Energy (kWh)",
             "storagenr":0
          },
          {
             "value":"2019-09-30T00:00:00.000000",
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
          "identnr":83251076,
          "version":0,
          "accessnr":156,
          "manufacturer":5317
       }
    }

### Code sample
**Python3**

    import requests
    import json
    
    url = "http://localhost:8000/commit"
    session = requests.session()
    
    headers = {'Content-type': 'application/json'}
    
    test_data = """
    {
       "data":[
          {
             "value":"2020-06-26T06:49:00.000000",
             "tariff":0,
             "subunit":0,
             "dimension":"Time Point (time & date)",
             "storagenr":0
          },
          {
             "value":29690,
             "tariff":0,
             "subunit":0,
             "dimension":"Energy (kWh)",
             "storagenr":0
          },
          {
             "value":"2019-09-30T00:00:00.000000",
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
          "identnr":83251076,
          "version":0,
          "accessnr":156,
          "manufacturer":5317
       }
    }
    """
    
    result = session.post(url, data=test_data, headers=headers)
    print(str(result.status_code) + ":" + result.text)

**Response**

    200: Committed to database

## export
Download a CSV file which contains the last message for each device. The specification of the CSV file is as follows.

 - File name: OMS-Data.csv
 - Delimiter: Comma (,)
 - File encode: UTF-8
 - Header: Yes. The 1st line. 
 - The each column represents the following data.
 
|Column |Data                          |
|-------|------------------------------|
|1      |Device ID
|2      |Device manufacturer
|3      |Device type
|4      |Device version
|5      |Message date time
|6      |Measurement dimension
|7      |Value new measurement
|8      |Value measurement in due date
|9      |Due date

    [GET] /export

### Parameters
This API does not take any parameter.

|Name                |Type            |In             |Description
|--------------------|----------------|---------------|-----------------------
|---                 |---             |---            |---

### Code sample
**Python3**

    import requests
    
    url = "http://localhost:8000/export"
    session = requests.session()
    
    result = session.get(url)
    print(result.text)

**Response**

    Device ID,Device manufacturer,Device type,Device version,Message date time,Measurement dimension,Value new measurement,Value measurement in due date,Due date
    80337,5317,4,0,2021.10.12 00:00:00.000000,Energy (kWh),29600,16274,2021.10.30

