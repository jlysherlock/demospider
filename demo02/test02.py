import hashlib
import time
import requests
from tqdm import tqdm

# 请求头校验比较宽松,只要ua 和 cookie 都符合要求即可
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

cookies = {
    "sessionid": "hy0iomsjkupivfg72vn5xzcti5v9fdwr"
}


def get_hex_md5_signature(timestamp, page):
    # 1. 将变量拼接成字符串 (对应 JS 的 `${timestamp}${page}`)
    # 确保 timestamp 和 page 都是字符串格式
    data = timestamp + str(page)

    # 盐值为字符串
    salt = "£¬¡£fdjf,jkgfkl"
    # 不能字节串相加，只能字符串相加后再编码成字节串
    data_with_salt = (data + salt).encode("latin1")
    md5_hash = hashlib.md5(data_with_salt)

    # 盐值为字节串
    # salt = b"\xa3\xac\xa1\xa3\x66\x64\x6a\x66\x2c\x6a\x6b\x67\x66\x6b\x6c"
    # md5_hash = hashlib.md5()
    # md5_hash.update(data.encode("latin1"))
    # md5_hash.update(salt)
    # 4. 获取 16 进制的加密结果 (对应 hex_md5)
    return md5_hash.hexdigest()


def get_page_data(i):
    timestamp = str(int(time.time() * 1000))
    sign = get_hex_md5_signature(timestamp, i)
    # print(sign)
    url = f"https://www.spiderdemo.cn/ob/api/ob_challenge1/page/{i}/"
    params = {
        "challenge_type": "ob_challenge1",
        "sign": sign,
        "timestamp": timestamp
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    # print(response.text)
    data = response.json()["page_data"]

    return sum(data)


if __name__ == '__main__':
    total = 0
    for i in tqdm(range(1, 101)):
        total += get_page_data(i)

    print(total)
