# 利用httpx模块发送http请求
import httpx
from tqdm import tqdm

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=1, i",
    "referer": "https://www.spiderdemo.cn/sec1/header_check/",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "hy0iomsjkupivfg72vn5xzcti5v9fdwr"
}


def get_page_data(i):
    url = f"https://www.spiderdemo.cn/sec1/api/challenge/page/{i}/"
    params = {
        "challenge_type": "header_check"
    }
    # with httpx.Client(headers=headers, cookies=cookies) as client:
    #     response = client.get(url, params=params)
    response = httpx.get(url, headers=headers, cookies=cookies, params=params)
    # print(response.text)
    data = response.json()["page_data"]
    return sum(data)


if __name__ == '__main__':
    total = 0
    for i in tqdm(range(1, 101)):
        total += get_page_data(i)

    print(total)
