import binascii
import hammingcode

'''
1.把文件转成二进制(int)的列表
2.把二进制(int)列表作为参数传给海明编码模块
3.拿到海明编码返回的二进制(int)列表后，将其转成字节写到新文件中
'''
class hamIO():
    def __init__(self,infile=None, outfile=None):
        self.infile = infile
        self.outfile = outfile
        # self.in_list

    def file_binintlist(self):
        with open(self.infile,'rb') as f:
            data = f.read()
        # print(data)
        b_list = []
        for Byte in data:
            num = bin(Byte)[2:]
            # 列表中加前置0
            for j in range((8-len(num))):
                b_list.append(0)
            # 再添加非0的二进制
            b_list += [int(n) for n in num]
        return b_list

    def write2file(self,b):
        # 把int的二进制列表转成字节
        Bytes = bytes(b)
        with open(self.outfile,'wb') as f:
            f.write(Bytes)

    def binintlist_bytes(self,l):
        '''
        把一个二进制列表每8位合并成一个int
        eg:[1,0,0,1,0,0,0,1] -> [145]
        '''
        # print('l is',l)
        data = []
        for i in range(0,len(l),8):
            slice = l[i:i+8:]
            num = 0
            for j in range(len(slice)):
                num += (2**j)*slice[len(slice) - j -1]
            # print('slice:',slice)
            data.append(num)
        
        a = bytes(data)
        return a

def bytes_binintlist(Bytes):

        b_list = []
        for Byte in Bytes:
            num = bin(Byte)[2:]
            # 列表中加前置0
            for j in range((8-len(num))):
                b_list.append(0)
            # 再添加非0的二进制
            b_list += [int(n) for n in num]
        return b_list

def binintlist_bytes(l):
    '''
    把一个二进制列表每8位合并成一个int
    eg:[1,0,0,1,0,0,0,1] -> [145]
    '''
    # print('l is',l)
    data = []
    for i in range(0,len(l),8):
        slice = l[i:i+8:]
        num = 0
        for j in range(len(slice)):
            num += (2**j)*slice[len(slice) - j -1]
        # print('slice:',slice)
        data.append(num)
        
    a = bytes(data)
    return a
        
if __name__ == '__main__':
    a = hamIO('../file/1.docx','../file/2.txt')
    L = a.file_binintlist()
    # 调入海明编码模块
    ham  = hammingcode.Hamming(data = L)
    ham.hammingEncode()

    data1 = a.binintlist_bytes(ham.HammingData)

    ham.makeMistake()
    a.write2file(data1)
    # with open(r'../file/saveham','rb') as f:
    #     f.read()
    b=hamIO(a.outfile,r'../file/right.docx')

    L2 = b.file_binintlist()
    ham2 = hammingcode.Hamming(Cryptodata = L2)
    value = ham2.hammingDecode()

    # print('hamdata:',ham.HammingData)
    data2 = a.binintlist_bytes(value)
    # print(data)
    b.write2file(data2)

















    # def bytes2bin(self):
    #     with open(self.infile,'rb') as f:
    #         data = f.read()
    #     # print('源文件的字节：')
    #     # print(data)
    #     s = ''
    #     for i in data:
    #         num = (bin(i)[2:])
    #         s += '0'*(8-len(num))+num
    #     # print(s)
    #     return s