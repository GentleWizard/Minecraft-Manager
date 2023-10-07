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

		self.wrapper = ctk.CTkCanvas(self)
		self.wrapper.pack(fill=tk.BOTH, expand=True)

		self.frame = ctk.CTkFrame(self.wrapper, corner_radius=0)
		self.wrapper.create_window((0, 0), window=self.frame, anchor="nw")

		self.scrollbar = ctk.CTkScrollbar(self.frame, command=self.wrapper.yview)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.wrapper.bind("<Configure>", lambda e: self.wrapper.configure(scrollregion=self.wrapper.bbox("all")))
		self.wrapper.configure(yscrollcommand=self.scrollbar.set)

		self.wrapper.bind_all("<MouseWheel>", self.on_mousewheel)
		bbox = self.wrapper.bbox('all')
		self.wrapper.configure(width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])

		category_options = {
			"Categories":       ctk.CTkLabel(self.frame, text="Categories", font=("Arial", 15)),
			"Adventure":        ctk.CTkCheckBox(self.frame, text="Adventure", font=("Arial", 15)),
			"Cursed":           ctk.CTkCheckBox(self.frame, text="Cursed", font=("Arial", 15)),
			"Decoration":       ctk.CTkCheckBox(self.frame, text="Decoration", font=("Arial", 15)),
			"Economy":          ctk.CTkCheckBox(self.frame, text="Economy", font=("Arial", 15)),
			"Equipment":        ctk.CTkCheckBox(self.frame, text="Equipment", font=("Arial", 15)),
			"Food":             ctk.CTkCheckBox(self.frame, text="Food", font=("Arial", 15)),
			"Game Mechanics":   ctk.CTkCheckBox(self.frame, text="Game Mechanics", font=("Arial", 15)),
			"Library":          ctk.CTkCheckBox(self.frame, text="Library", font=("Arial", 15)),
			"Magic":            ctk.CTkCheckBox(self.frame, text="Magic", font=("Arial", 15)),
			"Management":       ctk.CTkCheckBox(self.frame, text="Management", font=("Arial", 15)),
			"Minigame":         ctk.CTkCheckBox(self.frame, text="Minigame", font=("Arial", 15)),
			"Mobs":             ctk.CTkCheckBox(self.frame, text="Mobs", font=("Arial", 15)),
			"Optimization":     ctk.CTkCheckBox(self.frame, text="Optimization", font=("Arial", 15)),
			"Social":           ctk.CTkCheckBox(self.frame, text="Social", font=("Arial", 15)),
			"Storage":          ctk.CTkCheckBox(self.frame, text="Storage", font=("Arial", 15)),
			"Technology":       ctk.CTkCheckBox(self.frame, text="Technology", font=("Arial", 15)),
			"Transportation":   ctk.CTkCheckBox(self.frame, text="Transportation", font=("Arial", 15)),
			"Utility":          ctk.CTkCheckBox(self.frame, text="Utility", font=("Arial", 15)),
			"World Generation": ctk.CTkCheckBox(self.frame, text="World Generation", font=("Arial", 15)),
		}
		for category in category_options:
			category_options[category].pack(fill=tk.X, padx=5, pady=5)

		loader_options = {
			"Loaders":              ctk.CTkLabel(self.frame, text="Loaders", font=("Arial", 15)),
			"Fabric":               ctk.CTkCheckBox(self.frame, text="Fabric", font=("Arial", 15)),
			"Forge":                ctk.CTkCheckBox(self.frame, text="Forge", font=("Arial", 15)),
			"LiteLoader":           ctk.CTkCheckBox(self.frame, text="LiteLoader", font=("Arial", 15)),
			"Risugami's ModLoader": ctk.CTkCheckBox(self.frame, text="Risugami's ModLoader", font=("Arial", 15)),
			"NeoForge":             ctk.CTkCheckBox(self.frame, text="NeoForge", font=("Arial", 15)),
			"Quilt":                ctk.CTkCheckBox(self.frame, text="Quilt", font=("Arial", 15)),
			"Rift":                 ctk.CTkCheckBox(self.frame, text="Rift", font=("Arial", 15))
		}
		for loader in loader_options:
			loader_options[loader].pack(fill=tk.X, padx=5, pady=5)

		enviroment_options = {
			"Enviroments": ctk.CTkLabel(self.frame, text="Enviroments", font=("Arial", 15)),
			"Client":      ctk.CTkCheckBox(self.frame, text="Client", font=("Arial", 15)),
			"Server":      ctk.CTkCheckBox(self.frame, text="Server", font=("Arial", 15))
		}
		for enviroment in enviroment_options:
			enviroment_options[enviroment].pack(fill=tk.X, padx=5, pady=5)

		version_options = {
			"Versions":          ctk.CTkLabel(self.frame, text="Versions", font=("Arial", 15)),
			"Show All Versions": ctk.CTkCheckBox(self.frame, text="Show All Versions", font=("Arial", 15)),
		}
		for version in version_options:
			version_options[version].pack(fill=tk.X, padx=5, pady=5)

		versions_dropdown = ctk.CTkOptionMenu(self.frame, values=minecraft_versions, font=("Arial", 15))
		versions_dropdown.pack(fill=tk.X, padx=5, pady=5)

	def on_mousewheel(self, event):
		self.wrapper.yview_scroll(int(-1 * (event.delta / 120)), "units")
		self.wrapper.configure(scrollregion=self.wrapper.bbox("all"))
