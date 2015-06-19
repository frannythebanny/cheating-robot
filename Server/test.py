import requests

payload = {"word_status": "_ _ _"}

requests.put("http://195.169.210.194:1234/1", data=payload)
