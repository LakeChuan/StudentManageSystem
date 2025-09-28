import tkinter as tk
from tkinter import ttk

# from LoginPage import LoginPage
from views import InsertFrame, DeleteFrame, SearchFrame, UpdateFrame, AboutFrame

class MainPage:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title('学生成绩管理系统')
        self.root.geometry('1200x800+460+200')
        self.root.configure(bg='#f0f0f0')
        
        # 设置全局字体样式
        self.style = ttk.Style()
        self.style.configure('TButton', font=('微软雅黑', 12))
        self.style.configure('TLabel', font=('微软雅黑', 12))
        self.style.configure('TEntry', font=('微软雅黑', 12))
        
        # 初始化所有框架
        self.init_frames()
        self.create_page()

    def init_frames(self):
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建左侧功能按钮区域
        self.button_frame = tk.Frame(self.main_frame, bg='#f0f0f0', width=200)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # 创建右侧内容区域
        self.content_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建各个功能页面
        self.insert_frame = InsertFrame(self.content_frame)
        self.search_frame = SearchFrame(self.content_frame)
        self.delete_frame = DeleteFrame(self.content_frame)
        self.update_frame = UpdateFrame(self.content_frame)
        self.about_frame = AboutFrame(self.content_frame)

    def create_page(self):
        # 创建功能按钮
        buttons = [
            ('录入学生信息', self.show_insert),
            ('查询学生信息', self.show_search),
            ('修改学生信息', self.show_update),
            ('删除学生信息', self.show_delete),
            ('关于系统', self.show_about),
            ('退出系统', self.login_out)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.button_frame, text=text, command=command, width=20)
            btn.pack(pady=10)

        # 默认显示查询页面
        self.show_search()

    def show_insert(self):
        self.insert_frame.pack(fill=tk.BOTH, expand=True)
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.update_frame.pack_forget()
        self.about_frame.pack_forget()

    def show_search(self):
        self.search_frame.pack(fill=tk.BOTH, expand=True)
        self.insert_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.update_frame.pack_forget()
        self.about_frame.pack_forget()
        # 切换到查询页面时自动刷新数据
        self.search_frame.show_data_frame()

    def show_delete(self):
        self.delete_frame.pack(fill=tk.BOTH, expand=True)
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.update_frame.pack_forget()
        self.about_frame.pack_forget()

    def show_update(self):
        self.update_frame.pack(fill=tk.BOTH, expand=True)
        self.about_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()

    def show_about(self):
        self.about_frame.pack(fill=tk.BOTH, expand=True)
        self.update_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()

    def login_out(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    MainPage(root)
    root.mainloop()
