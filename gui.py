"""
Tkinter GUI for Daily Fortune App
Simple, clean interface for fortune display
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import platform
import sys
from fortune_data import FortuneManager

class FortuneApp:
    def __init__(self):
        self.fortune_manager = FortuneManager()
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("今日幸運籤餅")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Create and arrange GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="今日幸運籤餅", 
                               font=("Microsoft JhengHei", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Date
        today = datetime.now().strftime("%B %d, %Y")
        date_label = ttk.Label(main_frame, text=today, 
                              font=("Arial", 12))
        date_label.grid(row=1, column=0, pady=(0, 20))
        
        # Fortune display frame
        fortune_frame = ttk.LabelFrame(main_frame, text="您的籤餅", padding="20")
        fortune_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        fortune_frame.columnconfigure(0, weight=1)
        fortune_frame.rowconfigure(0, weight=1)
        
        # Fortune text
        self.fortune_text = tk.Text(fortune_frame, wrap=tk.WORD, font=("Microsoft JhengHei", 14),
                                   height=6, bg="#f8f9fa", relief="flat", 
                                   state="disabled", cursor="arrow")
        self.fortune_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for fortune text
        scrollbar = ttk.Scrollbar(fortune_frame, orient="vertical", 
                                 command=self.fortune_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.fortune_text.configure(yscrollcommand=scrollbar.set)
        
        # Button frame - two rows for better layout
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # First row buttons
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        
        self.generate_button = ttk.Button(button_frame, text="獲取今日籤餅", 
                                         command=self.generate_fortune)
        self.generate_button.grid(row=0, column=0, padx=(0, 2), pady=(0, 5), sticky=(tk.W, tk.E))
        
        self.show_today_button = ttk.Button(button_frame, text="今日籤餅", 
                                           command=self.show_today_fortune)
        self.show_today_button.grid(row=0, column=1, padx=2, pady=(0, 5), sticky=(tk.W, tk.E))
        
        stats_button = ttk.Button(button_frame, text="查看統計", 
                                 command=self.show_stats)
        stats_button.grid(row=0, column=2, padx=2, pady=(0, 5), sticky=(tk.W, tk.E))
        
        quit_button = ttk.Button(button_frame, text="退出", 
                                command=self.root.quit)
        quit_button.grid(row=0, column=3, padx=(2, 0), pady=(0, 5), sticky=(tk.W, tk.E))
        
        # Second row - history button spanning full width
        history_button = ttk.Button(button_frame, text="歷史籤餅", 
                                   command=self.show_history_selection)
        history_button.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Load existing fortune or show welcome message
        self.load_initial_state()
        
    def load_initial_state(self):
        """Load today's fortune if it exists, or show welcome message"""
        existing_fortune = self.fortune_manager.get_todays_fortune()
        
        if existing_fortune:
            self.display_fortune(existing_fortune)
            self.generate_button.config(text="今日籤餅已生成", state="disabled")
            self.show_today_button.config(state="normal")
        else:
            if self.fortune_manager.can_generate_fortune():
                self.display_message("點擊「獲取今日籤餅」來接收您的每日籤餅！")
                self.show_today_button.config(state="disabled")
            else:
                self.display_message("您已經收到今日的籤餅了，明天再來吧！")
                self.generate_button.config(text="明天再來", state="disabled")
                self.show_today_button.config(state="normal")
    
    def display_fortune(self, fortune):
        """Display fortune in the text widget"""
        self.fortune_text.config(state="normal")
        self.fortune_text.delete(1.0, tk.END)
        
        # Add fortune text
        self.fortune_text.insert(tk.END, f'"{fortune["text"]}"\n\n')
        
        # Add category and timestamp
        category_text = f"類別: {fortune['category'].title()}\n"
        if 'generated_at' in fortune:
            timestamp = datetime.fromisoformat(fortune['generated_at']).strftime("%I:%M %p")
            category_text += f"生成時間: {timestamp}"
        
        self.fortune_text.insert(tk.END, category_text)
        
        # Center align and style the fortune text
        self.fortune_text.tag_configure("fortune", justify="center", font=("Microsoft JhengHei", 16, "italic"))
        self.fortune_text.tag_configure("meta", justify="center", font=("Microsoft JhengHei", 10), foreground="gray")
        
        self.fortune_text.tag_add("fortune", "1.0", "2.0")
        self.fortune_text.tag_add("meta", "3.0", tk.END)
        
        self.fortune_text.config(state="disabled")
    
    def display_message(self, message):
        """Display a message in the text widget"""
        self.fortune_text.config(state="normal")
        self.fortune_text.delete(1.0, tk.END)
        self.fortune_text.insert(tk.END, message)
        self.fortune_text.tag_configure("center", justify="center")
        self.fortune_text.tag_add("center", "1.0", tk.END)
        self.fortune_text.config(state="disabled")
    
    def show_message(self, title, message, msg_type="info"):
        """Show message with proper window focus for macOS app bundles"""
        # Bring window to front and focus for macOS app bundles
        if platform.system() == "Darwin" and getattr(sys, 'frozen', False):
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.after(100, lambda: self.root.attributes('-topmost', False))
            self.root.focus_force()
        
        if msg_type == "error":
            messagebox.showerror(title, message, parent=self.root)
        else:
            messagebox.showinfo(title, message, parent=self.root)

    def generate_fortune(self):
        """Generate and display today's fortune"""
        try:
            if not self.fortune_manager.can_generate_fortune():
                self.show_message("已經生成", 
                                "您已經收到今日的籤餅了！\n明天再來獲取新的籤餅。")
                return
            
            fortune = self.fortune_manager.generate_fortune()
            self.display_fortune(fortune)
            
            # Update button states
            self.generate_button.config(text="籤餅已生成！", state="disabled")
            self.show_today_button.config(state="normal")
            
            # Show success message
            self.show_message("籤餅已生成！", 
                            f'您今日的籤餅：\n\n"{fortune["text"]}"')
            
        except Exception as e:
            self.show_message("錯誤", f"生成籤餅失敗: {str(e)}", "error")
    
    def show_today_fortune(self):
        """Show today's fortune in alert window"""
        try:
            existing_fortune = self.fortune_manager.get_todays_fortune()
            
            if existing_fortune:
                timestamp = datetime.fromisoformat(existing_fortune['generated_at']).strftime("%H:%M")
                self.show_message("今日籤餅", 
                                f'您今日的籤餅：\n\n"{existing_fortune["text"]}"\n\n類別: {existing_fortune["category"].title()}\n生成時間: {timestamp}')
            else:
                self.show_message("今日籤餅", "尚未生成今日籤餅！\n請先點擊「獲取今日籤餅」。")
                
        except Exception as e:
            self.show_message("錯誤", f"無法顯示今日籤餅: {str(e)}", "error")
    
    def show_stats(self):
        """Show user statistics in a popup"""
        try:
            stats = self.fortune_manager.get_stats()
            
            if stats["total_fortunes"] == 0:
                self.show_message("統計資料", "尚未生成籤餅！\n獲取您的第一個籤餅來查看統計資料。")
                return
            
            stats_text = f"""籤餅統計：

總共獲得籤餅: {stats['total_fortunes']} 次
目前連續天數: {stats['streak']} 天
首次籤餅: {stats['first_fortune']}
最新籤餅: {stats['last_fortune']}

繼續保持！每天回來維持您的連續記錄。"""
            
            self.show_message("您的籤餅統計", stats_text)
            
        except Exception as e:
            self.show_message("錯誤", f"載入統計資料失敗: {str(e)}", "error")
    
    def show_history_selection(self):
        """Show date selection window for fortune history"""
        try:
            available_dates = self.fortune_manager.get_available_dates()
            
            if not available_dates:
                self.show_message("歷史籤餅", "尚無歷史籤餅記錄！\n開始使用後，您可以在這裡查看過往的籤餅。")
                return
            
            # Create selection window
            history_window = tk.Toplevel(self.root)
            history_window.title("選擇日期")
            history_window.geometry("300x400")
            history_window.resizable(False, False)
            
            # Center the window
            history_window.transient(self.root)
            history_window.grab_set()
            
            # Title
            title_label = ttk.Label(history_window, text="選擇要查看的日期", 
                                   font=("Microsoft JhengHei", 14, "bold"))
            title_label.pack(pady=10)
            
            # Date list frame
            list_frame = ttk.Frame(history_window)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Scrollable listbox
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            date_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                     font=("Arial", 11), height=15)
            date_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=date_listbox.yview)
            
            # Populate dates with formatted display
            for date_str in available_dates:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%Y年 %m月 %d日 (%A)")
                    date_listbox.insert(tk.END, formatted_date)
                except:
                    date_listbox.insert(tk.END, date_str)
            
            # Button frame
            button_frame = ttk.Frame(history_window)
            button_frame.pack(pady=10)
            
            def on_show_fortune():
                selection = date_listbox.curselection()
                if selection:
                    selected_date = available_dates[selection[0]]
                    history_window.destroy()
                    self.show_historical_fortune(selected_date)
                else:
                    self.show_message("選擇日期", "請選擇一個日期！")
            
            def on_cancel():
                history_window.destroy()
            
            show_button = ttk.Button(button_frame, text="查看籤餅", command=on_show_fortune)
            show_button.pack(side=tk.LEFT, padx=(0, 10))
            
            cancel_button = ttk.Button(button_frame, text="取消", command=on_cancel)
            cancel_button.pack(side=tk.LEFT)
            
            # Double-click to show
            date_listbox.bind('<Double-1>', lambda e: on_show_fortune())
            
        except Exception as e:
            self.show_message("錯誤", f"無法顯示歷史記錄: {str(e)}", "error")
    
    def show_historical_fortune(self, date_str: str):
        """Show fortune for specific historical date"""
        try:
            fortune = self.fortune_manager.get_fortune_by_date(date_str)
            
            if fortune:
                # Format date for display
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%Y年 %m月 %d日")
                except:
                    formatted_date = date_str
                
                timestamp = datetime.fromisoformat(fortune['generated_at']).strftime("%H:%M")
                
                self.show_message(f"{formatted_date} 的籤餅", 
                                f'"{fortune["text"]}"\n\n類別: {fortune["category"].title()}\n生成時間: {timestamp}')
            else:
                self.show_message("歷史籤餅", f"找不到 {date_str} 的籤餅記錄。")
                
        except Exception as e:
            self.show_message("錯誤", f"無法顯示歷史籤餅: {str(e)}", "error")
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()
        except Exception as e:
            self.show_message("應用程式錯誤", f"發生未預期的錯誤: {str(e)}", "error")
            self.root.quit()