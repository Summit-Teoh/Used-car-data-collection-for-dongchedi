# 目标字符串
sample_string = "."

# 显示每个字符的 Unicode 代码点
unicode_code_points = [f"U+{ord(char):04X}" for char in sample_string]

# 打印结果
for char, code_point in zip(sample_string, unicode_code_points):
    print(f"Character: {char} \t Code Point: {code_point}")
