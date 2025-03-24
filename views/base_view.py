import tkinter as tk

class BaseView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        
    def create_widgets(self):
        """
        创建界面组件，子类需要重写此方法
        """
        pass 