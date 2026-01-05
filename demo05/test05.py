import requests
import base64
import io
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import ddddocr
from tqdm import tqdm


headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.spiderdemo.cn/font_anti/font_anti_challenge/?challenge_type=font_anti_challenge",
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
    url = f"https://www.spiderdemo.cn/font_anti/api/font_anti_challenge/page/{i}/"
    params = {
        "challenge_type": "font_anti_challenge"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    # 1. 准备你的 Base64 字符串 (注意：去掉开头的 data:application/x-font-woff;base64, 等前缀)
    base64_str = response.json()["b64Font"]
    # 2. 解码成二进制数据
    font_data = base64.b64decode(base64_str)
    # 3. 写入文件
    with open("font.ttf", "wb") as f:
        f.write(font_data)
    # print(response.json()["page_data"])
    return response.json()["page_data"]


def font_to_mapping(font_path):
    # 1. 初始化 OCR
    ocr = ddddocr.DdddOcr(show_ad=False)
    # 2. 加载字体
    font = TTFont(font_path)
    # 这里的 font_path 需要给 PIL 使用，确保路径正确 这是关键!!!!!!!!!!!!!!
    pil_font = ImageFont.truetype(font_path, 40)
    # 3. 获取所有字符的 Unicode 编码
    cmap = font.getBestCmap()
    # print(cmap)
    mapping_result = {}
    # 4. 遍历并识别
    for code, name in cmap.items():
        # 将 code 转为字符 (例如 0x30 -> '0')
        char = chr(code)
        # 创建一个白色背景的小画布
        img = Image.new('RGB', (50, 50), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        # 将字符画在画布中央 (黑色)
        # 注意：有些反爬字体的 Unicode 可能是自定义区域，直接 chr(code) 就能画出来
        draw.text((5, 5), char, font=pil_font, fill=(0, 0, 0))
        # 将图片转为 bytes 传给 OCR
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        # OCR 识别
        res = ocr.classification(img_bytes)
        # print(res)
        # 识别结果可能存在错误，这里将一些常见错误映射为正确结果
        confuse_map = {'O': '0', 'o': '0', 'D': '0', 'I': '1', 'l': '1', 'z': '2', 'Z': '2', 'S': '5', 's': '5'}
        # 将错误映射为正确结果 如果为数字，则返回数字本身  如果为字母，则返回对应的数字
        res = confuse_map.get(res, res)
        # 记录映射关系 (Unicode -> 识别出的文字)
        mapping_result[char] = res
        # print(f"字符: {chr(code)}  识别结果: {res}")

    return mapping_result


# 执行
if __name__ == "__main__":
    total = 0
    for i in tqdm(range(1, 101)):
        page_data = get_page_data(i)
        # print(page_data)
        # 获取字体映射关系
        mapping = font_to_mapping("font.ttf")
        for data_str in page_data:
            # 将数字型字符串映射为数字  data_str 类似"4372"字符串
            result_str = "".join([mapping[char] for char in data_str])
            total += int(result_str)

    print(total)
