import requests
import json
import os

# 获取文件信息
class FindPhotoList:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.path = "./json/"
        self.clienttype = None
        self.bdstoken = None
        self.need_thumbnail = None
        self.need_filter_hidden = None

        self.flag = True
    
    def save_json(self, photo_list):
        for photo in photo_list:
            file_name = self.path + photo["path"][12:] + ".json"
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(photo, f, ensure_ascii=False, indent=4)

    def crawler(self, URL):
        response = requests.get(URL, headers=self.headers)
        print(response.status_code)
        data = response.json()

        photo_list = data["list"]
        if(not photo_list):# 爬取完毕
            self.flag = False
            return
        self.save_json(photo_list)

        cursor = data["cursor"]
        
        return cursor

    def func(self):
        URL = f"https://photo.baidu.com/youai/file/v1/list?clienttype={self.clienttype}&bdstoken={self.bdstoken}&need_thumbnail={self.need_thumbnail}&need_filter_hidden={self.need_filter_hidden}"
        cursor = self.crawler(URL)
        while(self.flag):
            URL = f"https://photo.baidu.com/youai/file/v1/list?clienttype={self.clienttype}&bdstoken={self.bdstoken}&cursor={cursor}&need_thumbnail={self.need_thumbnail}&need_filter_hidden={self.need_filter_hidden}"
            cursor = self.crawler(URL)
    
    def start(self):
        with open("settings.json", 'r') as f:
            json_data = json.load(f)
        self.clienttype = json_data["clienttype"]
        self.bdstoken = json_data["bdstoken"]
        self.need_thumbnail = json_data["need_thumbnail"]
        self.need_filter_hidden = json_data["need_filter_hidden"]
        self.headers["Cookie"] = json_data["Cookie"]

        os.makedirs(self.path)

        self.func()
if __name__ == "__main__":
    find_photo_list = FindPhotoList()
    find_photo_list.start()