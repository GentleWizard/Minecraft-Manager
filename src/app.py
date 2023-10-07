# This program is for managing Minecraft mods.
import asyncio
import time
import tkinter as tk

from async_tkinter_loop import async_handler, async_mainloop

from src.filter import FilterBar
from src.results import Results
from src.search import modrinth_search


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Minecraft Mod Manager")
		self.geometry("700x400")

		self.results = Results(self)

		self.facets = []
		self.search_limit = 10
		self.search_offset = 0
		self.results.header.search.bind("<Return>", lambda _: self.search())

		self.sidebar = FilterBar(self)
		self.sidebar_visible = True
		self.toggle_filters()

	def toggle_filters(self):
		if self.sidebar_visible:
			self.sidebar.pack_forget()  # or grid_remove, or place_forget
			self.sidebar_visible = False
		else:
			self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)  # or grid, or place
			self.sidebar_visible = True

	@async_handler
	async def search(self):
		query = self.results.header.search.get()
		search_index = self.results.header.sorting.var.get()
		self.results.header.search.delete(0, tk.END)
		self.results.header.search.configure(placeholder_text='Searching...')
		self.results.header.search.configure(state=tk.DISABLED)

		current_time = time.time()
		result = await asyncio.create_task(
			modrinth_search(query, search_index, self.search_limit, self.search_offset))
		time_taken = time.time() - current_time
		print(f"Time taken: {time_taken}")

		self.results.header.search.configure(state=tk.NORMAL)
		self.results.header.search.configure(placeholder_text='Search')
		self.results.header.search.delete(0, tk.END)
		self.results.focus_set()
		self.results.display_projects(result.values())


if __name__ == "__main__":
	app = App()
	async_mainloop(app)
