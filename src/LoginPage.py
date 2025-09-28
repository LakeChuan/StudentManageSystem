import tkinter as tk
from tkinter import messagebox, ttk
from db import db
from MainPage import MainPage


class LoginPage():
    def __init__(self, master=None):
        self.root = master
        self.root.geometry("400x300+710+420")
        self.root.title("学生成绩管理系统")
        self.root.configure(bg='#f0f0f0')

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # 创建主框架
        self.page = tk.Frame(self.root, bg='#f0f0f0')
        self.page.pack(pady=20)

        # 标题
        title_label = tk.Label(self.page, text="学生成绩管理系统", font=('微软雅黑', 16, 'bold'), bg='#f0f0f0')
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # 用户名输入框
        tk.Label(self.page, text='账户:', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=1, column=0, pady=10, padx=5)
        username_entry = ttk.Entry(self.page, textvariable=self.username, width=25)
        username_entry.grid(row=1, column=1, columnspan=2, pady=10)

        # 密码输入框
        tk.Label(self.page, text='密码:', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=2, column=0, pady=10, padx=5)
        password_entry = ttk.Entry(self.page, textvariable=self.password, show='*', width=25)
        password_entry.grid(row=2, column=1, columnspan=2, pady=10)

        # 按钮框架
        button_frame = tk.Frame(self.page, bg='#f0f0f0')
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        # 登录按钮
        login_btn = ttk.Button(button_frame, text='登录', command=self.login, width=10)
        login_btn.grid(row=0, column=0, padx=5)

        # 注册按钮
        register_btn = ttk.Button(button_frame, text='注册', command=self.register, width=10)
        register_btn.grid(row=0, column=1, padx=5)

        # 退出按钮
        quit_btn = ttk.Button(button_frame, text='退出', command=self.root.quit, width=10)
        quit_btn.grid(row=0, column=2, padx=5)


    def login(self):
        name=self.username.get()
        pwd=self.password.get()
        flag,message=db.check_login(name,pwd)
        if flag:
            self.page.destroy()
            MainPage(self.root)

        else:
            messagebox.showerror(title='错误',message=message)

    def register(self):
        name = self.username.get()
        pwd = self.password.get()
        flag, message = db.check_register(name, pwd)
        if flag:
            # self.page.destroy()
            # MainPage(self.root)
            messagebox.showerror(title='成功',message=message)
            self.username.set('')
            self.password.set('')

        else:
            messagebox.showerror(title='错误', message=message)

if __name__ == '__main__':
    root = tk.Tk()
    LoginPage(master=root)
    root.mainloop()

