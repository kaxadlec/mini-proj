import requests

web_server_url = "http://192.168.15.245:80"

response = requests.get(web_server_url)
data = response.text
# print(data)
lines = data.split("\n")   # lines의 2번방에서 ':' 다음에 나온 아이피만 잘라서 쓰고싶음
print(lines)

ip_address =''
if len(lines) >= 4:
    ip_address = lines[2].split(": ")[1]

print(f"아이피 주소: {ip_address}")
print(lines[3])
