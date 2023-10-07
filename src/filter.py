import tkinter as tk

import customtkinter as ctk

minecraft_versions = [
	"1.20.2",
	"1.20.1",
	"1.20.0",
	"1.19.4",
	"1.19.3",
	"1.19.2",
	"1.19.1",
	"1.19",
	"1.18.2",
	"1.18.1",
	"1.18",
	"1.17.1",
	"1.17",
	"1.16.5",
	"1.16.4",
	"1.16.3",
	"1.16.2",
	"1.16.1",
	"1.16",
	"1.15.2",
	"1.15.1",
	"1.15",
	"1.14.4",
	"1.14.3",
	"1.14.2",
	"1.14.1",
	"1.14",
	"1.13.2",
	"1.13.1",
	"1.13",
	"1.12.2",
	"1.12.1",
	"1.12",
	"1.11.2",
	"1.11.1",
	"1.11",
	"1.10.2",
	"1.10.1",
	"1.10",
	"1.9.4",
	"1.9.3",
	"1.9.2",
	"1.9.1",
	"1.9",
	"1.8.9",
	"1.7.10"
]


class FilterBar(ctk.CTkFrame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, corner_radius=0, **kwargs)
		self.pack()

		self.wrapper = ctk.CTkCanvas(self, highlightthickness=0)
		self.wrapper.pack(fill=tk.BOTH, expand=True)

		self.frame = ctk.CTkFrame(self.wrapper, corner_radius=0)
		self.wrapper.create_window((0, 0), window=self.frame, anchor="w")

		self.wrapper.bind_all("<MouseWheel>", self.on_mousewheel)
		bbox = self.wrapper.bbox('all')
		self.wrapper.configure(width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])

		category_options = {
			"categories":       ctk.CTkLabel(self.frame, text="Categories", font=("Arial", 15)),
			"adventure":        ctk.CTkCheckBox(self.frame, text="Adventure", font=("Arial", 15)),
			"cursed":           ctk.CTkCheckBox(self.frame, text="Cursed", font=("Arial", 15)),
			"decoration":       ctk.CTkCheckBox(self.frame, text="Decoration", font=("Arial", 15)),
			"economy":          ctk.CTkCheckBox(self.frame, text="Economy", font=("Arial", 15)),
			"equipment":        ctk.CTkCheckBox(self.frame, text="Equipment", font=("Arial", 15)),
			"food":             ctk.CTkCheckBox(self.frame, text="Food", font=("Arial", 15)),
			"game mechanics":   ctk.CTkCheckBox(self.frame, text="Game Mechanics", font=("Arial", 15)),
			"library":          ctk.CTkCheckBox(self.frame, text="Library", font=("Arial", 15)),
			"magic":            ctk.CTkCheckBox(self.frame, text="Magic", font=("Arial", 15)),
			"management":       ctk.CTkCheckBox(self.frame, text="Management", font=("Arial", 15)),
			"minigame":         ctk.CTkCheckBox(self.frame, text="Minigame", font=("Arial", 15)),
			"mobs":             ctk.CTkCheckBox(self.frame, text="Mobs", font=("Arial", 15)),
			"optimization":     ctk.CTkCheckBox(self.frame, text="Optimization", font=("Arial", 15)),
			"social":           ctk.CTkCheckBox(self.frame, text="Social", font=("Arial", 15)),
			"storage":          ctk.CTkCheckBox(self.frame, text="Storage", font=("Arial", 15)),
			"technology":       ctk.CTkCheckBox(self.frame, text="Technology", font=("Arial", 15)),
			"transportation":   ctk.CTkCheckBox(self.frame, text="Transportation", font=("Arial", 15)),
			"utility":          ctk.CTkCheckBox(self.frame, text="Utility", font=("Arial", 15)),
			"world generation": ctk.CTkCheckBox(self.frame, text="World Generation", font=("Arial", 15)),
		}
		for category in category_options:
			category_options[category].pack(fill=tk.X, padx=15, pady=5)
		category_options["categories"].pack(fill=tk.X, pady=(15, 0))

		loader_options = {
			"loaders":              ctk.CTkLabel(self.frame, text="Loaders", font=("Arial", 15)),
			"fabric":               ctk.CTkCheckBox(self.frame, text="Fabric", font=("Arial", 15)),
			"forge":                ctk.CTkCheckBox(self.frame, text="Forge", font=("Arial", 15)),
			"liteLoader":           ctk.CTkCheckBox(self.frame, text="LiteLoader", font=("Arial", 15)),
			"risugami's modLoader": ctk.CTkCheckBox(self.frame, text="Risugami's ModLoader", font=("Arial", 15)),
			"neoForge":             ctk.CTkCheckBox(self.frame, text="NeoForge", font=("Arial", 15)),
			"quilt":                ctk.CTkCheckBox(self.frame, text="Quilt", font=("Arial", 15)),
			"rift":                 ctk.CTkCheckBox(self.frame, text="Rift", font=("Arial", 15))
		}
		for loader in loader_options:
			loader_options[loader].pack(fill=tk.X, padx=15, pady=5)
		loader_options["loaders"].pack(fill=tk.X, pady=(20, 0))

		enviroment_options = {
			"environments": ctk.CTkLabel(self.frame, text="Environments", font=("Arial", 15)),
			"client":       ctk.CTkCheckBox(self.frame, text="Client", font=("Arial", 15)),
			"server":       ctk.CTkCheckBox(self.frame, text="Server", font=("Arial", 15))
		}
		for enviroment in enviroment_options:
			enviroment_options[enviroment].pack(fill=tk.X, padx=15, pady=5)
		enviroment_options["environments"].pack(fill=tk.X, pady=(20, 0))

		version_options = {
			"versions":          ctk.CTkLabel(self.frame, text="Versions", font=("Arial", 15)),
			"show all versions": ctk.CTkCheckBox(self.frame, text="Show All Versions", font=("Arial", 15)),
		}
		for version in version_options:
			version_options[version].pack(fill=tk.X, padx=15, pady=5)
		version_options["versions"].pack(fill=tk.X, pady=(20, 0))

		versions_dropdown = ctk.CTkOptionMenu(self.frame, values=minecraft_versions, font=("Arial", 15))
		versions_dropdown.pack(fill=tk.X, padx=5, pady=5)

	def on_mousewheel(self, event):
		self.wrapper.yview_scroll(int(-1 * (event.delta / 120)), "units")
		self.wrapper.configure(scrollregion=self.wrapper.bbox("all"))
