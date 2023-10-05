import tkinter as tk

import customtkinter as ctk


class Results(ctk.CTkFrame):
	def __init__(self, master: any, **kwargs):
		super().__init__(master, **kwargs, corner_radius=0)
		self.pack(fill=tk.BOTH, expand=True)

	def get_results(self):
		pass
