import json

import requests
class Proxy:
    def yuliproxy(self, nums, region, city, token):
        payloads = {
            "nums": nums,
            "region": region,
            "city": city,
        }
        payloads = json.dumps(payloads)
        url = "https://5add-65-94-5-109.ngrok-free.app/get_proxy"
        res = requests.post(url, data=payloads, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"  # 确保添加这个头部
        })
        return res.json()

if __name__ == '__main__':
    proxy = Proxy()
    print(proxy.yuliproxy(1, "quebec", "montreal","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnYXZpbmN1aSIsImV4cCI6MTcwOTg1NDEzMX0.Z8HrQIBQO4DkSnQhvODTSz5nbtyI0rh0XGYgIhHR79M"))