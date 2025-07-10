import customtkinter as ctk

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("800x600")
        self.resizable(False, False)
        self.attributes("-alpha", 0.0)  

        self.label_title = ctk.CTkLabel(self, text="LunarchSysInfo", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(20, 10))

        self.label_version = ctk.CTkLabel(self, text="Версия: 1.0.0", font=ctk.CTkFont(size=14))
        self.label_version.pack(pady=5)

        self.label_author = ctk.CTkLabel(self, text="Разработчик: Lunarch Project", font=ctk.CTkFont(size=14))
        self.label_author.pack(pady=5)

        self.label_description = ctk.CTkLabel(
            self,
            text=(
                "LunarchSysInfo is a lightweight system information tool,\n"
                "inspired by AIDA64, developed using Python and customtkinter.\n\n"
                "Features include:\n"
                "- CPU, RAM, Disk, and OS details\n"
                "- Real-time system stats update\n"
                "- Simple and modern user interface\n\n"
                "This project is open-source and constantly evolving.\n"
                "Feel free to contribute or suggest improvements!"
            ),
            font=ctk.CTkFont(family="Cascadia Code", size=18),
            justify="center"
        )

        self.label_description.pack(pady=15)

        self.button_close = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.button_close.pack(pady=10)

        self.fade_in()  

    def fade_in(self, alpha=0.0):
        alpha += 0.05
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(15, lambda: self.fade_in(alpha))
