"""
玩家管理界面模块

提供玩家信息的图形化管理界面，包括：
- 玩家列表显示
- 玩家信息的增删改查
- 数据的可视化展示
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controller.playerController import PlayerController
from core.eventmanager import EventManager


class PlayerApp:
    def __init__(self, root):
        """
        初始化玩家管理界面
        
        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title("修仙者管理系统")
        self.root.geometry("1200x800")  # 设置窗口大小
        
        self.event_manager = EventManager()
        self.player_controller = PlayerController(self.event_manager)

        self.create_widgets()
        self.query_players()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建顶部按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # 添加按钮
        self.btn_add = ttk.Button(button_frame, text="新增修仙者", command=self.add_player)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_update = ttk.Button(button_frame, text="修改信息", command=self.update_player)
        self.btn_update.pack(side=tk.LEFT, padx=5)

        self.btn_delete = ttk.Button(button_frame, text="删除修仙者", command=self.delete_player)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_refresh = ttk.Button(button_frame, text="刷新列表", command=self.query_players)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)

        # 创建Treeview
        columns = (
            "ID", "姓名", "年龄", "性别", "灵根", "境界", "突破概率", "经验",
            "宗主", "父ID", "母ID", "师ID", "伴侣ID", "属性", "状态"
        )
        
        # 创建带滚动条的框架
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # 创建Treeview并配置滚动条
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        # 配置滚动条
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # 设置列标题和宽度
        column_widths = {
            "ID": 50, "姓名": 100, "年龄": 50, "性别": 50,
            "灵根": 100, "境界": 80, "突破概率": 80, "经验": 80,
            "宗主": 50, "父ID": 50, "母ID": 50, "师ID": 50,
            "伴侣ID": 50, "属性": 150, "状态": 50
        }

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=column_widths[col], anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def sort_treeview(self, col):
        """排序功能"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort()
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)

    def query_players(self):
        """查询并显示所有玩家"""
        # 清空现有数据
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 获取玩家列表
        result = self.player_controller.get_player_list()
        if result['success']:
            for player in result['data']:
                # 转换性别显示
                sex_display = "女" if player['sex'] == 0 else "男"
                # 转换状态显示
                status_display = "已故" if player['isDead'] == 1 else "在世"
                
                self.tree.insert("", tk.END, values=(
                    player['id'],
                    player['name'],
                    player['age'],
                    sex_display,
                    player['root'],
                    player['realm_level'],
                    player['base_breakup_probability'],
                    player['current_exp'],
                    "是" if player['isMaster'] == 1 else "否",
                    player['father_id'],
                    player['mother_id'],
                    player['teacher_id'],
                    player['companion_id'],
                    player['attribute'],
                    status_display
                ))
        else:
            messagebox.showerror("错误", result['message'])

    def create_player_form(self, window, player_data=None):
        """创建玩家表单"""
        fields = [
            ("姓名", 'name', str),
            ("年龄", 'age', int),
            ("性别(0女/1男)", 'sex', int),
            ("灵根", 'root', str),
            ("境界", 'realm_level', int),
            ("突破概率", 'base_breakup_probability', float),
            ("经验", 'current_exp', float),
            ("宗主(0否/1是)", 'isMaster', int),
            ("父ID", 'father_id', int),
            ("母ID", 'mother_id', int),
            ("师父ID", 'teacher_id', int),
            ("伴侣ID", 'companion_id', int),
            ("属性", 'attribute', str)
        ]

        entries = {}
        for i, (label, field, _) in enumerate(fields):
            ttk.Label(window, text=label).grid(row=i, column=0, padx=5, pady=2)
            entry = ttk.Entry(window)
            entry.grid(row=i, column=1, padx=5, pady=2)
            if player_data and field in player_data:
                entry.insert(0, str(player_data[field]))
            entries[field] = entry

        return entries

    def add_player(self):
        """添加玩家窗口"""
        window = tk.Toplevel(self.root)
        window.title("新增修仙者")
        window.geometry("400x500")

        entries = self.create_player_form(window)

        def submit():
            try:
                player_data = {
                    field: type_(entries[field].get())
                    for field, type_ in [
                        ('name', str), ('age', int), ('sex', int),
                        ('root', str), ('realm_level', int),
                        ('base_breakup_probability', float),
                        ('current_exp', float), ('isMaster', int),
                        ('father_id', int), ('mother_id', int),
                        ('teacher_id', int), ('companion_id', int),
                        ('attribute', str)
                    ]
                }
                result = self.player_controller.create_player(player_data)
                if result['success']:
                    messagebox.showinfo("成功", "添加修仙者成功")
                    window.destroy()
                    self.query_players()
                else:
                    messagebox.showerror("错误", result['message'])
            except ValueError as e:
                messagebox.showerror("输入错误", f"请检查输入格式: {str(e)}")

        ttk.Button(window, text="提交", command=submit).grid(row=13, column=0, columnspan=2, pady=10)

    def update_player(self):
        """更新玩家信息"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个修仙者")
            return

        player_id = self.tree.item(selected[0])['values'][0]
        result = self.player_controller.get_player_with_companion(player_id)
        
        if not result['success']:
            messagebox.showerror("错误", result['message'])
            return

        window = tk.Toplevel(self.root)
        window.title("修改修仙者信息")
        window.geometry("400x500")

        entries = self.create_player_form(window, result['data'])

        def submit():
            try:
                player_data = {
                    field: type_(entries[field].get())
                    for field, type_ in [
                        ('name', str), ('age', int), ('sex', int),
                        ('root', str), ('realm_level', int),
                        ('base_breakup_probability', float),
                        ('current_exp', float), ('isMaster', int),
                        ('father_id', int), ('mother_id', int),
                        ('teacher_id', int), ('companion_id', int),
                        ('attribute', str)
                    ]
                }
                result = self.player_controller.update_player(player_id, player_data)
                if result['success']:
                    messagebox.showinfo("成功", "更新修仙者信息成功")
                    window.destroy()
                    self.query_players()
                else:
                    messagebox.showerror("错误", result['message'])
            except ValueError as e:
                messagebox.showerror("输入错误", f"请检查输入格式: {str(e)}")

        ttk.Button(window, text="提交", command=submit).grid(row=13, column=0, columnspan=2, pady=10)

    def delete_player(self):
        """删除玩家"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个修仙者")
            return

        player_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("确认", "确定要删除该修仙者吗？"):
            result = self.player_controller.delete_player(player_id)
            if result['success']:
                messagebox.showinfo("成功", "删除修仙者成功")
                self.query_players()
            else:
                messagebox.showerror("错误", result['message'])

    def on_tree_double_click(self, event):
        """双击行时触发更新操作"""
        self.update_player()

    def close(self):
        """关闭应用程序"""
        if hasattr(self, 'player_controller'):
            self.player_controller.close()

def main():
    """程序入口函数"""
    root = tk.Tk()
    app = PlayerApp(root)
    try:
        root.mainloop()
    finally:
        app.close()

if __name__ == "__main__":
    main()