def replace_str(input_str, k):
    result = ''
    num = set()
    for i, char in enumerate(input_str):
        if char in num:
            result += '-'
        else:
            result += char
        
        if i>=k:
            num.remove(input_str[i-k])
        num.add(char)
    return result

x = input('请输入字符和k，并以空格隔开：').split(' ')
input_str = x[0]
k = int(x[1])
output_str = replace_str(input_str, k)
print(output_str)