import tkinter as tk
from datetime import datetime, timedelta
import json
import os

class WorkTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("工时计时器")
        self.root.geometry("400x200")
        
        # 数据文件路径
        self.data_file = "timer_data.json"
        
        # 初始化计时器变量
        self.is_working = False
        self.start_time = None
        self.elapsed_time = self.load_elapsed_time()
        self.after_id = None

        # 创建左右布局框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')
        
        # 左侧框架（原有内容）
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 创建时间显示标签
        self.time_label = tk.Label(
            self.left_frame,
            text="00:00:00",
            font=("Arial", 30)
        )
        self.time_label.pack_forget()  # 取消原有的pack
        self.time_label.pack(in_=self.left_frame, pady=20)
        
        # 右侧框架（新增控件）
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, padx=10)
        
        # 创建时间调整框架
        self.adjust_frame = tk.Frame(self.right_frame)
        self.adjust_frame.pack(pady=20)
        
        # 创建输入框
        self.time_entry = tk.Entry(self.adjust_frame, width=8)
        self.time_entry.insert(0, "0")
        self.time_entry.pack(side=tk.LEFT, padx=2)
        
        # 创建分钟标签
        tk.Label(self.adjust_frame, text="分钟").pack(side=tk.LEFT)
        
        # 创建加减按钮框架
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack()
        
        # 添加按钮
        self.add_button = tk.Button(
            self.button_frame,
            text="+",
            command=lambda: self.adjust_time(1),
            width=3
        )
        self.add_button.pack(side=tk.LEFT, padx=2)
        
        self.subtract_button = tk.Button(
            self.button_frame,
            text="-",
            command=lambda: self.adjust_time(-1),
            width=3
        )
        self.subtract_button.pack(side=tk.LEFT, padx=2)
        
        # 将原有按钮移动到左侧框架
        self.toggle_button = tk.Button(
            self.left_frame,
            text="开始搬砖",
            command=self.toggle_timer,
            width=15,
            height=2,
            bg="green",
            fg="white",
            font=("Arial", 12)
        )
        self.toggle_button.pack_forget()  # 取消原有的pack
        self.toggle_button.pack(in_=self.left_frame, pady=10)
        
        self.reset_button = tk.Button(
            self.left_frame,
            text="重置",
            command=self.reset_timer,
            width=8,
            height=1,
            font=("Arial", 8)
        )
        self.reset_button.pack_forget()  # 取消原有的pack
        self.reset_button.pack(in_=self.left_frame, side=tk.BOTTOM, pady=10)

        # 添加窗口关闭事件处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化时显示加载的时间
        self.update_display()

    def load_elapsed_time(self):
        """从文件加载累计时间"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    return timedelta(seconds=data.get('elapsed_seconds', 0))
        except Exception as e:
            print(f"加载数据失败: {e}")
        return timedelta()

    def save_elapsed_time(self):
        """保存累计时间到文件"""
        try:
            # 如果正在计时，先更新总时间
            if self.is_working and self.start_time:
                self.elapsed_time += datetime.now() - self.start_time
                self.start_time = datetime.now()

            data = {
                'elapsed_seconds': self.elapsed_time.total_seconds()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def on_closing(self):
        """窗口关闭时的处理"""
        self.save_elapsed_time()
        self.root.destroy()

    def toggle_timer(self):
        if not self.is_working:
            # 开始计时
            self.is_working = True
            self.toggle_button.config(text="这B班就上到这了", bg="red")
            self.start_time = datetime.now()
            self.update_timer()
        else:
            # 停止计时
            self.is_working = False
            self.toggle_button.config(text="开始工作", bg="green")
            if self.after_id:
                self.root.after_cancel(self.after_id)
            if self.start_time:
                self.elapsed_time += datetime.now() - self.start_time

    def update_display(self):
        """更新显示的时间"""
        hours = int(self.elapsed_time.total_seconds() // 3600)
        minutes = int((self.elapsed_time.total_seconds() % 3600) // 60)
        seconds = int(self.elapsed_time.total_seconds() % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)

    def update_timer(self):
        if self.is_working:
            current_time = datetime.now()
            total_elapsed = self.elapsed_time + (current_time - self.start_time)
            hours = int(total_elapsed.total_seconds() // 3600)
            minutes = int((total_elapsed.total_seconds() % 3600) // 60)
            seconds = int(total_elapsed.total_seconds() % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            
            self.after_id = self.root.after(1000, self.update_timer)

    def reset_timer(self):
        """重置计时器并清除保存的数据"""
        self.is_working = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.time_label.config(text="00:00:00")
        self.toggle_button.config(text="开始工作", bg="green")
        if self.after_id:
            self.root.after_cancel(self.after_id)
        # 清除保存的数据
        self.save_elapsed_time()

    def adjust_time(self, direction):
        """调整计时器时间
        direction: 1 表示增加时间，-1 表示减少时间"""
        try:
            minutes = int(self.time_entry.get())
            if minutes <= 0:
                return
                
            adjustment = timedelta(minutes=minutes * direction)
            # 如果正在计时，先更新当前累计时间
            if self.is_working and self.start_time:
                self.elapsed_time += datetime.now() - self.start_time
                self.start_time = datetime.now()
                
            new_time = self.elapsed_time + adjustment
            
            # 确保时间不会变成负数
            if new_time.total_seconds() < 0:
                new_time = timedelta()
                
            self.elapsed_time = new_time
            self.update_display()
            self.save_elapsed_time()
        except ValueError:
            # 输入无效时不做任何操作
            pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    timer = WorkTimer()
    timer.run() 