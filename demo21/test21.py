import hashlib
import time
import requests
import hmac


def calculate_hashes(page, timestamp):
    # 对应 JavaScript 中的 s + o
    o = "spiderdemo_sha_salt_2025"
    t = "hash_challenge"
    c = "spiderdemo_hmac_secret_2025"
    message = f"{str(page)}_{t}_{timestamp}"

    combined_string = message + o
    # 将字符串编码为 bytes (哈希运算需要字节流)
    data_bytes = combined_string.encode('utf-8')

    # 1. 实现 l = CryptoJS.SHA256(e)
    # 使用 standard SHA-256
    sha256_hash = hashlib.sha256(data_bytes).hexdigest()

    # 2. 实现 u = sha3_256(e)
    # 使用 standard SHA-3 (256-bit)
    sha3_256_hash = hashlib.sha3_256(data_bytes).hexdigest()

    # 3. 实现 t = hmac.sha256(e, s)
    key = c.encode('utf-8')
    # 使用 hmac 模块，指定哈希算法为 sha256
    # hmac.new(密钥, 消息, 算法)
    token = hmac.new(key, message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    # 4.实现MD5加密 有盐
    salt = "spiderdemo_md5_salt_2025"
    message_bytes = (message + salt).encode('utf-8')

    md5_hash = hashlib.md5(message_bytes).hexdigest()
    return sha256_hash, sha3_256_hash, token, md5_hash


# 测试数据
def get_page_data(i):
    timestamp = str(int(time.time() * 1000))
    sign, code, token, md5_hash = calculate_hashes(i, timestamp)
    headers = {
        "authority": "www.spiderdemo.cn",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.spiderdemo.cn/authentication/hash_challenge/?challenge_type=hash_challenge",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "x-request-token": token,
        "x-verify-code": md5_hash
    }
    cookies = {
        "sessionid": "ntmqcjxw6nqed25hqe8sfak0y8ca8hyp"
    }
    url = f"https://www.spiderdemo.cn/authentication/api/hash_challenge/page/{i}/"
    params = {
        "challenge_type": "hash_challenge",
        "sign": sign,
        "code": code,
        "t": timestamp
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(response.json())
    return response.json()["page_data"]


if __name__ == '__main__':
    total = 0
    for i in range(1, 101):
        total += sum(get_page_data(i))

    print(total)
