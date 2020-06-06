import binascii
import newhamming

def open_file(filename):
	with open(filename,'rb') as f:
		data = f.read()
		s = ''
		for i in data:
			num = (bin(i)[2:])
			s += '0'*(8-len(num))+num
		# print(s)
	return s


# def hexStringTobytes(str):
#     # str = str.replace(" ", "")
# 	return bytes.fromhex(str)


def hexStringTobytes(str):
	return bytes.fromhex(str) #######inportant 16(str)->bytes

def bytes2bin(filename):
	with open(filename,'rb') as f:
		data = f.read()
	# print('源文件的字节：')
	# print(data)
	s = ''
	for i in data:
		num = (bin(i)[2:])
		s += '0'*(8-len(num))+num
	# print(s)
	return s

def test(): 
	fh = open(r'ciyun.txt', 'rb')  
	a = fh.read() 
	#print 'raw: ',`a`,type(a)  
	hexstr = binascii.b2a_hex(a)
	print('a:',a)
	print('hexstr:',hexstr) #示意结果为4d5a900003000000....
	print(type(a),type(hexstr))
	#

def bin2hex(s):
	'''
	二进制转成16进制
	二进制字符: 00001000 -> 08
	'''
	count = 1
	hex_16 = ''
	a = ''
	for i in range(len(s)):
		a += s[i]
		if count == 4:
			# print('temp:',a)
			num = hex(int(a,2))
			hex_16 += num[2::]
			count = 0
			a = ''
		count += 1
	if a != '':
		num = hex(int(a,2))
		hex_16 += num[2::]
	return hex_16

			
def simple_bin2bytes(s):
	data = []
	for i in range(0,len(s),8):
		data.append(int(s[i:i+8],2))
	a = bytes(data)
	return a




if __name__ == '__main__':
	s = bytes2bin('171.docx') # ciyun.txt
	# print('源文件的二进制:')
	# print(s)

	#  进行海明编码
	ham = newhamming.Hamming(s)
	ham.hammingEncode()
	mybytes1 = bytes(ham.HammingData) #列表
	ham.newhammingDecode()
	data = simple_bin2bytes(ham.result())
	# data = simple_bin2bytes(s)
	# print(data)
	with open('new2.docx','wb') as f:
		f.write(data)


	# bin_str = bytes2bin()
	# # 我需要把二进制转成16进制

	# test()
	# a = hexStringTobytes('e6b288e69db0e58f91e79a84e697b6e997b461e2809866617364200d0a617364667364610d0a61647366e5958ae6b0b4e6b0b4616466617364200d0a616466617364200d0a61646661736420e788b1e79a84e889b2e694bee79a840d0a')
	# print(a)
	# bin_str = open_file('ciyun.txt')
	# print(bin_str)

	# # 因为8位一个字节,我们尝试自己合成字节
	# new_str = ''
	# index = 0
	# pre = 0
	# while index < len(bin_str):
	# 	index += 8
	# 	slice = bin_str[pre:index:]
	# 	# 转换开始吧
	# 	pre = index
	# 	new_str += slice

	# print(new_str)


















# with open('171.docx','rb') as f:
# 	data = f.read()
	# # print(data)
	# s = ''
	# count = 0
	# l = []
	# for i in  data:
	# 	count += 1
	# 	if count == 8:
	# 		count = 0
	# 		l.append(s)
	# 		s = ''
	# 	num = (bin(i)[2:])
	# 	s += '0'*(8-len(num))+num
		
	# if count != 0:
	# 	l.append(s)
# print(l)

# by = b''
# for i in range(len(l)):
# 	str1 = '0b' + l[i]
# 	num = eval(str1)
# 	mybytes = num.to_bytes(8,'big')
# 	if i == len(l)-1:
# 		mybytes = mybytes.lstrip(b'\0')
	
# 	by += mybytes
	


	
# s = '0b' + s
# print(s)
# a = eval(s)
# print(a)
# print(type(a))
# b = a.to_bytes(6,'big')
# print(b)
# print(type(b))
# print(b.lstrip(b'\0'))

# # print(a)
# with open('new.docx','wb') as fw:
# 	fw.write(data)


