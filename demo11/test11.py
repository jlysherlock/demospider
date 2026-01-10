import requests
import time
import ddddocr
from PIL import Image
import json


cookies = {
    "sessionid": "orocjnlfhgbcsocvzpgiwg75m7esc0sp"
}


def get_captcha():
    timestamp = int(time.time() * 1000)
    headers = {
        "authority": "www.spiderdemo.cn",
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://www.spiderdemo.cn/captcha/cap1_challenge/?challenge_type=cap1_challenge",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"
    }
    url = "https://www.spiderdemo.cn/captcha/api/cap1_challenge/captcha_image/"
    params = {
        "t": str(timestamp)
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    # print(response.content)
    with open("captcha.png", "wb") as f:
        f.write(response.content)


def ocr_captcha(image_path):
    # 1. 读取图片
    img = Image.open(image_path)
    # 裁剪图片
    crop_box = (53, 20, 95, 36)
    cropped_img = img.crop(crop_box)
    scale_factor = 2
    width, height = cropped_img.size
    resized_img = cropped_img.resize((width * scale_factor, height * scale_factor), resample=Image.LANCZOS)
    resized_img.save("resized.png")
    # 创建 OCR 对象
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open("resized.png", "rb") as f:
        image_bytes = f.read()
        res = ocr.classification(image_bytes)
        print(res)
    return res


def get_page_data(i, result):
    headers = {
        "authority": "www.spiderdemo.cn",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.spiderdemo.cn",
        "referer": "https://www.spiderdemo.cn/captcha/cap1_challenge/?challenge_type=cap1_challenge",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    url = "https://www.spiderdemo.cn/captcha/api/cap1_challenge/page/"
    data = {
        "captcha_input": result,
        "page_num": i,
        "challenge_type": "cap1_challenge"
    }
    res = requests.post(url, headers=headers, cookies=cookies, json=data)
    print(res.json())
    return res.json()


if __name__ == '__main__':
    total = 0
    for i in range(1, 6):
        while True:
            get_captcha()
            result = ocr_captcha("captcha.png")
            response = get_page_data(i, result)
            if response["success"] == "true":
                total += sum(response["page_data"])
                break
            else:
                print("验证码错误")
