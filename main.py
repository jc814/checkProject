# coding: UTF-8
import os.path
import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import webbrowser
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkimage.v2.region.image_region import ImageRegion
from huaweicloudsdkimage.v2 import *
import base64
import urllib
import json


class Application(tk.Tk):

    def __init__(self, df, image):
        super().__init__()
        self.df = df
        self.image = image
        self.title("图像话语分析标注工具")
        self.geometry("900x758")

        self.num = []
        self.number = 0
        self.previous = False
        self.count = 0
        self.current_index = 0

        # 提示信息
        self.frame_info = tk.Frame(self)
        self.frame_info.pack()
        self.progress = tk.Label(self.frame_info)
        self.progress.grid(row=0, column=0, padx=10)
        self.image_label = tk.Label(self.frame_info, cursor='hand2')
        self.image_label.grid(row=0, column=1, padx=10)

        # 创建一个图像显示框
        self.image_panel = tk.Label(self)
        self.image_panel.pack()

        # 创建失效按钮
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.ask_label = tk.Label(self.frame, text="是否跳过？")
        self.ask_label.grid(row=0, column=0, padx=10)
        self.skip_button = tk.Button(self.frame, text="失效或跳过", command=self.skip)
        self.skip_button.grid(row=0, column=1, padx=10)
        self.bind('<Down>', lambda event=None: self.skip_button.invoke())

        # 创建文本输入框
        self.frame1 = tk.Frame(self)
        self.frame1.pack()
        self.textbox1_label = tk.Label(self.frame1, text="图像叙事:", cursor='hand2')
        self.textbox1_label.grid(row=0, column=0, padx=10)
        self.text_input1 = tk.Entry(self.frame1, width=80)
        self.text_input1.grid(row=0, column=1, padx=10)
        self.search_button = tk.Button(self.frame1, text='搜索', command=self.search_on_baidu, width=10)
        self.search_button.grid(row=0, column=2, padx=10)

        self.frame2 = tk.Frame(self)
        self.frame2.pack()
        self.textbox2_label = tk.Label(self.frame2, text="图像概念:")
        self.textbox2_label.grid(row=0, column=0, padx=10)
        self.text_input2 = tk.Entry(self.frame2, width=80)
        self.text_input2.grid(row=0, column=1, padx=10)
        self.concept_button = tk.Button(self.frame2, text='获取概念', command=self.print_concept, width=10)
        self.concept_button.grid(row=0, column=2, padx=10)

        self.frame3 = tk.Frame(self)
        self.frame3.pack()
        self.textbox3_1_label = tk.Label(self.frame3, text="主题类别:")
        self.textbox3_2_label = tk.Label(self.frame3, text="0)其他")
        self.textbox3_3_label = tk.Label(self.frame3, text="1)政治")
        self.textbox3_4_label = tk.Label(self.frame3, text="2)财经")
        self.textbox3_5_label = tk.Label(self.frame3, text="3)体育")
        self.textbox3_6_label = tk.Label(self.frame3, text="4)娱乐")
        self.textbox3_7_label = tk.Label(self.frame3, text="5)社会")
        self.textbox3_8_label = tk.Label(self.frame3, text="6)科技")
        self.textbox3_9_label = tk.Label(self.frame3, text="7)美食")
        self.textbox3_10_label = tk.Label(self.frame3, text="8)健康")
        self.textbox3_11_label = tk.Label(self.frame3, text="9)教育")
        self.textbox3_12_label = tk.Label(self.frame3, text="10)环境")
        self.textbox3_13_label = tk.Label(self.frame3, text="11)时尚")
        self.textbox3_14_label = tk.Label(self.frame3, text="12)军事")
        self.textbox3_15_label = tk.Label(self.frame3, text="13)法律")
        self.textbox3_16_label = tk.Label(self.frame3, text="14)文化")
        self.textbox3_17_label = tk.Label(self.frame3, text="15)生活")
        self.textbox3_1_label.grid(row=0, column=0, padx=2)
        self.textbox3_2_label.grid(row=0, column=1, padx=2)
        self.textbox3_3_label.grid(row=0, column=2, padx=2)
        self.textbox3_4_label.grid(row=0, column=3, padx=2)
        self.textbox3_5_label.grid(row=0, column=4, padx=2)
        self.textbox3_6_label.grid(row=0, column=5, padx=2)
        self.textbox3_7_label.grid(row=0, column=6, padx=2)
        self.textbox3_8_label.grid(row=0, column=7, padx=2)
        self.textbox3_9_label.grid(row=0, column=8, padx=2)
        self.textbox3_10_label.grid(row=1, column=1, padx=2)
        self.textbox3_11_label.grid(row=1, column=2, padx=2)
        self.textbox3_12_label.grid(row=1, column=3, padx=2)
        self.textbox3_13_label.grid(row=1, column=4, padx=2)
        self.textbox3_14_label.grid(row=1, column=5, padx=2)
        self.textbox3_15_label.grid(row=1, column=6, padx=2)
        self.textbox3_16_label.grid(row=1, column=7, padx=2)
        self.textbox3_17_label.grid(row=1, column=8, padx=2)

        self.frame3_1 = tk.Frame(self)
        self.frame3_1.pack()
        self.textbox3_label = tk.Label(self.frame3_1, text="主题类别:")
        self.textbox3_label.grid(row=2, column=0)
        self.text_input3 = tk.Entry(self.frame3_1)
        self.text_input3.grid(row=2, column=1)

        self.frame4_1 = tk.Frame(self)
        self.frame4_1.pack()
        self.textbox4_label = tk.Label(self.frame4_1, text="距离:")
        self.textbox4_1_label = tk.Label(self.frame4_1, text="1)个人距离")
        self.textbox4_2_label = tk.Label(self.frame4_1, text="2)社会距离")
        self.textbox4_3_label = tk.Label(self.frame4_1, text="3)公共距离")
        self.textbox4_label.grid(row=0, column=0, padx=2)
        self.textbox4_1_label.grid(row=0, column=1, padx=2)
        self.textbox4_2_label.grid(row=0, column=2, padx=2)
        self.textbox4_3_label.grid(row=0, column=3, padx=2)
        self.frame4 = tk.Frame(self)
        self.frame4.pack()
        self.textbox4_label = tk.Label(self.frame4, text="距离:")
        self.textbox4_label.grid(row=0, column=0, padx=10)
        self.text_input4 = tk.Entry(self.frame4)
        self.text_input4.grid(row=0, column=1, padx=10)

        self.frame5_1 = tk.Frame(self)
        self.frame5_1.pack()
        self.textbox5_label = tk.Label(self.frame5_1, text="情感类别:")
        self.textbox5_0label = tk.Label(self.frame5_1, text="0)无情感")
        self.textbox5_1_label = tk.Label(self.frame5_1, text="1)愤怒anger     ")
        self.textbox5_2_label = tk.Label(self.frame5_1, text="2)恐惧fear      ")
        self.textbox5_3_label = tk.Label(self.frame5_1, text="3)悲伤sadness   ")
        self.textbox5_4_label = tk.Label(self.frame5_1, text="4)厌恶disgust   ")
        self.textbox5_5_label = tk.Label(self.frame5_1, text="5)兴奋excitement ")
        self.textbox5_6_label = tk.Label(self.frame5_1, text="6)愉悦amusement  ")
        self.textbox5_7_label = tk.Label(self.frame5_1, text="7)满足contentment")
        self.textbox5_8_label = tk.Label(self.frame5_1, text="8)敬畏awe        ")
        self.textbox5_label.grid(row=0, column=1, padx=2)
        self.textbox5_0label.grid(row=0, column=2, padx=2)
        self.textbox5_1_label.grid(row=1, column=0, padx=2)
        self.textbox5_2_label.grid(row=1, column=1, padx=2)
        self.textbox5_3_label.grid(row=1, column=2, padx=2)
        self.textbox5_4_label.grid(row=1, column=3, padx=2)
        self.textbox5_5_label.grid(row=2, column=0, padx=2)
        self.textbox5_6_label.grid(row=2, column=1, padx=2)
        self.textbox5_7_label.grid(row=2, column=2, padx=2)
        self.textbox5_8_label.grid(row=2, column=3, padx=2)
        self.frame5 = tk.Frame(self)
        self.frame5.pack()
        self.textbox5_3_label = tk.Label(self.frame5, text="情感类别:")
        self.textbox5_3_label.grid(row=0, column=0, padx=10)
        self.text_input5 = tk.Entry(self.frame5)
        self.text_input5.grid(row=0, column=1, padx=10)

        self.search()

        # 创建提交按钮
        self.frame6 = tk.Frame(self)
        self.frame6.pack()
        self.previous_button = tk.Button(self.frame6, text="上一张", command=self.move_previous)
        self.previous_button.grid(row=0, column=0, padx=10)
        self.bind('<Up>', lambda event=None: self.previous_button.invoke())
        self.submit_button = tk.Button(self.frame6, text="提交", command=self.mark)
        self.submit_button.grid(row=0, column=1, padx=10)
        self.bind('<Return>', lambda event=None: self.submit_button.invoke())

    def search(self):
        while True:
            if self.previous:
                break
            if len(keywords) != 0:
                if any(keyword in (self.df.loc[self.current_index, "图像概念"]) for keyword in keywords) or any(
                        keyword in (self.df.loc[self.current_index, "图像叙事"]) for keyword in keywords):
                    break
            elif str(self.df.loc[self.current_index, "概念"]) != "nan":
                if int(self.df.loc[self.current_index, "概念"]) == 1 or int(
                        self.df.loc[self.current_index, "概念"]) == 0:
                    self.count += 1
            elif cate != "":
                if int(self.df.loc[self.current_index, "类别"]) == cate:
                    break
            elif str(self.df.loc[self.current_index, "图像概念"]) == "nan":
                break
            elif len(keywords) == 0 and cate == "":
                break
            self.current_index += 1
            self.number += 1
        if self.number != 0:
            self.num.append(self.number)
        self.previous = False
        image_dir = os.path.join(self.image, self.df.loc[self.current_index, "图像名称"])

        # 读取图像文件
        self.image_label.configure(text=self.df.loc[self.current_index, "图像名称"])
        self.image_label.bind('<Button-1>',
                              lambda event: self.copy_to_clipboard(self.df.loc[self.current_index, "图像名称"]))
        image = Image.open(image_dir)

        # 计算缩放比例, 缩放图像
        width, height = image.size
        max_size = 380
        if width > height:
            if width > max_size:
                height = int(max_size * height / width)
                width = max_size
                width = int(max_size * width / height)
                height = max_size
            else:
                height = max_size
                width = int(max_size * width / height)
        else:
            if height > max_size:
                width = int(max_size * width / height)
                height = max_size
            else:
                height = max_size
                width = int(max_size * width / height)
        image = image.resize((width, height), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.image_panel.configure(image=photo)
        self.image_panel.image = photo
        # 读取图像叙述
        self.text_input1.insert(tk.END, self.df.loc[self.current_index, "图像叙事"])
        self.text_input2.insert(tk.END, self.df.loc[self.current_index, "图像概念"])
        self.text_input3.insert(tk.END, self.df.loc[self.current_index, "类别"])
        self.text_input4.insert(tk.END, self.df.loc[self.current_index, "距离"])
        self.text_input5.insert(tk.END, self.df.loc[self.current_index, "图像情感类别"])
        self.text_input3.select_range(0, tk.END)  # 选中文本范围
        self.text_input2.focus()  # 焦点放在entry1上
        self.textbox1_label.bind('<Button-1>',
                                 lambda event: self.copy_to_clipboard(self.df.loc[self.current_index, "图像叙事"]))
        self.progress.configure(
            text=f"已检查{self.count}张")
        return self.current_index

    def mark(self):
        print("提交")
        self.df.loc[self.current_index, "图像叙事"] = self.text_input1.get()
        self.df.loc[self.current_index, "图像概念"] = self.text_input2.get()
        self.df.loc[self.current_index, "类别"] = self.text_input3.get()
        self.df.loc[self.current_index, "距离"] = self.text_input4.get()
        self.df.loc[self.current_index, "图像情感类别"] = self.text_input5.get()
        self.df.loc[self.current_index, "概念"] = 1
        os.system('tput reset')
        self.show_info()

        # 写入数据
        self.df.to_csv(file, index=False, encoding="GB18030")
        self.next()

    def copy_to_clipboard(self, data):
        print(data)
        self.clipboard_append(data)

    def skip(self):
        self.df.loc[self.current_index, "图像叙事"] = self.text_input1.get()
        self.df.loc[self.current_index, "图像概念"] = self.text_input2.get()
        self.df.loc[self.current_index, "类别"] = self.text_input3.get()
        self.df.loc[self.current_index, "距离"] = self.text_input4.get()
        self.df.loc[self.current_index, "图像情感类别"] = self.text_input5.get()
        self.df.loc[self.current_index, "检查"] = 0
        self.show_info()

        # 写入数据
        self.df.to_csv(file, index=False, encoding="GB18030")

        self.next()

    def show_info(self):
        print(self.df.loc[self.current_index, "图像叙事"],
              self.df.loc[self.current_index, "图像概念"],
              self.df.loc[self.current_index, "类别"],
              self.df.loc[self.current_index, "距离"],
              self.df.loc[self.current_index, "图像情感类别"],
              self.df.loc[self.current_index, "检查"])

    def next(self):
        # 清空文本输入框
        self.text_input1.delete(0, tk.END)
        self.text_input2.delete(0, tk.END)
        self.text_input3.delete(0, tk.END)
        self.text_input4.delete(0, tk.END)
        self.text_input5.delete(0, tk.END)

        # 清空图像显示框
        self.image_panel.configure(image="")
        # 显示下一行数据
        self.current_index += 1
        self.count += 1
        self.number = 1
        if self.current_index >= len(self.df):
            self.current_index = 0
        self.search()

    def search_on_baidu(self):
        text1 = self.text_input1.get()
        url = 'https://www.baidu.com/s?wd=' + text1
        webbrowser.open(url)

    def is_blank_image(self, image_path):
        """
        判断图片是否为空白图片
        :param image_path: 图片路径
        :return: True or False
        """
        # 打开图片
        image = Image.open(image_path)

        # 获取图片的像素值
        pixels = image.load()

        # 统计非白色像素点的数量
        non_white_pixels = 0
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if pixels[i, j] != (255, 255, 255):
                    non_white_pixels += 1

        # 如果非白色像素点数量为0，则认为图片为空白图片
        if non_white_pixels == 0:
            return True
        else:
            return False

    def get_concept(self, path):
        if not os.path.exists(path) or self.is_blank_image(path):
            return str(0)
        else:
            ak = "HJV057FQV6XTREOWR0IE"
            sk = "aVza9ruuhAyMojUWOyBtfoxFsG8vA18jIJLMBZZM"

            credentials = BasicCredentials(ak, sk)

            client = ImageClient.new_builder().with_credentials(credentials).with_region(
                ImageRegion.value_of("cn-north-4")).build()
            imagebase64 = self.get_file_content_as_base64(path)
            # print(imagebase64)
            # 图像识别
            request = RunImageTaggingRequest()
            request.body = ImageTaggingReq(
                image=imagebase64,
                limit=5,
                threshold=10,
            )
            response = client.run_image_media_tagging(request)
            # print(str(response))
            # 名人识别
            people_request = RunCelebrityRecognitionRequest()
            people_request.body = CelebrityRecognitionReq(
                image=imagebase64
            )
            people_response = client.run_celebrity_recognition(people_request)
            # print(str(people_response))

            return self.extract_tags(str(response)) + self.extract_tags(str(people_response), 2)

    def print_concept(self):
        image_dir = os.path.join(self.image, self.df.loc[self.current_index, "图像名称"])
        try:
            items = str(self.get_concept(image_dir));
            print(items.replace('[','').replace(']','').replace(',','；').replace("'",""))
        except:
            print("获取概念失败，请稍后重试")

    def extract_tags(self, json_data, cl='1'):
        if cl == '1':
            tags = []
            data = json.loads(json_data)
            for tag in data['result']['tags']:
                # tags.append(tag['type'])
                tags.append(tag['i18n_tag']['zh'])
                for instance in tag['instances']:
                    tags.append(instance['tag'])
            return tags
        else:
            data = json.loads(json_data)
            tags = [item["label"] for item in data["result"]]
            return tags

    def get_file_content_as_base64(self, path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def move_previous(self):
        if len(self.num) > 1:
            # 清空文本输入框
            self.text_input1.delete(0, tk.END)
            self.text_input2.delete(0, tk.END)
            self.text_input3.delete(0, tk.END)
            self.text_input4.delete(0, tk.END)
            self.text_input5.delete(0, tk.END)
            # 清空图像显示框
            self.image_panel.configure(image="")
            # 显示上一行数据
            self.current_index -= self.num.pop()
            self.previous = True
            self.df.loc[self.current_index, "检查"] = "nan"
            self.number = 0
            self.count -= 1
            self.search()


if __name__ == "__main__":
    keywords = []
    cate = ""
    file = r"E:\project\result_05.csv"  # result_xx.csv结果文件的绝对路径
    image = r"E:\project\imgs"  # 存放图片的文件夹
    # file = r"path\to\result_05.csv"  # result_xx.csv结果文件的绝对路径
    # image = r"path\to\image"  # 存放图片的文件夹
    df = pd.read_csv(file, encoding="GB18030")
    app = Application(df, image)
    app.mainloop()

