import requests

url = 'http://localhost:8000'

#  GET
print('GET')

req = requests.get(url + '/')
print('req: ' + req.text)

#  POST /api/v1/convert
print('\nPOST /api/v1/convert')

req2 = requests.post(url + '/api/v1/convert', json = {"date":"12.20.2021 22:21:05", 'target_tz': 'Europe/Moscow',"tz": "GMT"})
print('req1: ' + req2.text)

req_2_1 = requests.post(url + '/api/v1/convert', json = {"date":"12.17.2020 11:24:21", "tz": "Asia/Seoul", 'target_tz': 'Japan'})
print('req2: ' + req_2_1.text)

# POST /api/v1/datediff

print('\nPOST /api/v1/datediff')

req3 = requests.post(url + '/api/v1/datediff', json = {"first_date":"12.20.2021 22:21:05", "first_tz": "EST", "second_date":"12:30pm 2020-12-01", "second_tz": "Europe/Moscow"})
print('request 1: ' + req3.text)

req_3_1 = requests.post(url + '/api/v1/datediff', json = {"first_date":"11.10.2021 11:20:20", "first_tz": "Japan", "second_date":"04:40pm 2021-10-05", "second_tz": "Europe/Moscow"})
print('request 1: ' + req_3_1.text)
