import tkinter as tk

class ViewManager:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.views = {}
        
        # 配置根窗口
        self.root.title("界面管理系统")
        self.root.geometry("800x600")
        
    def register_view(self, view_name, view_class):
        """注册一个新界面"""
        self.views[view_name] = view_class
        
    def show_view(self, view_name):
        """显示指定的界面"""
        # 如果当前有显示的界面，先隐藏它
        if self.current_view:
            self.current_view.pack_forget()
            
        # 创建并显示新界面
        if view_name in self.views:
            self.current_view = self.views[view_name](self.root)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        else:
            raise ValueError(f"未找到界面: {view_name}") 