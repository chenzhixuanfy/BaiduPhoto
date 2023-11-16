import requests
import os
import json

class BaiduPhoto:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.URL = "https://photo.baidu.com/youai/file/v2/download?clienttype={clienttype}&bdstoken={bdstoken}&fsid={fsid}"
        self.json_path = "./json/"
        self.save_path = "./BauduPhoto/"
        self.clienttype = None
        self.bdstoken = None
        self.folder_names = []
    
    # 下载图片
    def download_photo(self):
        files= os.listdir(self.json_path) #得到文件夹下的所有文件名称
        for file in files:
            with open(self.json_path+file, 'r', encoding="utf-8") as f:
                json_data = json.load(f)
            date = json_data["extra_info"]["date_time"][:10].replace(':', '-')
            filename = json_data["path"][12:]
            fsid = json_data["fsid"]
            if(date not in self.folder_names):# 创建新文件夹
                os.makedirs(self.save_path + date)
                self.folder_names.append(date)
            
            # 获得下载链接
            response = requests.get(self.URL.format(clienttype = self.clienttype, bdstoken = self.bdstoken, fsid = fsid), headers=self.headers)
            print(f"{date}, {filename}, {response.status_code}. ")
            r_json = response.json()
            download_url = r_json['dlink']

            # 下载图片
            r_download = requests.get(download_url, headers=self.headers)
            with open(self.save_path + date + '/' + filename, 'wb') as f:
                f.write(r_download.content)
    
    def start(self):
        with open("settings.json", 'r') as f:
            json_data = json.load(f)
        self.clienttype = json_data["clienttype"]
        self.bdstoken = json_data["bdstoken"]
        self.headers["Cookie"] = json_data["Cookie"]

        self.download_photo()      
    

if __name__ == "__main__":
    baidu_photo = BaiduPhoto()
    baidu_photo.start()