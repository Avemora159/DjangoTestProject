import json
from io import BytesIO
import pycurl


def send_REST_request(ip, port, payload):
    try:
        response = BytesIO()
        headers = ["Content-Type:application/json", "Api-Key: ---"]
        url = "http://%s:%s/admin/#!/campaigns/" % (ip, port)
        print (url)
        conn = pycurl.Curl()
        conn.setopt(pycurl.URL, url)
        conn.setopt(pycurl.HTTPHEADER, headers)
        conn.setopt(pycurl.POST, 1)
        conn.setopt(pycurl.POSTFIELDS, '%s'%json.dumps(payload))
        conn.setopt(pycurl.WRITEFUNCTION, response.write)
        conn.perform()
        return response.getvalue()
    except:
        return None


if __name__ == '__main__':
    payload = """{
	"columns": [],
	"filters": [],
	"grouping": [
		"campaign"
	],
	"limit": 100,
	"metrics": [
		"clicks",
		"campaign_unique_clicks",
		"conversions",
		"roi_confirmed"
	],
	"offset": 0,
	"range": {
		"from": null,
		"interval": "last_monday",
		"timezone": "Europe/Istanbul",
		"to": null
	},
	"summary": false
}"""
    print (send_REST_request("136.244.93.168", 80, payload=payload))
# end def send_REST_request
#
# import requests
# url = '------'
# api_key = '-----'
# headers = {"Content-Type": "application/json",
#            "Api-Key": api_key}
# json_request_ = """
#     {
#         "columns": [],
#         "filters": [],
#         "grouping": [
#             "campaign"
#         ],
#         "limit": 100,
#         "metrics": [
#             "clicks",
#             "campaign_unique_clicks",
#             "conversions",
#             "roi_confirmed"
#         ],
#         "offset": 0,
#         "range": {
#             "from": null,
#             "interval": "yesterday",
#             "timezone": "Europe/Istanbul",
#             "to": null
#         },
#         "summary": false
#     }
#     """
# key = {'Api-Key': '-------'}
# response = requests.post(url, json=json_request_, params=key, headers=headers, auth=('test_python', 'Fnas1312NaBNN'))
# print (response.json())
