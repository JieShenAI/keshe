import linecache
import hashlib
import sys
import Main
import myAES
import mycloud
def login():
    file = r'C:\Users\tiffa\Desktop\文件分割代码\user\user.txt'
    user_id = input('账号:').strip(' ')
    userpwd = input('密码:').strip(' ')
    if search(user_id,userpwd,file):
        print('登录成功')

    else:
        print('登录失败')
        sys.exit(0)
    return user_id
    

def search(userid,userpwd,file):
    with open(file) as file:
        for line in file.readlines():
            user_info = line.strip('\n')
            user_info = line.split(' ')
            if userid == user_info[0] and userpwd == user_info[1]:
                # print('登录成功')
                return True
    
    return False
    
def generate_key(string_text,user_id,set_id):
    m = hashlib.md5()
    m.update((string_text+user_id).encode())
    hash1 = m.digest()
    m2 = hashlib.md5()
    m2.update((user_id*2).encode())
    hash2 = m2.digest()
    print('已经根据你的配置文件自动为你生成你可能会用到的AES密钥。')
    return hash1, hash2,set_id

def generate_key2(user_id):
    m2 = hashlib.md5()
    m2.update((user_id*2).encode())
    hash2 = m2.digest()
    return hash2
def generate_key1(filepath,user_id,set_id):
    the_line = linecache.getline(filepath,set_id)
    m = hashlib.md5()
    m.update((the_line+user_id).encode())
    hash1 = m.digest()
    return hash1


def set(mode,user_id):
    filepath = r'C:\Users\tiffa\Desktop\文件分割代码\user\root.ini'
    # the_line = linecache.getline(,0)
    count = len(open(filepath, 'r').readlines())
    
    if mode == '1':
        print('你有%d个配置,你打算用哪一个(下标从0开始)?'%(count))
        while True:
            num = int(input('>'))
            if num >= 1 and num <= count:
                break
        set_id = num
        the_line = linecache.getline(filepath,num)
        # print(the_line)
    
    elif mode == '2':
        set_id = count
        the_line = input('你想添加的配置>')
        with open(r'C:\Users\tiffa\Desktop\文件分割代码\user\root.ini','a') as f:
            data = '\n'+the_line
            f.write(data)
    return generate_key(the_line, user_id,set_id)

def slice_file(key1,key2,set_id):
    infile = input('你想加密切割的文件名>')
    AEScipher = myAES.file_encrypt(infile,key1)
    # 切割
    print('密文字节长度是%d,所以推荐你输入%d,避免子文件太多.'%(len(AEScipher),len(AEScipher)/10))

    block_size = int(input('你想切割的字节大小>'))
    
    # filename = infile[-4::]
    filename = input('输入一个文件名，添加进填充部分>')
    path = input('存放切割文件的文件夹(最好是空文件夹)>')
    print('努力为您分割文件中...')
    Main.cut_file(path,AEScipher,block_size,filename,set_id,key2)
    print('文件拆分完成')
    #


def meau(user_id):
    
    filepath = r'C:\Users\tiffa\Desktop\文件分割代码\user\root.ini'
    print('*'*10,'菜单','*'*10)
    print('1:文件加密切割保存')
    print('2:恢复文件')
    print('3:上传到云盘')
    print('q:退出')
    case = input()
    if case == '1':
        print('1:选择现有的配置文件')
        print('2:添加生成新的配置文件')
        print('(警告！！！配置文件只允许添加，不允许删除前面的配置，删除后已加密的文件无法恢复)')
        choose = input()
        AESkey1,AESkey2,set_id = set(choose,user_id)
        slice_file(AESkey1,AESkey2,set_id)

        meau(user_id)
    elif case == '2':

        path = input('存放切割文件的文件夹>') 
        key2 = generate_key2(user_id)
        
        cipher_bytes,set_id = Main.file_hammingDecode_merge(path,key2)
        key1 = generate_key1(filepath,user_id,set_id)
        plaintext = myAES.myAES(key1).decrypto(cipher_bytes)
        infile = input('你想存放文件的名字>')
        with open(infile,'wb') as f:
            f.write(plaintext)

        meau(user_id)
    elif case == '3':
        upload = mycloud.cloud()
        meau(user_id)
    elif case == 'q':
        sys.exit(0)



if __name__ == '__main__':
    user_id = login()
    meau(user_id)
    
            

        
        
    
