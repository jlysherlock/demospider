# 利用httpx模块发送http请求,带请求头和cookie
import httpx

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



def get_page_data(i):
    url = f"https://www.spiderdemo.cn/sec1/api/challenge/page/{i}/"
    params = {
        "challenge_type": "header_check"
    }
    response = httpx.get(url, headers=headers, cookies=cookies, params=params)

    data = response.json()["page_data"]
    return sum(data)

if __name__ == '__main__':
    total = 0
    for i in tqdm(range(1, 101)):
        total += get_page_data(i)

    print(total)

