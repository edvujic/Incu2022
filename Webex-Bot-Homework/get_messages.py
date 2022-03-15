import requests

roomId = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vODk0MThkNzAtYTNkYy0xMWVjLWIwODItMTUzM2E3MDM0ZjNj'
token = 'ZDRjOWEyMzMtN2Q5OS00MTUwLTk3YzgtNjk5YjBjMjFjNjZhZWViZmQyNGItNTY3_PE93_8d150a97-48b0-4274-bc9d-59a26a936ea5'

url = "https://webexapis.com/v1/messages?roomId=" + roomId

header = {"content-type": "application/json; charset=utf-8", 
         "authorization": "Bearer " + token}

response = requests.get(url, headers = header, verify = True)

print(response.json())
