from  lanzou.api import LanZouCloud
import os
class cloud():
    def __init__(self):
        self.cloud_cookie_path = input('输入存放你cookie的文件>')
        self.cloud_cookie_path = r'C:\Users\tiffa\Desktop\备份\user\root_cloud.ini'
        lzy = self.login()
        if lzy != False:
            self.lzy = lzy
            self.uploadfile()
            # self.show_links(1931009)
        

    # def show_links(self,folder_id):
    #     # mylist = self.lzy.get_file_list(folder_id)
    #     # print(mylist)
    #     self.lzy.get_share_info(folder_id)


    def uploadfile(self):
        all_Folder = self.lzy.get_move_folders()
        for i in all_Folder:
            print(i)
        folder_id = int(input('选择一个你想存放文件夹的id>'))
        # self.show_links(folder_id)
        dir_path = input('输入你要上传文件夹的路径>')
        code = self.lzy.upload_dir(dir_path,folder_id)
        if code == LanZouCloud.SUCCESS:
            print('文件夹上传成功')

        else:
            print('上传错误,状态码为:',code)
        


    def get_cookie(self):
        while not os.path.exists(self.cloud_cookie_path):
            print ("cloud_cookie_path doesn't exists")
            self.cloud_cookie_path = input('输入存放你cookie的文件,或者如果你不知道输入 [q] 退出>')
            if self.cloud_cookie_path == 'q':
                return False
        with open(self.cloud_cookie_path) as f:
            data = f.readlines()
            self.ylogin,self.phpdisk_info = data[0].split(' ')

        return True

    def login(self):
        lzy = LanZouCloud()
        if self.get_cookie():
            cookie = {'ylogin':self.ylogin,'phpdisk_info':self.phpdisk_info}
            if lzy.login_by_cookie(cookie) == LanZouCloud.SUCCESS:
                print('与云服务器连接成功...')
                return lzy
            else:
                print('你可能输入了错误的cookie地址')
                return False
        else:
            print(登录失败)
            return False
        



if __name__ == '__main__':
    pass


# cookie = {'ylogin':'1414367','phpdisk_info':'BzJfaVEyVW0FNAZgCWRSAVo%2BBwxZMVU3V2ZQNwI1UGpTblViA2MAOwU3UwoMZVE%2BUTFXbVphVDZTYwJjBWVQMAc3Xz9RMFVpBTcGbwlqUj5aPAc9WTFVZ1dlUGYCPFAzU2FVbwNnAGoFZFM3DF9ROlE0V2daNFQyU2gCawU2UGAHNF9t'}
# # cookie = {'ylogin':'14fasdfasdfasdf14367','phpdisk_info':'BzJfaVEyVfsdafasffdfaffW0FNAZgCWRSAVo%2BBwxZMVU3V2ZQNwI1UGpTblViA2MAOwU3UwoMZVE%2BUTFXbVphVDZTYwJjBWVQMAc3Xz9RMFVpBTcGbwlqUj5aPAc9WTFVZ1dlUGYCPFAzU2FVbwNnAGoFZFM3DF9ROlE0V2daNFQyU2gCawU2UGAHNF9t'}

# if lzy.login_by_cookie(cookie) == LanZouCloud.SUCCESS:
#     print('hello')


