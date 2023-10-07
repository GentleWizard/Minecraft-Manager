# This program is for managing Minecraft mods.
import asyncio
import time
import tkinter as tk

from async_tkinter_loop import async_handler, async_mainloop

from src.filter import FilterBar
from src.results import Results
from src.search import modrinth_search


class LoadingScreen(tk.Toplevel):
	def __init__(self, master=None):
		super().__init__(master)
		self.loading_label = tk.Label(self, text="Loading...", font=("Arial", 20))
		self.loading_label.pack(fill=tk.BOTH, expand=True)
		self.wm_attributes("-topmost", True)
		width = 350
		height = 150
		self.geometry(
			f"{width}x{height}+{(self.winfo_screenwidth() // 2) - (width // 2)}+{(self.winfo_screenheight() // 2) - (height // 2)}")


class App(tk.Tk):
	def __init__(self, width=800, height=500):
		super().__init__()
		self.iconify()
		self.loading_screen = LoadingScreen(self)
		self.loading_screen.overrideredirect(True)

		self.geometry(
			f"{width}x{height}+{int((self.winfo_screenwidth() // 2) - (width / 2))}+{int((self.winfo_screenheight() // 2) - (height / 2))}")
		self.loading_screen.update()

		self.title("Minecraft Mod Manager")

		self.results = Results(self)

		self.facets = []
		self.search_limit = 15
		self.search_offset = 0
		self.results.header.search.bind("<Return>", lambda _: self.search())

		self.search()
		self.sidebar = FilterBar(self)
		self.sidebar_visible = True
		self.toggle_filters()

		self.loading_screen.destroy()
		self.deiconify()
		self.attributes('-topmost', True)

	def toggle_filters(self):
		if self.sidebar_visible:
			self.sidebar.pack_forget()  # or grid_remove, or place_forget
			self.sidebar_visible = False
			self.results.manage_what_projects_are_displayed()
		else:
			self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)  # or grid, or place
			self.sidebar_visible = True
			self.results.manage_what_projects_are_displayed()

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
	app = App(width=825, height=425)
	async_mainloop(app)
