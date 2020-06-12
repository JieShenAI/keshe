import random
class Hamming():
    '''
    说明：
    不允许 这样实例化：a = Hamming([1,0,1,0,1,0,1,0,1,0])
    正确写法必须写上形参名
    编码模块：
        eg: a = Hamming(data=[1,0,1,0,1,0,1,0,1,0])  #（正确实例化写法）
        输入参数：[1,0,1,0,1,0,1,0,1,0] 二进制的(int)列表
        hammingEncode 返回编码后的列表
        hanmmingDecode 直接返回解码后不带有校验位的值
        如果没有填 Cryptodata，也是可以解密的只不过解密的是hammingEncode编码的值
    解码模块：
        eg:a = Hamming(Cryptodata=[0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0])  #（正确实例化写法）

    self.HammingData是编码和解码模块公用的，因为编码后会直接把返回值送入self.HammingData，这样解码函数就不需要传参数进去了
    同时如果用户希望只用解码的模块，那么我们需要把self.HammingData覆盖物为用户传入的Cryptodata

    '''
    def __init__(self,data=None,Cryptodata=None):
        '''
        传二进制int 列表进来
        '''
        self.data = data
        self.Cryptodata = Cryptodata
        self.HammingData = []

    def fill_HammingData(self):
        
        left = len(self.HammingData) % 8
        if left != 0:
            # 那我先把最后一个字节用0填充满，
            # 再增加一个用来说明我填充了多少bit的字节，这样解码的时候，可以根据最后填充的字节，来对删去我们填充的0
            for i in range(8-left):
                self.HammingData.append(0)
            
            add_bin = bin(8-left)[2::]

            # 填充说明要删去长度的字节
            for index in range(8-len(add_bin)):
                self.HammingData.append(0)
            l = [int(i) for i in add_bin]
            self.HammingData += l

    
        
    def hammingEncode(self):

        self.dataLen = len(self.data)
        self.r = 0  # 校验位长度

        #  2**r - 1 >= n + r
        while pow(2,self.r) - self.r < self.dataLen + 1:
            self.r += 1 
        self.HammingLen = self.r + self.dataLen #求出插入校验码后的总长
        self.HammingData = [0] * self.HammingLen
        for i in range(self.r):
            self.HammingData[pow(2,i)-1] = 1#先默认校验位都设置为1
        
        dataIndex = 0
        for i in range(self.HammingLen):#插入数据
            if self.HammingData[i] == 0:  # 跳过检验位
                self.HammingData[i] = self.data[dataIndex]
                dataIndex += 1
        # print(self.HammingData)

        for pn in range(1,self.r+1):#逐个计算校验位
            #pn所在位置
            pos = pow(2,(pn-1)) - 1
            temp = 0

            '''
            第k个校验位的校验规则是从当前位开始连续校验2^(k−1)然后跳过2^(k-1)
            '''
            for pr in range(pos,self.HammingLen+1,pow(2,pn)):              
                for i in range(pr,min(pr+pow(2,(pn-1)),self.HammingLen)):#疯狂异或
                    temp ^= self.HammingData[i]

            #  因为我temp的初值是0,然后得到了1；那么我要temp得到0，检验位肯定要从1 -> 0
            #  偶校验 1的个数为偶数个
            if temp == 1:
                self.HammingData[pos] = 0
        # print(self.HammingData)
        # 随机mistake 1 bit

        self.fill_HammingData()

        return self.HammingData

    def makeMistake(self):
        k = random.randint(0, len(self.HammingData))
        # print(k, '下标处设置错误')
        if self.HammingData[k] == 0:
            self.HammingData[k] = 1
        else:
            self.HammingData[k] = 0
        # print(self.HammingData)

    def result(self):
        '''
        消除掉检验位
        :return: 二进制(int)列表
        '''
        result = []
        count = 2
        num = 0
        for i in range(2,len(self.HammingData)):
            if i != 2**count - 1:
                result.append(self.HammingData[i])
            else:
                num += 1
                count += 1
        # print('len(self.HammingData)',len(self.HammingData))
        # print('num:','*'*20)
        # print(num)
        return result

    # 填充数字的去除
    def delete_add(self):
        add = self.Cryptodata[-8::]
        self.Cryptodata = self.Cryptodata[:-8:]
        num = 0
        for i in range(8):
            num += (2**i)*add[8-i-1]

        for i in range(num):
            del self.Cryptodata[-1]
    def hammingDecode(self):

        '''
        划重点，思路来自 https://www.bilibili.com/video/BV1SJ41157pR?from=search&seid=17199430653259420305
        我不会证明，拿来先用
        return: 解码之后，不带有校验位的列表
        '''

        # 如果有需要解密的就把解密的编码拿过来
        if self.Cryptodata != None:
            self.delete_add()
            self.HammingData = self.Cryptodata

        # 需要根据编码的长度算出  de_r   (2**de_r - 1 >= length)
        length = len(self.HammingData)
        de_r = 0
        while(1):
            if (2**de_r - 1) >= length:
                break
            de_r += 1
        # print('de_r:',de_r)
        List = []
        for pn in range(1,de_r+1):#逐个计算校验组
            #pn所在位置
            pos = pow(2,(pn-1)) - 1
            temp = 0
            for pr in range(pos,length+1,pow(2,pn)):
                for i in range(pr,min(pr+pow(2,(pn-1)),length)):#疯狂异或
                    temp ^= self.HammingData[i]
            
            # print(temp)
            List.append(temp)

        self.wrongindex = -1
        for i in range(len(List)):
            self.wrongindex += (2**i)*List[i]

        # 下标为-1代表没有错误，什么操作也不干
        if self.wrongindex != -1:
            self.HammingData[self.wrongindex] ^= 1  # 相当于取反
        if self.wrongindex != -1:
            print(self.wrongindex,'下标处的错误已纠正')
        # print('hello')
        return self.result()

if __name__ ==  '__main__':

    # str1 = [1,0,1,0,1,0,1,0,1,0]

    cry = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0]
    # print(len(str1))
    a = Hamming(Cryptodata=cry)
    # print('encode:')
    # en = a.hammingEncode()
    # print('正确的：')
    # print(en)
    # a.makeMistake()
    # print("错误的：")
    # print(a.HammingData)
    # print('decode:')
    # print('value:',a.hammingDecode())
    # print(a.HammingData)
    # print('wrongindex:',a.wrongindex)
    print(a.hammingDecode())



