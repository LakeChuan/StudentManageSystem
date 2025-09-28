"""

        tk.Label(self.about_frame, text='学生信息管理系统 V0.0.1', font=('Arial', 16)).pack(pady=10)
        tk.Label(self.about_frame, text='作者：张湖川', font=('Arial', 16)).pack(pady=10)
        tk.Label(self.about_frame, text='日期：2025年3月25日', font=('Arial', 16)).pack(pady=10)

"""

import tkinter as tk
from tkinter import ttk
from db import db
from tkinter import messagebox


from sqlalchemy import column


class InsertFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.chinese = tk.StringVar()
        self.math = tk.StringVar()
        self.english = tk.StringVar()
        self.status = tk.StringVar()
        self.create_page()

    def create_page(self):
        # 创建输入框架
        input_frame = tk.Frame(self, bg='#f0f0f0')
        input_frame.pack(pady=30)

        # 标题
        title_label = tk.Label(input_frame, text="学生信息录入", font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.grid(row=0, column=0, columnspan=3, pady=30)

        # 学号输入
        tk.Label(input_frame, text='学 号：', font=('微软雅黑', 12), bg='#f0f0f0').grid(row=1, column=0, pady=15, padx=10)
        tk.Entry(input_frame, textvariable=self.student_id, width=25, font=('微软雅黑', 12)).grid(row=1, column=1, pady=15)

        # 姓名输入
        tk.Label(input_frame, text='姓 名：', font=('微软雅黑', 12), bg='#f0f0f0').grid(row=2, column=0, pady=15, padx=10)
        tk.Entry(input_frame, textvariable=self.name, width=25, font=('微软雅黑', 12)).grid(row=2, column=1, pady=15)

        # 成绩输入
        tk.Label(input_frame, text='语 文：', font=('微软雅黑', 12), bg='#f0f0f0').grid(row=3, column=0, pady=15, padx=10)
        tk.Entry(input_frame, textvariable=self.chinese, width=25, font=('微软雅黑', 12)).grid(row=3, column=1, pady=15)

        tk.Label(input_frame, text='数 学：', font=('微软雅黑', 12), bg='#f0f0f0').grid(row=4, column=0, pady=15, padx=10)
        tk.Entry(input_frame, textvariable=self.math, width=25, font=('微软雅黑', 12)).grid(row=4, column=1, pady=15)

        tk.Label(input_frame, text='英 语：', font=('微软雅黑', 12), bg='#f0f0f0').grid(row=5, column=0, pady=15, padx=10)
        tk.Entry(input_frame, textvariable=self.english, width=25, font=('微软雅黑', 12)).grid(row=5, column=1, pady=15)

        # 按钮区域
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=6, column=0, columnspan=3, pady=30)

        ttk.Button(button_frame, text='录入数据', command=self.recode_info, width=15).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text='清空数据', command=self.clear_data, width=15).pack(side=tk.LEFT, padx=20)

        # 状态显示
        tk.Label(input_frame, textvariable=self.status, font=('微软雅黑', 12), bg='#f0f0f0').grid(row=7, column=0, columnspan=3)

    def clear_data(self):
        self.student_id.set('')
        self.name.set('')
        self.chinese.set('')
        self.math.set('')
        self.english.set('')
        self.status.set('')

    def validate_score(self, score_str):
        try:
            score = float(score_str)
            if 0 <= score <= 100:
                return True
            return False
        except ValueError:
            return False

    def recode_info(self):
        # 验证必填字段
        if not self.student_id.get().strip():
            messagebox.showerror("错误", "请输入学生学号！")
            return
        if not self.name.get().strip():
            messagebox.showerror("错误", "请输入学生姓名！")
            return

        # 验证成绩
        scores = {
            '语文': self.chinese.get(),
            '数学': self.math.get(),
            '英语': self.english.get()
        }

        for subject, score in scores.items():
            if not score.strip():
                messagebox.showerror("错误", f"请输入{subject}成绩！")
                return
            if not self.validate_score(score):
                messagebox.showerror("错误", f"{subject}成绩必须在0-100分之间！")
                return

        stu = {
            'student_id': self.student_id.get().strip(),
            'name': self.name.get().strip(),
            'chinese': self.chinese.get().strip(),
            'math': self.math.get().strip(),
            'english': self.english.get().strip()
        }

        if db.insert(stu):
            self.clear_data()
            self.status.set('录入成功')


class DeleteFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.create_page()

    def create_page(self):
        # 创建搜索框架
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        # 搜索选项
        self.search_type = tk.StringVar(value="student_id")
        tk.Label(search_frame, text="搜索方式：", font=('微软雅黑', 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(search_frame, text="学号", value="student_id", 
                      variable=self.search_type, bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(search_frame, text="姓名", value="name", 
                      variable=self.search_type, bg='#f0f0f0').pack(side=tk.LEFT, padx=5)

        # 搜索输入框
        self.search_var = tk.StringVar()
        tk.Label(search_frame, text="搜索内容：", font=('微软雅黑', 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_student).pack(side=tk.LEFT, padx=5)

        # 创建结果表格
        columns = ("student_id", "name", "chinese", "math", "english", "average")
        columns_value = ("学号", "姓名", "语文", "数学", "英语", "平均分")

        # 创建带滚动条的表格
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_view = ttk.Treeview(table_frame, columns=columns, show='headings',
                                     yscrollcommand=scrollbar_y.set, selectmode='extended')
        scrollbar_y.config(command=self.tree_view.yview)

        # 设置列宽和对齐方式
        self.tree_view.column("student_id", width=100, anchor='center')
        self.tree_view.column("name", width=100, anchor='center')
        self.tree_view.column("chinese", width=80, anchor='center')
        self.tree_view.column("math", width=80, anchor='center')
        self.tree_view.column("english", width=80, anchor='center')
        self.tree_view.column("average", width=80, anchor='center')

        # 设置表头
        for col, text in zip(columns, columns_value):
            self.tree_view.heading(col, text=text)

        self.tree_view.pack(fill=tk.BOTH, expand=True)

        # 底部按钮
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        delete_btn = ttk.Button(button_frame, text='删除选中', command=self.delete_selected)
        delete_btn.pack(side=tk.RIGHT, padx=5)

    def search_student(self):
        # 清空表格
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass

        search_value = self.search_var.get().strip()
        if not search_value:
            messagebox.showerror("错误", "请输入搜索内容！")
            return

        # 根据搜索类型查询
        search_type = self.search_type.get()
        students = db.search_students(search_type, search_value)
        
        if not students:
            messagebox.showinfo("提示", "未找到匹配的学生信息！")
            return

        # 显示查询结果
        for index, stu in enumerate(students):
            try:
                average = (float(stu['chinese']) + float(stu['math']) + float(stu['english'])) / 3
            except (ValueError, TypeError):
                average = 0.0

            values = (
                stu.get('student_id', ''),
                stu.get('name', ''),
                stu.get('chinese', ''),
                stu.get('math', ''),
                stu.get('english', ''),
                f"{average:.1f}"
            )
            item = self.tree_view.insert('', index+1, values=values, tags=('selected',))
            # 设置选中行的背景色
            self.tree_view.tag_configure('selected', background='#e0e0e0')

    def delete_selected(self):
        selected_items = self.tree_view.selection()
        if not selected_items:
            messagebox.showerror("错误", "请先选择要删除的学生！")
            return

        # 获取选中项的信息
        student_info = []
        for item in selected_items:
            values = self.tree_view.item(item)['values']
            student_info.append(f"学号：{values[0]}，姓名：{values[1]}")

        # 确认删除
        confirm_msg = "确定要删除以下学生信息吗？\n\n" + "\n".join(student_info)
        if not messagebox.askyesno("确认删除", confirm_msg):
            return

        # 执行删除
        success_count = 0
        failed_count = 0
        failed_students = []

        for item in selected_items:
            values = self.tree_view.item(item)['values']
            student_id = values[0]
            
            # 执行删除操作
            if db.delete_by_username(student_id):
                self.tree_view.delete(item)
                success_count += 1
            else:
                failed_count += 1
                failed_students.append(f"学号：{student_id}，姓名：{values[1]}")

        # 显示删除结果
        if success_count > 0:
            if failed_count > 0:
                failed_msg = "以下学生信息删除失败：\n\n" + "\n".join(failed_students)
                messagebox.showwarning("警告", f"成功删除{success_count}条学生信息！\n\n{failed_msg}")
            else:
                messagebox.showinfo("成功", f"成功删除{success_count}条学生信息！")
            # 清空搜索框并刷新显示
            self.search_var.set('')
            self.search_student()
        else:
            messagebox.showerror("错误", "删除操作失败！")


class SearchFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.create_page()

    def create_page(self):
        # 创建顶部控制面板
        control_frame = tk.Frame(self, bg='#f0f0f0')
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # 排序选项
        tk.Label(control_frame, text="排序方式：", font=('微软雅黑', 12), bg='#f0f0f0').pack(side=tk.LEFT, padx=10)
        self.sort_subject = tk.StringVar(value="student_id")  # 默认按学号排序
        subjects = [
            ("学号", "student_id"),
            ("语文", "chinese"),
            ("数学", "math"),
            ("英语", "english"),
            ("平均分", "average")
        ]
        for text, value in subjects:
            tk.Radiobutton(control_frame, text=text, value=value,
                          variable=self.sort_subject, command=self.show_data_frame,
                          font=('微软雅黑', 12), bg='#f0f0f0').pack(side=tk.LEFT, padx=10)

        # 排序方向
        self.sort_order = tk.StringVar(value="asc")  # 默认升序
        tk.Radiobutton(control_frame, text="升序", value="asc",
                      variable=self.sort_order, command=self.show_data_frame,
                      font=('微软雅黑', 12), bg='#f0f0f0').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(control_frame, text="降序", value="desc",
                      variable=self.sort_order, command=self.show_data_frame,
                      font=('微软雅黑', 12), bg='#f0f0f0').pack(side=tk.LEFT, padx=10)

        # 创建表格
        columns = ("student_id", "name", "chinese", "math", "english", "average")
        columns_value = ("学号", "姓名", "语文", "数学", "英语", "平均分")

        # 创建带滚动条的表格
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_view = ttk.Treeview(table_frame, columns=columns, show='headings',
                                     yscrollcommand=scrollbar_y.set, style='Custom.Treeview')
        scrollbar_y.config(command=self.tree_view.yview)

        # 设置列宽和对齐方式
        self.tree_view.column("student_id", width=120, anchor='center')
        self.tree_view.column("name", width=120, anchor='center')
        self.tree_view.column("chinese", width=100, anchor='center')
        self.tree_view.column("math", width=100, anchor='center')
        self.tree_view.column("english", width=100, anchor='center')
        self.tree_view.column("average", width=100, anchor='center')

        # 设置表头
        for col, text in zip(columns, columns_value):
            self.tree_view.heading(col, text=text)

        self.tree_view.pack(fill=tk.BOTH, expand=True)

        # 配置Treeview样式
        style = ttk.Style()
        style.configure('Custom.Treeview', font=('微软雅黑', 12))
        style.configure('Custom.Treeview.Heading', font=('微软雅黑', 12, 'bold'))

        # 显示数据
        self.show_data_frame()

    def show_data_frame(self):
        try:
            # 删除原有数据
            for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
                pass

            # 获取所有学生数据
            students = list(db.all())
            
            if not students:
                return

            # 计算平均分并添加排序键
            for student in students:
                try:
                    student['average'] = (float(student['chinese']) + float(student['math']) + float(student['english'])) / 3
                except (ValueError, TypeError):
                    student['average'] = 0.0

            # 根据选择的科目和排序方向进行排序
            sort_key = self.sort_subject.get()
            reverse = self.sort_order.get() == "desc"
            
            # 特殊处理学号排序
            if sort_key == "student_id":
                # 将学号转换为整数进行排序（如果可能的话）
                def get_sort_key(x):
                    try:
                        return int(x.get(sort_key, '0'))
                    except ValueError:
                        return str(x.get(sort_key, ''))
                students.sort(key=get_sort_key, reverse=reverse)
            else:
                students.sort(key=lambda x: float(x.get(sort_key, 0)), reverse=reverse)

            # 插入数据到表格
            for index, stu in enumerate(students):
                values = (
                    stu.get('student_id', ''),
                    stu.get('name', ''),
                    stu.get('chinese', ''),
                    stu.get('math', ''),
                    stu.get('english', ''),
                    f"{stu.get('average', 0):.1f}"
                )
                self.tree_view.insert('', index+1, values=values)

        except Exception as e:
            messagebox.showerror("错误", f"显示数据时出错：{str(e)}")


class UpdateFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.chinese = tk.StringVar()
        self.math = tk.StringVar()
        self.english = tk.StringVar()
        self.status = tk.StringVar()
        self.create_page()

    def create_page(self):
        # 创建输入框架
        input_frame = tk.Frame(self, bg='#f0f0f0')
        input_frame.pack(pady=20)

        # 标题
        title_label = tk.Label(input_frame, text="学生信息修改", font=('微软雅黑', 14, 'bold'), bg='#f0f0f0')
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # 学号输入（用于查询）
        tk.Label(input_frame, text='学 号：', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=1, column=0, pady=10, padx=5)
        tk.Entry(input_frame, textvariable=self.student_id, width=20).grid(row=1, column=1, pady=10)
        ttk.Button(input_frame, text='查询', command=self.search_user).grid(row=1, column=2, padx=5)

        # 姓名输入
        tk.Label(input_frame, text='姓 名：', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=2, column=0, pady=10, padx=5)
        tk.Entry(input_frame, textvariable=self.name, width=20).grid(row=2, column=1, pady=10)

        # 成绩输入
        tk.Label(input_frame, text='语 文：', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=3, column=0, pady=10, padx=5)
        tk.Entry(input_frame, textvariable=self.chinese, width=20).grid(row=3, column=1, pady=10)

        tk.Label(input_frame, text='数 学：', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=4, column=0, pady=10, padx=5)
        tk.Entry(input_frame, textvariable=self.math, width=20).grid(row=4, column=1, pady=10)

        tk.Label(input_frame, text='英 语：', font=('微软雅黑', 10), bg='#f0f0f0').grid(row=5, column=0, pady=10, padx=5)
        tk.Entry(input_frame, textvariable=self.english, width=20).grid(row=5, column=1, pady=10)

        # 按钮区域
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text='保存修改', command=self.update_user).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text='清空数据', command=self.clear_data).pack(side=tk.LEFT, padx=10)

        # 状态显示
        tk.Label(input_frame, textvariable=self.status, font=('微软雅黑', 10), bg='#f0f0f0').grid(row=7, column=0, columnspan=3)

    def clear_data(self):
        self.student_id.set('')
        self.name.set('')
        self.chinese.set('')
        self.math.set('')
        self.english.set('')
        self.status.set('')

    def search_user(self):
        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("错误", "请输入要查询的学生学号！")
            return

        flag, info = db.search_by_username(student_id)
        if flag:
            self.name.set(info['name'])
            self.chinese.set(info['chinese'])
            self.math.set(info['math'])
            self.english.set(info['english'])
            self.status.set('查询成功')
        else:
            self.clear_data()

    def update_user(self):
        if not self.student_id.get():
            messagebox.showerror("错误", "请先查询要修改的学生信息！")
            return

        stu = {
            'student_id': self.student_id.get(),
            'name': self.name.get(),
            'chinese': self.chinese.get(),
            'math': self.math.get(),
            'english': self.english.get()
        }

        if db.update(stu):
            self.clear_data()
            self.status.set('修改成功')

class AboutFrame(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        tk.Label(self, text='学生信息管理系统 V0.0.1', font=('微软雅黑', 18, 'bold')).pack(pady=20)
        tk.Label(self, text='作者：张湖川', font=('微软雅黑', 14)).pack(pady=10)
        tk.Label(self, text='日期：2025年3月25日', font=('微软雅黑', 14)).pack(pady=10)

