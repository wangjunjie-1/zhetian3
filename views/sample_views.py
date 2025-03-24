from .base_view import BaseView
import tkinter as tk

class HomeView(BaseView):
    def create_widgets(self):
        label = tk.Label(self, text="这是主页")
        label.pack(pady=20)
        
        # 添加一个按钮跳转到设置页面
        btn = tk.Button(self, text="进入设置", 
                       command=lambda: self.master.view_manager.show_view("settings"))
        btn.pack()

class SettingsView(BaseView):
    def create_widgets(self):
        label = tk.Label(self, text="这是设置页面")
        label.pack(pady=20)
        
        # 添加一个按钮返回主页
        btn = tk.Button(self, text="返回主页", 
                       command=lambda: self.master.view_manager.show_view("home"))
        btn.pack() 