# Elastic5GC Monitor
This repo is part of Elastic5GC project. You can see info about this project [here!](#)
This is a resource monitor, that centralize all stats of AMF services.

## Endpoints
### POST /entry/<int:amf_id>
Register AMF CPU usage.
|Param|Location|Type|Description
|-|-|-|-|
amf_id | URL| integer| Uniq identifier of AMF service|
cpu_usage| BODY | float | CPU usage in percentage|

**Response**

String 'OK'

**Example of request**

``curl -X POST http://localhost:5000/entry/1234 -dcpu_usage=1.2345``

----

### GET /entries/<int:num_of_periods>
Retrieve a ordered (creation date DESC) set of entries grouped by cofigured time window with size of *num_of_periods*.
|Param|Location|Type|Description
|-|-|-|-|
num_of_periods | URL | integer| Quantity of periods to retriev|

**Response**
An array of grouped entries by time window.
<pre>
[
  {
    "_id": string - identifier of time window,
    "count": int - total of entries,
    "entries": [
      {
        "amf_id": int - identifier of AMF service,
        "cpu_usage": float - CPU usage in percentage,
        "created_at": string - date of usage registration
      }
    ]
  }
]
</pre>

**Example of request**

``curl http://localhost:5000/entries/2``

<pre>
[
  {
    "_id": "200905134803",
    "count": 1,
    "entries": [
      {
        "amf_id": 2021,
        "cpu_usage": "0.8854521364092276",
        "created_at": "Sat, 05 Sep 2020 13:48:30 GMT"
      }
    ]
  },
  {
    "_id": "200905134802",
    "count": 3,
    "entries": [
      {
        "amf_id": 2021,
        "cpu_usage": "0.8464800498504486",
        "created_at": "Sat, 05 Sep 2020 13:48:20 GMT"
      },
      {
        "amf_id": 2020,
        "cpu_usage": "1.85501711567351",
        "created_at": "Sat, 05 Sep 2020 13:48:29 GMT"
      },
      {
        "amf_id": 1111,
        "cpu_usage": "0.43829315644555694",
        "created_at": "Sat, 05 Sep 2020 13:48:29 GMT"
      }
    ]
  }
]
</pre>

## Pre reqs
* Docker Engine - [How to install](https://docs.docker.com/engine/install/)
* Python 3.5 or superior
* Flask 1.1.X

# Env Vars
|Variable|Type|Description|
|-|-|-|
|TIME_WINDOW| int | Time in seconds to segment data|


### Running on docker
**Create environment file**

``cd docker && cp environment.sample enviroment``
>Change configs to match to your setup.

**Running**

``sudo docker-compose up``
