import tkinter as tk

import customtkinter as ctk

from src.footer import Footer
from src.header import Header
from src.search import Project


class Results(ctk.CTkFrame):
	def __init__(self, master: any, **kwargs):
		super().__init__(master, **kwargs, corner_radius=0)
		self.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

		self.header = Header(self)

		self.wrapper = ctk.CTkCanvas(self, highlightthickness=0)
		self.wrapper.pack(fill='both', expand=True)

		self.wrapper.bind("<Configure>", lambda _: self.manage_what_projects_are_displayed())

		self.projects_frame = ctk.CTkFrame(self.wrapper, corner_radius=0)
		self.wrapper.create_window((0, 0), window=self.projects_frame, anchor="nw")
		self.projects_frame.bind("<MouseWheel>", self.on_mousewheel)
		self.wrapper.bind("<MouseWheel>", self.on_mousewheel)

		self.scrollbar = ctk.CTkScrollbar(self.wrapper, command=self.wrapper.yview, fg_color="#2f3136")
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.wrapper.configure(yscrollcommand=self.scrollbar.set)

		self.footer = Footer(self)
		self.projects = []

		self.wrapper.configure(scrollregion=self.wrapper.bbox("all"))

		self.wrapper.update_idletasks()

		self.project_width = 250
		self.project_height = 200

	def display_projects(self, projects):
		# Clear the existing projects
		self.projects.clear()
		for project in projects:
			project_frame = ProjectFrame(self.projects_frame, project, corner_radius=15, fg_color="#2f3136",
										 width=self.project_width,
										 height=self.project_height)
			self.projects.append(project_frame)

		self.manage_what_projects_are_displayed()

	def manage_what_projects_are_displayed(self):
		self.wrapper.update_idletasks()
		self.wrapper.configure(scrollregion=self.wrapper.bbox("all"))

		# Calculate the number of columns based on the width of the projects_frame
		projects_per_row = max(1,
							   self.projects_frame.winfo_width() // self.project_width)  # Assuming each project is 200 pixels wide

		# Place the projects in the grid
		for i, project in enumerate(self.projects):
			project.grid(row=i // projects_per_row, column=i % projects_per_row, padx=10, pady=10)
			project.update_idletasks()
			for child in project.winfo_children():
				if not isinstance(child, ctk.CTkTextbox):
					child.bind("<MouseWheel>", self.on_mousewheel)
			project.bind("<MouseWheel>", self.on_mousewheel)
		self.wrapper.create_window((0, 0), window=self.projects_frame, anchor="nw",
								   width=self.wrapper.winfo_width())

	def on_mousewheel(self, event):
		self.wrapper.yview_scroll(int(-1 * (event.delta / 120)), "units")
		self.wrapper.configure(scrollregion=self.wrapper.bbox("all"))


class ProjectFrame(ctk.CTkFrame):
	def __init__(self, master: any, project: Project, **kwargs):
		super().__init__(master, **kwargs)
		self.project = project
		self.pack_propagate(False)

		self.title = ctk.CTkLabel(self, corner_radius=15, font=("Arial", 20), text=project.title)
		self.title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

		self.description = ctk.CTkTextbox(self, corner_radius=15, font=("Arial", 12), width=200, height=100)
		self.description.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		self.description.insert(tk.END, project.description)
		self.description.configure(state='disabled')

		self.download_button = ctk.CTkButton(self, text="Download", corner_radius=15, font=("Arial", 10),
											 command=lambda: print(f"Downloading: {project.title}"), width=10)
		self.download_button.place(relx=0.9, rely=0.9, anchor=tk.E)

		self.view_button = ctk.CTkButton(self, text="View", corner_radius=15, font=("Arial", 10),
										 command=lambda: print(f"Viewing: {project.title}"), width=10)
		self.view_button.place(relx=0.35, rely=0.9, anchor=tk.W)
