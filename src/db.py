import json
from pymongo import MongoClient
from tkinter import messagebox

class MysqlDatabase():
    def __init__(self):

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['educational_system']
        self.users = self.db['users']
        self.students=self.db['students']


        # self.users = json.loads(open('user.json',mode='r',encoding='utf-8').read())
        # self.students = json.loads(open('students.json', mode='r', encoding='utf-8').read())

    # def __str__(self):
    #     return "Name: {}, Age: {}, Grade: {}".format(self.name, self.age, self.grade)

    def check_login(self, username, password):
        if not username or not password:
            # messagebox.showerror("错误", "用户名和密码不能为空")
            return False,'用户名和密码不能为空'

        user = self.users.find_one({"username": username, "password": password})
        if user:
            return True,'登录成功'
        else:
            # messagebox.showerror("错误", "用户名或密码错误")
            return False, "用户名或密码错误"


    def check_register(self, username, password):
        if not username or not password:
            # messagebox.showerror("错误", "用户名和密码不能为空")
            return False,'用户名和密码不能为空'

        if self.users.find_one({"username": username}):
            messagebox.showerror("错误", "用户名已存在")
            return False,'用户名已存在'

        self.users.insert_one({"username": username, "password": password})
        # messagebox.showinfo("成功", "注册成功，请登录")
        return True,'注册成功，请登录'

        # for user in self.users:
        #     print(user)
        #     if user['username'] == username:
        #         if user['password'] == password:
        #            return True,'Login successful'
        #         else:
        #             return False,"Invalid password"

        return False,"Login unsuccessful, 用户不存在"
        # if username == 'admin' and password == 'password':
        #     print("Login successful")
        # else:
        #     print("Invalid username or password")

    def all(self):
        try:
            students = list(self.students.find())
            print("\n=== 数据库中的所有学生信息 ===")
            for student in students:
                print(f"学生数据：{student}")
                if 'student_id' not in student:
                    student['student_id'] = str(student['_id'])
            return students
        except Exception as e:
            print(f"获取所有学生信息时出错：{str(e)}")
            return []

    def search_students(self, search_type, search_value):
        """根据学号或姓名搜索学生"""
        try:
            print(f"\n=== 搜索学生信息 ===")
            print(f"搜索条件：类型={search_type}, 值={search_value}")
            
            if search_type == "student_id":
                # 尝试不同的查询方式
                student = self.students.find_one({"student_id": search_value})
                if not student:
                    # 尝试将搜索值转换为字符串
                    student = self.students.find_one({"student_id": str(search_value)})
                if not student:
                    # 尝试将搜索值转换为整数
                    try:
                        student = self.students.find_one({"student_id": int(search_value)})
                    except ValueError:
                        pass
                
                print(f"查询结果：{student}")
                
                if student:
                    return [{
                        'student_id': str(student.get('student_id', '')),
                        'name': student.get('name', ''),
                        'chinese': student.get('chinese', ''),
                        'math': student.get('math', ''),
                        'english': student.get('english', '')
                    }]
                return []
            else:
                students = list(self.students.find({"name": {"$regex": search_value, "$options": "i"}}))
                print(f"查询结果：{students}")
                return [{
                    'student_id': str(student.get('student_id', '')),
                    'name': student.get('name', ''),
                    'chinese': student.get('chinese', ''),
                    'math': student.get('math', ''),
                    'english': student.get('english', '')
                } for student in students]
        except Exception as e:
            print(f"查询学生信息时出错：{str(e)}")
            messagebox.showerror("错误", f"查询学生信息时出错：{str(e)}")
            return []

    def check_student_id_exists(self, student_id):
        """检查学号是否已存在"""
        return bool(self.students.find_one({"student_id": student_id}))

    def insert(self,student):
        if not student['student_id']:
            messagebox.showerror("错误", "请输入学生学号！")
            return False
        if not student['name']:
            messagebox.showerror("错误", "请输入学生姓名！")
            return False
        if not student['chinese']:
            messagebox.showerror("错误", "请输入学生语文成绩！")
            return False
        if not student['math']:
            messagebox.showerror("错误", "请输入学生数学成绩！")
            return False
        if not student['english']:
            messagebox.showerror("错误", "请输入学生英语成绩！")
            return False

        try:
            # 尝试将成绩转换为浮点数进行验证
            float(student['chinese'])
            float(student['math'])
            float(student['english'])
        except ValueError:
            messagebox.showerror("错误", "成绩必须是数字！")
            return False

        # 检查学号是否已存在
        if self.check_student_id_exists(student['student_id']):
            messagebox.showerror("错误", "该学号已存在！")
            return False

        self.students.insert_one(student)
        messagebox.showinfo("成功", "学生信息添加成功！")
        return True


    def update(self,stu):
        if not stu['student_id']:
            messagebox.showerror("错误", "请输入要修改的学生学号！")
            return False
            
        # 检查是否存在该学号的学生
        existing_student = self.students.find_one({"student_id": stu['student_id']})
        if not existing_student:
            messagebox.showerror("错误", "未找到该学号的学生！")
            return False

        try:
            # 验证成绩数据
            float(stu['chinese'])
            float(stu['math'])
            float(stu['english'])
        except ValueError:
            messagebox.showerror("错误", "成绩必须是数字！")
            return False

        result = self.students.update_one(
            {"student_id": stu['student_id']}, 
            {"$set": stu}
        )
        
        if result.modified_count > 0:
            messagebox.showinfo("成功", "学生信息修改成功！")
            return True
        else:
            messagebox.showerror("错误", "信息未改变！")
            return False


    def debug_print_student(self, student_id):
        """调试函数：打印指定学号的学生信息"""
        try:
            student = self.students.find_one({"student_id": student_id})
            if student:
                print(f"找到学生信息：{student}")
                return True
            else:
                print(f"未找到学号为{student_id}的学生")
                return False
        except Exception as e:
            print(f"查询出错：{str(e)}")
            return False

    def delete_by_username(self,student_id):
        if not student_id:
            messagebox.showerror("错误", "学号不能为空！")
            return False
            
        try:
            print(f"\n=== 尝试删除学生信息 ===")
            print(f"要删除的学号：{student_id}")
            print(f"学号类型：{type(student_id)}")
            
            # 将学号转换为字符串
            student_id = str(student_id)
            
            # 查询学生信息
            student = self.students.find_one({"student_id": student_id})
            print(f"查询到的学生信息：{student}")
            
            if not student:
                return False
                
            # 执行删除操作
            result = self.students.delete_one({"student_id": student_id})
            print(f"删除操作结果：{result.raw_result}")
            
            return result.deleted_count > 0
                
        except Exception as e:
            print(f"删除操作出错：{str(e)}")
            return False

    def search_by_username(self,student_id):
        if not student_id:
            messagebox.showerror("错误", "请输入要查询的学生学号！")
            return False, None
            
        student = self.students.find_one({"student_id": student_id})
        if student:
            return True, student
        else:
            messagebox.showerror("错误", f'未找到学号为{student_id}的学生信息！')
            return False, None

    # for student in self.students:
    #     # print(student)
    #     if student['name'] == name:
    #         return True,student
    # return False,f'{name}学生不存在'

db = MysqlDatabase()

if __name__ == '__main__':
    print(db.check_login('admin', '123456'))
    # print(db.all())
