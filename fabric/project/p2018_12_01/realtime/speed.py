
""" http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

    /jobs/:jobid/accumulators
"""
import requests

r = requests.get('http://192.168.80.30:8081/jobs/overview')
print(r.json())