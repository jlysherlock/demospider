
from PIL import Image, ImageDraw, ImageFont




# 创建图像和绘图对象
image = Image.new('RGB', (400, 40), color=(255, 255, 255))
draw = ImageDraw.Draw(image)
# 加载中文字体（需替换为实际路径）
font = ImageFont.truetype('simkai.ttf', 40)
# 绘制中文文本
draw.text((0, 0), "我是一个好人", font=font, fill=(0, 0, 0))
# 保存图像
image.save('chinese_text.png')


