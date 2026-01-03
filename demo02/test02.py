import hashlib
import time
import requests
from tqdm import tqdm



headers = {
    'Host': 'www.spiderdemo.cn',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Sec-Ch-Ua': '"Not_A Brand";v="99", "Chromium";v="142"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.spiderdemo.cn/sec1/header_check/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=1, i'
}

cookies = {
    "sessionid": "6ycyvjk4fby8z0t3l87veiygavbxlxmn"
}


def get_hex_md5_signature(timestamp, page):
    # 1. 将变量拼接成字符串 (对应 JS 的 `${timestamp}${page}`)
    # 确保 timestamp 和 page 都是字符串格式
    data = timestamp + str(page)

    # 盐值
    # salt = b"\xa3\xac\xa1\xa3\x66\x64\x6a\x66\x2c\x6a\x6b\x67\x66\x6b\x6c"
    salt ="£¬¡£fdjf,jkgfkl"
    data_with_salt = (data + salt).encode("latin1")

    md5_hash = hashlib.md5(data_with_salt)
    # 4. 获取 16 进制的加密结果 (对应 hex_md5)
    return md5_hash.hexdigest()



def get_page_data(i):
    timestamp = str(int(time.time() * 1000))
    sign = get_hex_md5_signature(timestamp, i)
    print(sign)
    url = f"https://www.spiderdemo.cn/ob/api/ob_challenge1/page/{i}/"
    params = {
        "challenge_type": "ob_challenge1",
        "sign": sign,
        "timestamp": timestamp
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(response.text)
    data = response.json()["page_data"]

    return sum(data)



if __name__ == '__main__':
    total = 0
    for i in tqdm(range(1, 2)):
        total += get_page_data(i)

    print(total)
