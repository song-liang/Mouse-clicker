import tkinter as tk
from tkinter import ttk, messagebox
from pynput import mouse, keyboard
import time
import json
import threading
import os

class MouseClickSimulator:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.LabelFrame(root, text="鼠标点击模拟器")
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 第一行：点击次数、时间间隔和快捷键提示
        ttk.Label(self.frame, text="点击次数:").grid(row=0, column=0, padx=(10, 5), sticky="w")
        self.click_count = tk.IntVar(value=10)
        ttk.Entry(self.frame, textvariable=self.click_count, width=8).grid(row=0, column=1, padx=(5, 10), sticky="w")
        
        ttk.Label(self.frame, text="间隔时间(秒):").grid(row=0, column=2, padx=(10, 5), sticky="w")
        self.interval = tk.DoubleVar(value=0.5)
        ttk.Entry(self.frame, textvariable=self.interval, width=8).grid(row=0, column=3, padx=(5, 10))
        
        ttk.Label(self.frame, text="快捷键: F8 开始/停止", foreground="gray").grid(row=0, column=4, sticky="w")
        
        # 状态显示(居中)
        self.status = tk.StringVar(value="准备就绪")
        ttk.Label(self.frame, textvariable=self.status).grid(row=2, column=0, columnspan=5, sticky="nsew")

        # 控制器
        self.controller = mouse.Controller()
        self.is_clicking = False
        self.listener = None
        
        # 启动键盘监听
        self.start_keyboard_listener()
    
    def start_keyboard_listener(self):
        def on_press(key):
            if key == keyboard.Key.f8:
                if not self.is_clicking:
                    self.start_clicking()
                else:
                    self.stop_clicking()
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
    
    def start_clicking(self):
        self.is_clicking = True
        self.status.set("点击中...按F8停止")
        
        def click_loop():
            count = self.click_count.get()
            interval = self.interval.get()
            
            for i in range(count):
                if not self.is_clicking:
                    break
                
                self.controller.click(mouse.Button.left)
                time.sleep(interval)
            
            self.is_clicking = False
            self.status.set("点击完成")
        
        threading.Thread(target=click_loop).start()
    
    def stop_clicking(self):
        self.is_clicking = False
        
    def show_records(self):
        """显示保存的记录文件"""
        self.record_list.delete(0, tk.END)
        records_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            for file in os.listdir(records_dir):
                if file.endswith(".json"):
                    self.record_list.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("错误", f"无法读取记录文件: {e}")
        self.status.set("已停止")


class MouseClickRecorder:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.LabelFrame(root, text="鼠标点击记录器")
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 控制按钮(优化缩放布局)
        btn_width = 12
        self.frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="buttons")
        ttk.Button(self.frame, text="开始记录", command=self.start_recording, width=btn_width).grid(row=0, column=0, padx=(5, 2), pady=5, sticky="nsew")
        ttk.Button(self.frame, text="停止记录", command=self.stop_recording, width=btn_width).grid(row=0, column=1, padx=(2, 2), pady=5, sticky="nsew")
        ttk.Button(self.frame, text="保存记录", command=self.save_recording, width=btn_width).grid(row=0, column=2, padx=(2, 2), pady=5, sticky="nsew")
        ttk.Button(self.frame, text="加载记录", command=self.load_recording, width=btn_width).grid(row=0, column=3, padx=(2, 5), pady=5, sticky="nsew")
        
        # 循环设置
        ttk.Label(self.frame, text="循环次数:").grid(row=1, column=0, padx=(1, 2), sticky="w")
        self.loop_count = tk.IntVar(value=1)
        ttk.Entry(self.frame, textvariable=self.loop_count, width=8).grid(row=1, column=1, padx=(1, 2), sticky="w")

        ttk.Label(self.frame, text="快捷键: F9 开始/停止", foreground="gray").grid(row=1, column=3, sticky="w")
        
        # 状态显示(居中)
        self.status = tk.StringVar(value="准备就绪")
        ttk.Label(self.frame, textvariable=self.status).grid(row=2, column=0, columnspan=5, sticky="nsew")
        
        # # 文件记录显示区域
        # self.record_list = tk.Listbox(self.frame, height=2)
        # self.record_list.grid(row=3, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")
        # ttk.Button(self.frame, text="显示记录", command=self.show_records).grid(row=4, column=0, columnspan=5, pady=5)

        # 数据存储
        self.recordings = []
        self.current_recording = []
        self.is_recording = False
        self.is_playing = False
        self.listener = None
        
        # 启动键盘监听
        self.start_keyboard_listener()
    
    def start_keyboard_listener(self):
        def on_press(key):
            if key == keyboard.Key.f9:
                if not self.is_playing:
                    self.start_playback()
                else:
                    self.stop_playback()
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
    
    # def show_records(self):
    #     """显示保存的记录文件"""
    #     self.record_list.delete(0, tk.END)
    #     records_dir = os.path.dirname(os.path.abspath(__file__))
    #     try:
    #         for file in os.listdir(records_dir):
    #             if file.endswith(".json"):
    #                 self.record_list.insert(tk.END, file)
    #     except Exception as e:
    #         messagebox.showerror("错误", f"无法读取记录文件: {e}")
            
    def start_recording(self):
        self.is_recording = True
        self.current_recording = []
        self.status.set("记录中...点击停止记录按钮结束")
        
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                self.current_recording.append({
                    "time": time.time(),
                    "x": x,
                    "y": y
                })
        
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()
    
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.mouse_listener.stop()
            
            # 移除最后一次点击（停止按钮的点击）
            if self.current_recording:
                self.current_recording.pop()
            
            # 计算时间间隔
            if len(self.current_recording) > 1:
                for i in range(1, len(self.current_recording)):
                    self.current_recording[i]["interval"] = self.current_recording[i]["time"] - self.current_recording[i-1]["time"]
                
                self.recordings.append(self.current_recording)
                self.status.set(f"已记录 {len(self.current_recording)} 次点击")
            else:
                self.status.set("记录失败: 点击次数不足")
    
    def save_recording(self):
        if not self.recordings:
            self.status.set("没有可保存的记录")
            return
            
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json")],
            initialfile=f"mouse_{time.strftime('%Y%m%d_%H%M%S')}"
        )
        if not filename:
            return
            
        try:
            with open(filename, 'w') as f:
                json.dump(self.recordings[-1], f, indent=4)
            self.status.set(f"记录已保存到 {filename}")
        except Exception as e:
            self.status.set(f"保存失败: {e}")
    
    def load_recording(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json")],
            title="选择要加载的记录文件"
        )
        if not filename:
            return
            
        try:
            with open(filename, "r") as f:
                self.recordings.append(json.load(f))
            self.status.set(f"已加载 {len(self.recordings[-1])} 次点击记录")
        except Exception as e:
            self.status.set(f"加载失败: {e}")
    
    def start_playback(self):
        if not self.recordings:
            self.status.set("没有可播放的记录")
            return
        
        self.is_playing = True
        self.status.set("播放中...按F9停止")
        
        def playback_loop():
            recording = self.recordings[-1]
            loops = self.loop_count.get()
            
            for _ in range(loops):
                if not self.is_playing:
                    break
                
                controller = mouse.Controller()
                
                for i, event in enumerate(recording):
                    if not self.is_playing:
                        break
                    
                    controller.position = (event["x"], event["y"])
                    controller.click(mouse.Button.left)
                    
                    if i < len(recording)-1 and "interval" in recording[i+1]:
                        time.sleep(recording[i+1]["interval"])
                
                # 循环间隔1秒
                if self.is_playing:
                    time.sleep(1)
            
            self.is_playing = False
            self.status.set("播放完成")
        
        threading.Thread(target=playback_loop).start()
    
    def stop_playback(self):
        self.is_playing = False
        self.status.set("播放已停止")


def main():
    root = tk.Tk()
    root.title("鼠标控制器")
    
    # 创建两个页面
    simulator = MouseClickSimulator(root)
    recorder = MouseClickRecorder(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()