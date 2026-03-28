import tkinter as tk
import random
from tkinter import messagebox
import sys
import json
import os
import webbrowser

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных чисел")
        self.root.geometry("500x450")
        self.root.minsize(400, 350)
        
        self.current_theme = "light"
        self.theme_colors = {
            "light": {
                "bg": "white",
                "fg": "black",
                "frame_bg": "lightgray",
                "entry_bg": "white",
                "entry_fg": "black",
                "button_bg": "SystemButtonFace"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "white",
                "frame_bg": "#3c3c3c",
                "entry_bg": "#4a4a4a",
                "entry_fg": "white",
                "button_bg": "#4a4a4a"
            }
        }
        
        self.settings_file = "generator_settings.json"
        self.load_settings()
        
        self.animation_id = None
        self.skip_animation = False
        
        self.create_menu()
        
        self.title_label = tk.Label(root, text="Генератор случайных чисел", 
                               font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        frame = tk.Frame(root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Минимальное число:").grid(row=0, column=0, padx=5, pady=5)
        self.min_entry = tk.Entry(frame, width=15)
        self.min_entry.grid(row=0, column=1, padx=5, pady=5)
        self.min_entry.insert(0, str(self.saved_min))
        
        tk.Label(frame, text="Максимальное число:").grid(row=1, column=0, padx=5, pady=5)
        self.max_entry = tk.Entry(frame, width=15)
        self.max_entry.grid(row=1, column=1, padx=5, pady=5)
        self.max_entry.insert(0, str(self.saved_max))
        
        self.generate_btn = tk.Button(root, text="Сгенерировать", 
                                command=self.generate_number_with_animation,
                                font=("Arial", 12), bg="green", fg="white")
        self.generate_btn.pack(pady=10)
        
        self.result_label = tk.Label(root, text="Нажмите кнопку для генерации", 
                                     font=("Arial", 14), fg="blue", cursor="hand2")
        self.result_label.pack(pady=20)
        
        self.result_label.bind("<Button-1>", self.copy_number)
        
        self.current_number = None
        
        self.apply_theme()
    
    def generate_number_with_animation(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            
            if min_val >= max_val:
                messagebox.showerror("Ошибка", "Минимальное число не может быть больше максимального!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа!")
            return
        
        if self.skip_animation:
            self.generate_number()
            return
        
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        
        self.animate_generation(0)
    
    def animate_generation(self, step):
        if step < 10:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            temp_num = random.randint(min_val, max_val)
            self.result_label.config(text=f"Генерация... {temp_num}", fg="orange")
            self.animation_id = self.root.after(50, lambda: self.animate_generation(step + 1))
        else:
            self.generate_number()
            self.animation_id = None
    
    def generate_number(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            
            if min_val >= max_val:
                messagebox.showerror("Ошибка", "Минимальное число не может быть больше максимального!")
                return
            
            random_num = random.randint(min_val, max_val)
            self.current_number = random_num
            self.result_label.config(text=f"Случайное число: {random_num}\n(нажмите для копирования)", 
                                     fg="green")
            
            self.save_settings()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа!")
    
    def copy_number(self, event):
        if self.current_number is not None:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(self.current_number))
            self.root.update()
            
            original_text = self.result_label.cget("text")
            self.result_label.config(text=f"✅ Скопировано: {self.current_number}", 
                                     fg="orange")
            self.root.after(1500, lambda: self.result_label.config(
                text=original_text, fg="green"))
        else:
            messagebox.showinfo("Информация", "Сначала сгенерируйте число!")
    
    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(anchor="nw", padx=10, pady=5)
        
        self.menu_button = tk.Canvas(menu_frame, width=30, height=25, 
                                     cursor="hand2", bg=self.root.cget("bg"),
                                     highlightthickness=0)
        self.menu_button.pack(side="left")
        
        self.menu_button.create_line(5, 7, 25, 7, width=2, fill="black")
        self.menu_button.create_line(5, 12, 25, 12, width=2, fill="black")
        self.menu_button.create_line(5, 17, 25, 17, width=2, fill="black")
        
        self.menu_button.bind("<Button-1>", self.show_menu)
        
        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Пропустить анимацию", command=self.toggle_skip_animation)
        self.popup_menu.add_command(label="Сменить тему", command=self.toggle_theme)
        self.popup_menu.add_command(label="О программе", command=self.info_window)
        self.popup_menu.add_command(label="Автор", command=self.open_channel)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Выход", command=self.root.quit)
    
    def open_channel(self):
        webbrowser.open("https://www.youtube.com/@ЛёгкиеПрограммы")
    
    def toggle_skip_animation(self):
        self.skip_animation = not self.skip_animation
        self.save_settings()
        if self.skip_animation:
            messagebox.showinfo("Анимация", "Анимация отключена")
        else:
            messagebox.showinfo("Анимация", "Анимация включена")
    
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.save_settings()
    
    def apply_theme(self):
        colors = self.theme_colors[self.current_theme]
        
        self.root.configure(bg=colors["bg"])
        self.title_label.configure(bg=colors["bg"], fg=colors["fg"])
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=colors["frame_bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=colors["frame_bg"], fg=colors["fg"])
                    elif isinstance(child, tk.Entry):
                        child.configure(bg=colors["entry_bg"], fg=colors["entry_fg"])
                    elif isinstance(child, tk.Button):
                        child.configure(bg=colors["button_bg"], fg=colors["fg"])
        
        self.generate_btn.configure(bg="green" if self.current_theme == "light" else "#006400")
        
        if self.current_number is None:
            self.result_label.configure(bg=colors["bg"], fg="blue")
        else:
            self.result_label.configure(bg=colors["bg"])
        
        self.menu_button.configure(bg=colors["bg"])
        self.menu_button.delete("all")
        color = "white" if self.current_theme == "dark" else "black"
        self.menu_button.create_line(5, 7, 25, 7, width=2, fill=color)
        self.menu_button.create_line(5, 12, 25, 12, width=2, fill=color)
        self.menu_button.create_line(5, 17, 25, 17, width=2, fill=color)
    
    def save_settings(self):
        try:
            settings = {
                "min_value": self.min_entry.get(),
                "max_value": self.max_entry.get(),
                "theme": self.current_theme,
                "skip_animation": self.skip_animation
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.saved_min = int(settings.get("min_value", 1))
                    self.saved_max = int(settings.get("max_value", 100))
                    self.current_theme = settings.get("theme", "light")
                    self.skip_animation = settings.get("skip_animation", False)
            else:
                self.saved_min = 1
                self.saved_max = 100
                self.current_theme = "light"
                self.skip_animation = False
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            self.saved_min = 1
            self.saved_max = 100
            self.current_theme = "light"
            self.skip_animation = False
    
    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()
    
    def info_window(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("О программе")
        info_window.geometry("350x250")
        info_window.minsize(300, 200)
        
        colors = self.theme_colors[self.current_theme]
        info_window.configure(bg=colors["bg"])
        
        info_text = tk.Label(info_window,
                            text="Генератор случайных чисел\n\n"
                                 "Версия: 2.0\n"
                                 "Python: " + str(sys.version_info.major) + "." + 
                                 str(sys.version_info.minor) + "\n"
                                 "Tkinter: установлен\n\n"
                                 "Возможности:\n"
                                 "• Темная/светлая тема\n"
                                 "• Анимация генерации\n"
                                 "• Копирование в буфер обмена\n"
                                 "• Автосохранение настроек",
                            bg=colors["bg"], fg=colors["fg"], justify="left")
        info_text.pack(pady=20)
        
        close_btn = tk.Button(info_window, text="Закрыть", 
                             command=info_window.destroy,
                             bg="red", fg="white")
        close_btn.pack(pady=10)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = RandomNumberGenerator(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("ОШИБКА:")
        print(traceback.format_exc())
        input("Нажмите Enter для выхода...")