import requests



url = "https://www.spiderdemo.cn/authentication/api/protobuf_challenge/page/2/"
data = '\\u0008\\u0002\\u0012\\u0012surwrexibfkdoohqjh\\u0018ôäÙ\\u008e¼3" afd0ddbc9123803abbce5271119c4bce'.encode('unicode_escape')
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)