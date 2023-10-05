# This program is for managing Minecraft mods.
import tkinter as tk
from dataclasses import dataclass

from async_tkinter_loop import async_mainloop

from src.footer import Footer
from src.header import Header
from src.results import Results


@dataclass
class Mod:
	def __init__(self,
				 name: str,
				 description: str,
				 author: str,
				 urls: list,
				 scope: list[bool, bool],
				 downloads: int,
				 id: int,
				 icon: str
				 ):
		"""
		A class for storing mod data.

		:param name: The name of the mod.
		:param description: The description of the mod.
		:param author: The author of the mod.
		:param urls: Any urls that the mod has.
		:param scope: Whether the mod is client-side or server-side. (client-side, server-side)
		:param downloads: how many downloads the mod has.
		:param id: The id of the mod.
		:param icon: The icon of the mod.
		"""
		self.name = name
		self.description = description
		self.author = author
		self.url = urls
		self.client_side = scope[0]
		self.server_side = scope[1]
		self.downloads = downloads
		self.id = id
		self.icon = icon


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Minecraft Mod Manager")
		self.geometry("700x400")
		self.resizable(False, False)

		self.header = Header(self)
		self.results = Results(self)
		self.footer = Footer(self)


if __name__ == "__main__":
	app = App()
	async_mainloop(app)
