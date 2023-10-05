import tkinter as tk

import customtkinter as ctk


class Footer(ctk.CTkFrame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, corner_radius=0, **kwargs)
		self.pack(side=tk.BOTTOM, fill=tk.X)

		self.page = NavButton(self, text="Back", font=("Arial", 15))
		self.page.pack(side=tk.LEFT, padx=5, pady=5)

		self.page = ctk.CTkLabel(self, text="Page 1/1", font=("Arial", 15))
		self.page.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

		self.page = NavButton(self, text="Next", font=("Arial", 15))
		self.page.pack(side=tk.RIGHT, padx=5, pady=5)


class NavButton(ctk.CTkButton):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, corner_radius=3, **kwargs)
