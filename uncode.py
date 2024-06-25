# 目标字符串
unicode_string = "."

# 将字符串编码为 UTF-8 字节码
byte_sequence = unicode_string.encode('utf-8')

# 显示字节码
print(byte_sequence)

# 以十六进制形式显示字节码
hex_representation = byte_sequence.hex()
print(hex_representation)

# 更详细的以空格分隔的十六进制表示
hex_representation_with_spaces = ' '.join(f'{byte:02x}' for byte in byte_sequence)
print(hex_representation_with_spaces)
