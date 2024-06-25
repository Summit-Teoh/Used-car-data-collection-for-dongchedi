# import fontTools
# from fontTools.ttLib import TTFont

# font = TTFont('6.17\\font.woff2')
# font.saveXML('6.17\\font.xml')


# print(chr(0xe3e8))
# print(chr(0xe3e9))
import re
# 读取xml文件
f = open('6.17\\font.xml', 'r', encoding='utf-8')
file_data = f.read()
f.close()

x = re.findall('<map code="0x(.*?)" name="(.*?)"/>', file_data)

glyph = re.findall('<GlyphID id="(.*?)" name="(.*?)"/>', file_data)

glyph_dict = {k: v for v, k in glyph}  #将键和值互换


str_list = ["0xe3f0","0xe3f1"]
# str_list = [' ', ''] + [i for i in str_data]

x_dict = {f'&#x{k}': str_list[int(glyph_dict[v])] for k, v in x}
print(x_dict)