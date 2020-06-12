import myAES,hammingcode,hammingIO
import os,sys
import hashlib
import login
def hash_bytes(Bytes):
    m = hashlib.md5()
    m.update(Bytes)
    return m.digest()

def hash_check(Bytes,block_hash):
    if hash_bytes(Bytes) == block_hash:
        return True
    else:
        return False

def add_AES(block_hash,filename,block_id,set_id,key2):
    
    add = block_hash
    # filename.encode()[0:13:]

    # 如果文件名不是13 Bytes则将其填充成13Bytes
    filename = filename.encode()[0:13:]
    length = len(filename)
    left = 13 - length
    for i in range(left):
        filename += b'\0'
    if len(filename)== 13:
        # print('len is 13')
        pass
    else:
        print('add error')


    add += filename
    block_id = int(block_id).to_bytes(length=2, byteorder='big')
    add += block_id
    set_id = int(set_id).to_bytes(length=1, byteorder='big')
    add += set_id

    # print('len_add>',len(add))
    # 调用AES加密
    en = myAES.myAES(key2)
    crypter = en.encrypt(add)
    return crypter
    
def add_check(Bytes,key2):
    # 首先进行AES解密
    de = myAES.myAES(key2)
    Bytes = de.decrypto(Bytes)
    block_hash = Bytes[0:16:]
    filename = Bytes[-16:-3:].rstrip(b'\0').decode()
    file_id = int.from_bytes(Bytes[-3:-1:],byteorder='big')
    set_id = int.from_bytes(Bytes[-1::],byteorder='big')
    return block_hash,filename,file_id, set_id
        

# AES加密文件部分
def AES_encode(infile,key1):
    '''
    1.把文件AES加密成字节
    2.返回字节                              # 转换成二进制(int)的列表
    '''
    
    cipherBytes = myAES.file_encrypt(infile,key1)

    return cipherBytes


# 进入海明编码
def hamming_encode(Bytes):
    '''
    1.把字节转成二进制列表
    2.二进制列表转换成海明编码后的二进制列表
    3.返回字节
    '''
    b_list = hammingIO.bytes_binintlist(Bytes)

    a = hammingcode.Hamming(data = b_list)  # 实例化时，必须加形参名
    
    # 得到了海明编码的二进制(int)列表
    en_list = a.hammingEncode()
    # 转成字节
    mybytes = hammingIO.binintlist_bytes(en_list)
    # error = hammingIO.bytes_binintlist(mybytes)
    return mybytes

def hamming_decode(Bytes):
    '''
    输入为字节
    1.海明解码
    2.返回字节流
    '''
    b_list = hammingIO.bytes_binintlist(Bytes)
    ham = hammingcode.Hamming(Cryptodata=b_list)
    

    # print('解码后:')
    b = ham.hammingDecode()
    a = hammingIO.binintlist_bytes(b)
    # print(type(a))
    # print('first')
    return a


def cut_file(path,mybytes,block_size,file_name,set_id,key2):
    '''
    setid ,key2
    1.把字节分成固定大小的小块再添加hash
    2.进行海明编码
    注意：这个存放切割文件的文件夹最好是空的，不然可能在后面合并的时候，把多余的文件合并进来
    '''
    block_num = 0
    for i in range(0,len(mybytes), block_size):
        slice = mybytes[i:i+block_size:]

        # 在每个小文件的后面加上hash后的16byte的字节
        myhash_bytes = hash_bytes(slice)

        add_AES_bytes = add_AES(myhash_bytes,file_name,block_num,set_id,key2)  # block_hash,filename,block_id,set_id,key2

        slice += add_AES_bytes

        # 进入海明编码吧
        # 把字节转成二进制(int)列表

        slice = hamming_encode(slice)
        
        filename = os.path.join(path, ("part--%04d.zip" % block_num))
        block_num += 1
        with open(filename,'wb') as f:
            f.write(slice)

def file_hammingDecode_merge(path,key2):

    '''
    把这个路径下的文件合并到一起,不需要写入到新文件
    key2用于解密add
    '''
    
    if not os.path.exists(path):
        print ("cutfile doesn't exists, you need a srcpath")
        raise IOError
    files = os.listdir(path)
    # print(files)
    all_right = True
    Bytes = b''

    # 保存恢复文件的名字
    real_filename = ''
    file_right = False
    bytes_list = []
    sort_list = []
    for eachfile in files:
        filepath = os.path.join(path, eachfile)
        with open(filepath, 'rb') as infile:
            # 调用海明解码
            slice_bytes = hamming_decode(infile.read())

            # 对add的32位字节进行检验
            block_hash,filename,file_id, set_id = add_check(slice_bytes[-32::],key2)
            while file_right == False:
                print('恢复的文件名是<%s>,right? y or n,q 退出'%(filename))
                case = input('>')
                if case=='y' or case=='Y':
                    print('正在努力为您加载...')
                    real_filename = filename
                    file_right = True
                    break
                elif case == 'n' or case == 'N':
                    break

                elif case == 'q':
                    sys.exit(0)
                         
            if file_right == False or filename != real_filename:
                print(filename,' ',real_filename)
                # print('error')
                continue
            
            if hash_check(slice_bytes[:-32:],block_hash) != True:
                print(filepath,'完整性校验错误')
                all_right = False

            bytes_list.append(slice_bytes[:-32:])  # 删除最后32字节的add，不能直接加进去
            sort_list.append(file_id)
            
    Bytes = b''
    # 拼接字节
    for i in range(len(bytes_list)):
        # print('index:',sort_list.index(i))

        Bytes += bytes_list[sort_list.index(i)]

    if all_right:
        print('所有子文件完整性都验证完毕，全部通过！')

    # set_id
    return Bytes,set_id
    




















# if __name__ == '__main__':

    # infile = r'C:\Users\tiffa\Desktop\备份\file\1.txt'
    # key1 = ''
    # AEScipher = AES_encode(infile,key1)
    
    # # 切割
    # block_size = int(input('你想切割的字节大小：'))

    # # 对每个子文件添加hash,再进行海明编码，再写入到子文件中
    # cut_file(r'C:\Users\tiffa\Desktop\备份\file\cutpath',AEScipher,block_size)

    # # 读取每个子文件，海明解码后，再检验hash,再拼成一个字节返回
    # cipher_bytes = file_hammingDecode_verifyHash(r'C:\Users\tiffa\Desktop\备份\file\cutpath')
    # # new_bytes = merge_file(r'C:\Users\tiffa\Desktop\备份\file\cutpath')


    # plaintext = myAES.myAES('keys').decrypto(cipher_bytes)
    # # print(plaintext)

    # with open(r'C:\Users\tiffa\Desktop\备份\file\2.txt','wb') as f:
    #     f.write(plaintext)