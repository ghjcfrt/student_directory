import sqlite3
from tkinter import (
    END,
    LEFT,
    Button,
    Entry,
    Frame,
    Label,
    Scrollbar,
    Tk,
    messagebox,
    ttk,
)


# 数据库设置
def setup_database():
    conn = sqlite3.connect("student_directory.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            password TEXT,
            address TEXT,
            phone TEXT
        )
        """
    )
    conn.commit()
    return conn, c


# 数据库操作
conn, c = setup_database()


# 查询学生 数据库操作
def execute_query(query, params=()):
    try:
        c.execute(query, params)
        conn.commit()
    except sqlite3.IntegrityError as e:
        messagebox.showerror("错误", f"数据库错误: {e}")
        return False
    return True


# 添加学生 数据库操作
def add_student(student_id, name, password, address, phone):
    if execute_query(
        "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
        (student_id, name, password, address, phone),
    ):
        messagebox.showinfo("成功", "学生添加成功")
        app.display_students()


# 删除学生 数据库操作
def delete_student(student_id):
    if execute_query("DELETE FROM students WHERE student_id=?", (student_id,)):
        messagebox.showinfo("成功", "学生删除成功")
        app.display_students()


# 更新学生 数据库操作
def update_student(student_id, name, password, address, phone):
    if execute_query(
        "UPDATE students SET name=?, password=?, address=?, phone=? WHERE student_id=?",
        (name, password, address, phone, student_id),
    ):
        messagebox.showinfo("成功", "学生更新成功")
        app.display_students()


# GUI
class StudentManagementApp:
    # 初始化
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.conn, self.c = setup_database()
        self.display_students()

    # 设置UI
    def setup_ui(self):
        self.root.title("学生名录管理系统")
        self.setup_frames()
        self.setup_widgets()

    # 设置框架
    def setup_frames(self):
        self.left_frame = Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

    # 设置控件
    def setup_widgets(self):
        # 创建一个水平布局框架
        horizontalLayout = Frame(self.root)
        horizontalLayout.grid(row=0, column=0, sticky="ew")

        # 左侧框架
        self.setup_left_frame()
        self.left_frame.grid(row=0, column=0, padx=5, pady=5)

        # 分割线
        separator = Frame(root, width=2, bd=1, relief="sunken")
        separator.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        # 右侧框架
        self.setup_right_frame()
        self.right_frame.grid(row=0, column=2, padx=5, pady=5)

    # 设置左侧框架
    def setup_left_frame(self):
        Label(self.left_frame, text="学生ID").grid(row=0, column=0, padx=10, pady=5)
        Label(self.left_frame, text="姓名").grid(row=1, column=0, padx=10, pady=5)
        Label(self.left_frame, text="密码").grid(row=2, column=0, padx=10, pady=5)
        Label(self.left_frame, text="地址").grid(row=3, column=0, padx=10, pady=5)
        Label(self.left_frame, text="电话").grid(row=4, column=0, padx=10, pady=5)

        self.student_id_entry = Entry(self.left_frame)
        self.name_entry = Entry(self.left_frame)
        self.password_entry = Entry(self.left_frame)
        self.address_entry = Entry(self.left_frame)
        self.phone_entry = Entry(self.left_frame)

        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)
        self.phone_entry.grid(row=4, column=1, padx=10, pady=5)

        Button(self.left_frame, text="添加学生", command=self.add_student_gui).grid(
            row=0, column=2, padx=10, pady=5
        )
        Button(self.left_frame, text="删除学生", command=self.delete_student_gui).grid(
            row=2, column=2, padx=10, pady=5
        )
        Button(self.left_frame, text="更新学生", command=self.update_student_gui).grid(
            row=4, column=2, padx=10, pady=5
        )
        Button(self.left_frame, text="清空", command=self.clear_entries).grid(
            row=6, column=1, padx=10, pady=5
        )

    # 设置右侧框架
    def setup_right_frame(self):
        search_frame = Frame(self.right_frame)
        search_frame.grid(row=0, column=0, padx=10, pady=5)

        Label(search_frame, text="搜索:").pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame, width=40)
        self.search_entry.pack(side=LEFT, padx=5)
        Button(search_frame, text="搜索", command=self.search_students).pack(
            side=LEFT, padx=5
        )

        columns = ("学生ID", "姓名", "密码", "地址", "电话")
        self.student_tree = ttk.Treeview(
            self.right_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100 if col != "address" else 150)

        self.student_tree.grid(row=1, column=0, padx=10, pady=5)

        scrollbar = Scrollbar(self.right_frame, command=self.student_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.student_tree.config(yscrollcommand=scrollbar.set)
        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

    # 添加学生
    def add_student_gui(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        if not student_id or not name:
            messagebox.showerror("输入错误", "学生ID和姓名不能为空")
            return
        add_student(
            student_id,
            name,
            self.password_entry.get(),
            self.address_entry.get(),
            self.phone_entry.get(),
        )
        self.display_students()

    # 删除学生
    def delete_student_gui(self):
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showerror("输入错误", "学生ID不能为空")
            return
        delete_student(student_id)
        self.display_students()

    # 更新学生
    def update_student_gui(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        if not student_id or not name:
            messagebox.showerror("输入错误", "学生ID和姓名不能为空")
            return
        update_student(
            student_id,
            name,
            self.password_entry.get(),
            self.address_entry.get(),
            self.phone_entry.get(),
        )
        self.display_students()

    # 清空输入框
    def clear_entries(self):
        for entry in (
            self.student_id_entry,
            self.name_entry,
            self.password_entry,
            self.address_entry,
            self.phone_entry,
        ):
            entry.delete(0, END)

    # 搜索学生
    def search_students(self):
        search_term = self.search_entry.get()
        c.execute(
            "SELECT * FROM students WHERE student_id LIKE ? OR name LIKE ?",
            (f"%{search_term}%", f"%{search_term}%"),
        )
        self.update_tree(c.fetchall())

    # 显示学生
    def display_students(self):
        c.execute("SELECT * FROM students")
        self.update_tree(c.fetchall())

    # 更新树
    def update_tree(self, students):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for student in students:
            self.student_tree.insert("", END, values=student)

    # 选择学生
    def on_student_select(self, event):
        selected = self.student_tree.selection()
        if selected:
            student = self.student_tree.item(selected[0], "values")
            self.student_id_entry.delete(0, END)
            self.student_id_entry.insert(0, student[0])
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, student[1])
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, student[2])
            self.address_entry.delete(0, END)
            self.address_entry.insert(0, student[3])
            self.phone_entry.delete(0, END)
            self.phone_entry.insert(0, student[4])


# 主函数
if __name__ == "__main__":
    root = Tk()
    app = StudentManagementApp(root)
    root.mainloop()
    conn.close()
