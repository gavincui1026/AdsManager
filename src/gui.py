import json
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.ttk import *
from tkinter import Tk, Frame, Button
import requests
from PIL import Image, ImageTk
from itertools import cycle
import os
from src.ads import AdsPower




class LoginWindow(Tk):
    """
    创建登录窗体的GUI界面已经登录的方法
    """
    def __init__(self):
        super().__init__()  # 先执行tk这个类的初始化
        self.title("Ads管理器")
        # self.geometry("620x420")
        self.resizable(0,0) # 窗体大小不允许变，两个参数分别代表x轴和y轴
        self.iconbitmap("."+os.sep+"img"+os.sep+"chip.ico")
        # self["bg"] = "royalblue"
        # 加载窗体
        self.setup_UI()

    def setup_UI(self):
        # ttk中控件使用style对象设定
        self.Style01 = Style()
        self.Style01.configure("user.TLabel",font = ("华文黑体",20,"bold"),foreground = "royalblue")
        self.Style01.configure("TEntry",font = ("华文黑体",20,"bold"))
        self.Style01.configure("TButton",font = ("华文黑体",20,"bold"),foreground = "royalblue")
        self.gif_file = "." + os.sep + "img" + os.sep + "starrynight.gif"
        self.image = Image.open(self.gif_file)

        try:
            self.frames = []
            while True:
                photo = ImageTk.PhotoImage(self.image.copy())
                self.frames.append(photo)
                self.image.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass  # We're done reading frames

        self.frames_cycle = cycle(self.frames)
        self.label_image = Label(self, image=None)
        self.label_image.pack(padx=10, pady=10)

        self.update_animation()
        # 创建一个Label标签 + Entry   --- 用户名
        self.Label_user = Label(self,text = "用户名:", style = "user.TLabel")
        self.Label_user.pack(side = LEFT,padx = 10,pady = 10)
        self.Entry_user = Entry(self,width = 12)
        self.Entry_user.pack(side = LEFT,padx = 10,pady = 10)
        # 创建一个Label标签 + Entry   --- 密码
        self.Label_password = Label(self, text = "密码:", style = "user.TLabel")
        self.Label_password.pack(side = LEFT,padx = 10,pady = 10)
        self.Entry_password = Entry(self, width=12,show = "*")
        self.Entry_password.pack(side = LEFT,padx = 10,pady = 10)
        # 创建一个按钮    --- 登录
        self.Button_login = Button(self,text = "登录",width = 4,command = self.login)
        self.Button_login.pack(side = LEFT,padx = 20,pady = 10)
    def update_animation(self):
        frame = next(self.frames_cycle)
        self.label_image.configure(image=frame)
        self.after(100, self.update_animation)
    def login(self):
        # 获取用户名和密码
        username = self.Entry_user.get()
        password = self.Entry_password.get()
        url="https://5add-65-94-5-109.ngrok-free.app/login"
        # 判断用户名和密码是否正确
        payload = {
            "username": username,
            "password": password
        }
        data=json.dumps(payload)
        res = requests.post(url, data=data)
        print(res.json())
        if res.status_code == 200:
            if res.json()["status"] =='success':
                # 登录成功
                self.destroy()
                # 创建主窗体
                self.main_window = MainWindow(token=res.json()["token"])
                self.main_window.mainloop()
            else:
                # 登录失败
                messagebox.showinfo("提示", "用户名或密码错误")
        else:
            messagebox.showinfo("提示", "服务器错误")

class MainWindow(Tk):
    def __init__(self,token):
        super().__init__()
        self.title('Ads管理器')
        self.geometry('500x400')  # 调整窗口大小以适应新的布局
        self.setup_UI()
        self.token=token

    def setup_UI(self):
        # 标题和说明区域
        header_frame = Frame(self)
        header_frame.pack(fill='x', padx=20, pady=20)

        title_label = Label(header_frame, text='Ads管理器', font=('Arial', 18, 'bold'))
        title_label.pack()
        # 按钮和表格区域
        action_frame = Frame(self)
        action_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 按钮区域
        action_frame = Frame(self)
        action_frame.pack(fill='x', pady=20)

        # 按钮容器，用于容纳实际的按钮
        button_container = Frame(action_frame)
        button_container.pack(pady=10)

        # 按钮区域
        modify_proxy_button = Button(button_container, text='修改代理', command=self.modify_proxy, font=('Arial', 12), fg='white', bg='#4CAF50', padx=20, pady=10)
        modify_proxy_button.grid(row=0, column=0, padx=5, pady=10)

        launch_browser_button = Button(button_container, text='原神!启动！', command=self.launch_browser, font=('Arial', 12), fg='white', bg='#2196F3', padx=20, pady=10)
        launch_browser_button.grid(row=0, column=1, padx=5, pady=10)

        # 让button_container在其父容器action_frame中居中
        button_container.pack(anchor='center')

        # 表格区域 - 使用Listbox模拟
        browser_list_frame = Frame(self)
        browser_list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = Scrollbar(browser_list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.browser_list = Listbox(browser_list_frame, yscrollcommand=scrollbar.set)
        self.browser_list.pack(side=LEFT, fill='both', expand=True)
        scrollbar.config(command=self.browser_list.yview)
    def modify_proxy(self):
        print("Modify Proxy Configuration")

    def launch_browser(self):
        # 创建新窗口
        manager = AdsManager(self,token=self.token)

    def add_browser(self, city):
        # 添加浏览器到列表
        browser_name = f"{city}"  # 使用城市作为浏览器名称
        self.browser_list.insert(END, browser_name)


    def modify_complete(self):
        # 修改完成的处理函数
        pass

    def insert_browsers(self, browser_ids):
        for browser_id in browser_ids:
            self.add_browser(browser_id)



class AdsManager(Toplevel):
    def __init__(self,parent,token):
        super().__init__()
        self.title('Ads Manager')
        self.geometry('600x400')
        self.setup_UI()
        self.parent=parent
        self.token=token

    def setup_UI(self):
        self.tree = Treeview(self, columns=("Region", "City"), show="headings")
        self.tree.heading("Region", text="Region")
        self.tree.heading("City", text="City")
        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # 添加浏览器按钮
        add_button = Button(self, text="+", command=self.open_add_dialog)
        add_button.pack(anchor=NE, padx=10, pady=5)
        completed_button = Button(self, text="修改完成", command=self.modify_complete)
        completed_button.pack(padx=10, pady=5)

    def open_add_dialog(self):
        # 打开添加浏览器的对话框
        AddBrowserDialog(self)

    def add_browser_to_table(self, region, city):
        # 将新浏览器添加到表格中同时也添加到MainWindow的Listbox中
        self.tree.insert("", END, values=(region, city))


    def modify_complete(self):
        # 修改完成的处理函数
        city_names = (self.tree.item(item)['values'][1] for item in self.tree.get_children())
        proxies={}
        for item in self.tree.get_children():
            city=self.tree.item(item)['values'][1]
            region=self.tree.item(item)['values'][0]
            proxies[region]=city
        self.parent.insert_browsers(city_names)
        self.destroy()
        ads_power = AdsPower(proxies,token=self.token)





class AddBrowserDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Browser")
        self.geometry("300x200")  # 调整窗口大小以适应下拉列表
        self.parent = parent

        # 省份数据，示例数据
        self.provinces = [
            "alberta",
            "british Columbia",
            "manitoba",
            "new Brunswick",
            "newfoundland and Labrador",
            "nova Scotia",
            "ontario",
            "prince Edward Island",
            "quebec",
            "saskatchewan"
        ]
        # 城市数据，示例数据，实际应用中应根据省份动态变化
        self.cities = {"alberta": ["calgary", "edmonton"], "british Columbia": ["vancouver", "victoria"], "manitoba": ["winnipeg"], "new Brunswick": ["fredericton", "saint John", "moncton"], "newfoundland and Labrador": ["st. John's"], "nova Scotia": ["halifax"], "ontario": ["toronto", "ottawa", "mississauga", "brampton", "hamilton", "london", "markham", "vaughan", "kitchener", "windsor"], "prince Edward Island": ["charlottetown"], "quebec": ["montreal", "quebec City", "laval", "gatineau", "longueuil", "sherbrooke", "saguenay", "levis", "trois-rivieres", "terrebonne"], "saskatchewan": ["saskatoon", "regina"]}

        # 省份选择区域
        Label(self, text="Province:").pack(pady=(10, 0))
        self.province_combobox = Combobox(self, values=self.provinces)
        self.province_combobox.pack()
        self.province_combobox.bind("<<ComboboxSelected>>", self.update_cities)

        # 城市选择区域
        Label(self, text="City:").pack(pady=(10, 0))
        self.city_combobox = Combobox(self)
        self.city_combobox.pack()

        # 确认按钮
        self.add_button = Button(self, text="Add", command=self.add_browser)
        self.add_button.pack(pady=10)

    def update_cities(self, event=None):
        province = self.province_combobox.get()
        cities = self.cities.get(province, [])
        self.city_combobox['values'] = cities
        if cities:
            self.city_combobox.current(0)  # 默认选择第一个城市

    def add_browser(self):
        # 这里实现添加单个浏览器实例的逻辑
        # 可以通过获取province_combobox和city_combobox的值来进行
        province = self.province_combobox.get()
        city = self.city_combobox.get()
        print(f"Adding browser instance for {province}, {city}")
        self.parent.add_browser_to_table(province, city)
        # 这里可以根据需要执行其他操作，比如更新主界面等
        self.destroy()
if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()