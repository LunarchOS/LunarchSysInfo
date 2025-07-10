import customtkinter as ctk
import platform
import psutil
import cpuinfo
from about import AboutWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SystemInfoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LunarchSysInfo")
        self.geometry("1280x800")
        self.attributes("-alpha", 0.0)

        self.custom_font_big = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        self.custom_font_text = ctk.CTkFont(family="Cascadia Code", size=19)

        self.label = ctk.CTkLabel(self, text="🖥️ LunarchSysInfo — About System", font=self.custom_font_big)
        self.label.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=(0, 10))

        self.button_update = ctk.CTkButton(button_frame, text="🔄 Update data", command=self.update_all, font=self.custom_font_text)
        self.button_update.pack(side="left", padx=10)

        self.button_about = ctk.CTkButton(button_frame, text="ℹ️ About", command=self.open_about, font=self.custom_font_text)
        self.button_about.pack(side="left", padx=10)

        self.tabview = ctk.CTkTabview(self, width=1200, height=700)
        self.tabview.pack(padx=20, pady=10)

        self.tabs = {
            "CPU": self.tabview.add("CPU"),
            "RAM": self.tabview.add("RAM"),
            "Disk": self.tabview.add("Disk"),
            "OS": self.tabview.add("OS"),
            "All": self.tabview.add("All")
        }

        self.textboxes = {}
        for name, tab in self.tabs.items():
            box = ctk.CTkTextbox(tab, width=1150, height=650, font=self.custom_font_text)
            box.pack(padx=10, pady=10)
            self.textboxes[name] = box

        self.update_all()
        self.after(0, self.fade_in)

    def fade_in(self, alpha=0.0):
        alpha += 0.02
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(10, lambda: self.fade_in(alpha))

    def update_all(self):
        self.update_cpu()
        self.update_ram()
        self.update_disk()
        self.update_os()
        self.update_all_in_one()

    def update_cpu(self):
        cpu = cpuinfo.get_cpu_info()
        text = f"""
CPU: {cpu['brand_raw']}
Architecture: {platform.machine()}
Frequency: {psutil.cpu_freq().current:.2f} MHz
Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} log.
"""
        self.textboxes["CPU"].delete("1.0", ctk.END)
        self.textboxes["CPU"].insert(ctk.END, text)

    def update_ram(self):
        ram = psutil.virtual_memory()
        text = f"""
Total: {ram.total / 1024**3:.2f} GB
Available: {ram.available / 1024**3:.2f} GB
Used: {ram.used / 1024**3:.2f} GB ({ram.percent}%)
"""
        self.textboxes["RAM"].delete("1.0", ctk.END)
        self.textboxes["RAM"].insert(ctk.END, text)

    def update_disk(self):
        text = ""
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                text += f"{part.device} [{part.mountpoint}]\n  {usage.used / 1024**3:.1f} / {usage.total / 1024**3:.1f} GB ({usage.percent}%)\n\n"
            except PermissionError:
                continue

        self.textboxes["Disk"].delete("1.0", ctk.END)
        self.textboxes["Disk"].insert(ctk.END, text)

    def update_os(self):
        text = f"""
OS: {platform.system()} {platform.release()}
Version: {platform.version()}
Name of computer: {platform.node()}
Architecture: {platform.machine()}
"""
        self.textboxes["OS"].delete("1.0", ctk.END)
        self.textboxes["OS"].insert(ctk.END, text)

    def update_all_in_one(self):
        self.textboxes["All"].delete("1.0", ctk.END)
        all_info = ""
        for name in ["OS", "CPU", "RAM", "Disk"]:
            all_info += f"=== {name.upper()} ===\n"
            all_info += self.textboxes[name].get("1.0", ctk.END)
            all_info += "\n"

        self.textboxes["All"].insert(ctk.END, all_info)

    def open_about(self):
        about_window = AboutWindow(self)
        about_window.grab_set()

if __name__ == "__main__":
    app = SystemInfoApp()
    app.mainloop()
