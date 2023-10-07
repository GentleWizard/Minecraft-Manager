import tkinter as tk

import customtkinter as ctk


class Header(ctk.CTkFrame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, corner_radius=0, **kwargs)
		self.pack(side=tk.TOP, fill=tk.X)

		self.toggle_filters = ctk.CTkButton(self, text="Filter", font=("Arial", 15))
		self.toggle_filters.configure(command=master.master.toggle_filters, corner_radius=3, width=55)
		self.toggle_filters.pack(side=tk.LEFT, padx=5, pady=5)

		self.search = ctk.CTkEntry(self, font=("Arial", 15), corner_radius=3, placeholder_text="Search")
		self.search.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)

		self.sorting = SortingDropdown(self, ['Relevance', 'Downloads', 'Follows', 'Newest', 'Updated'])
		self.sorting.pack(side=tk.RIGHT, padx=5, pady=5)


class SortingDropdown(ctk.CTkOptionMenu):
	def __init__(self, master=None, data: list = None, **kwargs):
		super().__init__(master, values=data, font=("Arial", 15), corner_radius=3, command=self.change, **kwargs)

		self.var = tk.StringVar(self)
		self.var.set(data[0])

	def change(self, *args):
		self.var.set(self.get())
