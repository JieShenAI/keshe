import os
from Cryptodome.Cipher import AES
from binascii import b2a_hex,a2b_hex  # b2a 16->字符串 ；a2b 字符串->16
from Cryptodome import Random
class myAES(object):
    def __init__(self,key):
        '''
        初始化方法
        key:
        '''
        # self.key = key.encode('utf-8')
        self.key = key
        # 加密格式
        self.mode = AES.MODE_ECB
        # self.iv = Random.new().read(AES.block_size) # 读取处理的数据  16进制的数据
    
    def to_16(self,text):
        # text = text.encode('utf-8')  # windows用的gbk
        length = 16
        # 用户输入的字符串长度
        count = len(text)
        if count<length:
            add = (length - count)
            text = text + ('\0'*add).encode('utf-8')
        elif count>length:
            add = (length - (count % length))
            text = text + ('\0'*add).encode('utf-8')  # '\0' 和 '0' 的区别
        self.to16_text = text
        # print(self.to16_text)
        # return b2a_hex(self.to16_text)
        # print(self.to16_text)
        return self.to16_text

    def encrypt(self,text):
        '''
        加密函数 如果text不足16位，使用空格来补足16位
        16位 密钥规则
        return 加密后的字节
        '''
        # text = text.encode('utf-8')  # windows用的gbk
        # enkey = self.to_16(self.key)
        enkey = self.key
        cryptor = AES.new(enkey,self.mode)  # ,self.iv
        # 密钥的长度 AES-128(16) 24(AES-192) 32(AES-256) bytes为长度
        length = 16
        

        count = len(text)
        if count % 16 != 0:
            if count<length:
                add = (length - count)
                text = text + ('\0'*add).encode('utf-8')
            elif count>length:
                add = (length - (count % length))
                text = text + ('\0'*add).encode('utf-8')  # '\0' 和 '0' 的区别

        self.ciphertext = cryptor.encrypt(text)
        # # print('iv',b2a_hex(self.iv))

        # # print(self.ciphertext)
        # return b2a_hex(self.ciphertext)
        # 返回的是字节
        return self.ciphertext


    def decrypto(self,text):
        '''
        解密函数
        return 
        '''
        dekey = self.to_16(self.key)
        aes = AES.new(dekey,self.mode)  # ,self.iv
        # 解密的数据
        plaintext = aes.decrypt(text).rstrip(b'\0')
        # print(type(plaintext))
        return plaintext


def file_encrypt(infile,key1):

    with open(infile,'rb') as f:
        data = f.read()
        A = myAES(key1)
        cipher = A.encrypt(data)
    return cipher

def file_decrypt(infile,outfile):
    # infile = '2'
    # outfile = '3.txt'
    with open(infile,'rb') as f:
        data = f.read()

        key = 'keys'
        A = myAES(key)
        plain_text = A.decrypto(data)

        with open(outfile,'wb') as wf:

            plain_text = plain_text.rstrip(b'\0')   ############!!!!!!!!!!!!1
            # print(bytes.decode(a))
            wf.write(plain_text)


def cutfile(encryptfile,despath,block_size):
    # srcpath = 'code.zip'
    # despath = 'file_test'
    inputfile = open(encryptfile, 'rb') #rb 读二进制文件

    try:
        chunknum  = 0
        while 1:
            
            chunk = inputfile.read(block_size)
            #此处进行加密
            # !!!!!!!!!!!!!!!!!!!!!!!	
            #over
            if not chunk: # 文件块是空的
                break
            # chunk = 
            # 加密 !!!!!!!!!!!!!!!
            chunknum = chunknum + 1
            filename = os.path.join(despath, ("part--%04d.zip" % chunknum))
            fileobj = open(filename, 'wb')
            fileobj.write(chunk) 
    except IOError:
        print ("read file error\n")
        raise IOError
    finally:
        inputfile.close()

def mergefile(cutpath,mergepath):
    #  '将src路径下的所有文件块合并，并存储到des路径下。'
    if not os.path.exists(cutpath):
        print ("cutfile doesn't exists, you need a srcpath")
        raise IOError
    files = os.listdir(cutpath)
    
    with open(mergepath, 'wb') as output:
        # output可以一直往里面填充数据的原因是，主循环未退出，文件没有close
        for eachfile in files:
            filepath = os.path.join(cutpath, eachfile)
            with open(filepath, 'rb') as infile:
                data = infile.read()
                output.write(data)

def generate_encrypt_file():
    # 需要进行加密的文件名
    source = 'code.zip'

    # 存放加密数据的文件名
    encryptfile = '2'

    # # 密文恢复验证的文件名
    # recover = 'recover.txt'

    # 先把文件加密
    file_encrypt(source,encryptfile)


if __name__ == '__main__':

    # 需要进行加密的文件名
    source = r'D:\pycarm_code\file\1.docx'

    # 存放加密数据的文件名
    encryptfile = r'D:\pycarm_code\file\encry_total.docx'

    # # 密文恢复验证的文件名
    recover = r'D:\pycarm_code\file\recover.docx'

    # 先把文件加密
    file_encrypt(source,encryptfile)

    # 文件解密
    # file_decrypt(encryptfile,recover)

    # 存放分块数据的文件名 注意此处是文件夹
    cutfile_path = r'D:\pycarm_code\file\cutpath'
    mergefile_path = r'D:\pycarm_code\file\mergefile'
    
    # # 再把加密的文件分割
    cutfile(encryptfile,cutfile_path,500)

    # 加密文件的合并解密
    mergefile(cutfile_path,mergefile_path)

    # # 文件解密
    file_decrypt(mergefile_path,recover)
    






