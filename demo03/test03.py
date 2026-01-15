import challenge_pb2
import requests
from google.protobuf.json_format import ParseDict

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/x-protobuf",
    "origin": "https://www.spiderdemo.cn",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.spiderdemo.cn/authentication/protobuf_challenge/?challenge_type=protobuf_challenge",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": "h39wwk8mf13mo4405jx90ys4v2du9ucf"
}

# 1. 准备你的请求参数（字典格式）
# 注意：字典的 Key 必须与 .proto 文件中的字段名完全一致
params = {
    "page": 5,
    "challengetype": "web_spider",
    "timestamp": 1705300000,
    "signature": "a1b2c3d4e5f6g7h8"
}


def serialize_dict_to_proto(data_dict):
    # 2. 实例化一个空的请求对象
    request = challenge_pb2.ChallengeRequest()

    try:
        # 3. 将字典数据填充（解析）到 Proto 对象中
        # ignore_unknown_fields=True 可以跳过字典中多余的、未定义的键
        ParseDict(data_dict, request, ignore_unknown_fields=True)

        # 4. 序列化为二进制流
        binary_data = request.SerializeToString()

        print(f"序列化成功！长度: {len(binary_data)} bytes")
        return binary_data

    except Exception as e:
        print(f"序列化失败，请检查字段类型是否匹配: {e}")
        return None


# 执行序列化
payload = serialize_dict_to_proto(params)

# 打印查看二进制结果（爬虫请求时直接传这个 payload）
print(f"二进制负载: {payload}")

# 1. 模拟获取到的二进制数据 (实际应用中来自 requests.get(...).content)
# raw_data = response.content 

def parse_my_proto_data(raw_data):
    # 2. 实例化 Response 对象
    # 根据你提供的文件，Response 的类名是 ChallengeResponse
    response_obj = challenge_pb2.ChallengeResponse()

    try:
        # 3. 解析二进制数据
        response_obj.ParseFromString(raw_data)

        # 4. 提取数据
        print(f"当前页码: {response_obj.current_page}")
        print(f"总页数: {response_obj.total_pages}")
        print(f"时间戳: {response_obj.timestamp}")
        print(f"签名: {response_obj.signature}")

        # 5. 遍历重复列 (Repeated 字段，类似列表)
        for item in response_obj.numbers:
            print(f"ID: {item.id}, 数值: {item.value}")

        return response_obj
    except Exception as e:
        print(f"解析失败: {e}")
        return None

# 如果你想看完整的字典格式，可以转换一下
# from google.protobuf.json_format import MessageToDict
# dict_obj = MessageToDict(response_obj)

