import tkinter as tk

import customtkinter as ctk


class Header(ctk.CTkFrame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, corner_radius=0, **kwargs)
		self.pack(side=tk.TOP, fill=tk.X)

		self.mod_loader = SortingDropdown(self, ["Fabric", "Forge"])
		self.mod_loader.pack(side=tk.LEFT, padx=5, pady=5)

		self.sorting = SortingDropdown(self, ["Downloads", "Name", "Author"])
		self.sorting.pack(side=tk.LEFT, padx=5, pady=5)

		self.sorting = SortingDropdown(self, ["Ascending", "Descending"])
		self.sorting.pack(side=tk.LEFT, padx=5, pady=5)

		self.search = SearchBar(self)
		self.search.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)


class SearchBar(ctk.CTkEntry):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)
		self.bind("<Return>", lambda event: self.search())

	def search(self):
		content = self.get()
		self.delete(0, tk.END)
		return content


class SortingDropdown(ctk.CTkOptionMenu):
	def __init__(self, master=None, data: list = None, **kwargs):
		super().__init__(master, values=data, font=("Arial", 15), corner_radius=3, **kwargs)

		self.var = tk.StringVar(self)
		self.var.set(data[0])
