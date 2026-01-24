import requests
import json

a = requests.request("get","http://tratu.soha.vn/dict/en_vn/Construction")

print(a.json)