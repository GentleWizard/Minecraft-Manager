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

		self.wrapper = ctk.CTkFrame(self, corner_radius=0)
		self.wrapper.pack(fill=tk.BOTH, expand=True)
		self.wrapper.pack_propagate(False)

		self.projects_frame = ctk.CTkFrame(self.wrapper, corner_radius=0)
		self.projects_frame.pack(fill=tk.BOTH, expand=True)

		self.footer = Footer(self)
		self.projects = []

	def display_projects(self, projects):
		for project in projects:
			self.projects.append(project)
			project_frame = ProjectFrame(self.projects_frame, project, fg_color="red")
			project_frame.grid(sticky="nwse", padx=5, pady=5, ipadx=5, ipady=5)


class ProjectFrame(ctk.CTkFrame):
	def __init__(self, master: any, project: Project, **kwargs):
		super().__init__(master, **kwargs)
		self.grid(sticky="nwse", padx=5, pady=5)
