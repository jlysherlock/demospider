#把ttf文件转成xml文件
from fontTools.ttLib import TTFont
font = TTFont('font.ttf')
font.saveXML('font.xml')
font.close()
print('ok')
