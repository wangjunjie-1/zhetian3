import tkinter as tk
from .view_manager import ViewManager
from .sample_views import HomeView, SettingsView

def main():
    root = tk.Tk()
    
    # 创建视图管理器
    view_manager = ViewManager(root)
    root.view_manager = view_manager  # 将视图管理器附加到root以便访问
    
    # 注册视图
    view_manager.register_view("home", HomeView)
    view_manager.register_view("settings", SettingsView)
    
    # 显示初始视图
    view_manager.show_view("home")
    
    root.mainloop()

if __name__ == "__main__":
    main() 