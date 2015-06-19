import requests

payload = {
    'word_status': " H E L L _"
    }

requests.put("195.169.210.194:1234/1", data=payload)
