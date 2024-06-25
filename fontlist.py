def replace_unrecognized_chars(input_str):
    # 映射表，包含code和字符的映射
    glyph_map = {
        0xe439: '0',  #  
        0xe54c: '1',  #  
        0xe463: '2',  #  
        0xe49D: '3',  #  
        0xe41D: '4',  #  
        0xe411: '5',  #  
        0xe534: '6',  #  
        0xe3EB: '7',  #  
        0xe4E3: '8',  #  
        0xe45D: '9',  #  
        0xe40a: ' ',  #  
        0xe525: '年',
        0xe492: '万',
        0xe4a8: '公里',


    }
    
    # 构造一个新的字符串，用于保存替换后的结果
    result = []
    
    # 遍历输入字符串中的每一个字符
    for char in input_str:
        # 获取字符的Unicode码点
        code_point = ord(char)
        
        # 如果码点在映射表中，进行替换；否则，保持原字符
        if code_point in glyph_map:
            result.append(glyph_map[code_point])
        else:
            result.append(char)
    
    # 将列表转换为字符串并返回
    return ''.join(result)

# 测试函数
# sh_price = '\ue4e3.\ue54c\ue4e3\ue40a'
# print(replace_unrecognized_chars(sh_price))
