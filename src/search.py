import json
from dataclasses import dataclass

import aiohttp


async def fetch(session, url, **kwargs):
	async with session.get(url, **kwargs) as response:
		data = await response.text()
		return json.loads(data)


async def modrinth_search(query: str = None, index: str = "relevance", limit: int = 10, offset: int = 0):
	query = json.dumps(query)
	limit = json.dumps(limit)
	offset = json.dumps(offset)

	projects_found = []
	async with aiohttp.ClientSession() as session:
		response = await fetch(
			session,
			'https://api.modrinth.com/v2/search',
			params={
				'query':  query,
				'index':  index.lower(),
				'limit':  limit,
				'offset': offset
			})

		for project in response['hits']:
			projects_found.append(project['project_id'])

	return await get_projects(projects_found)


@dataclass
class Project:
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

	def __repr__(self):
		return self.title


async def get_projects(project_ids: list[int, ...]):
	projects = {}
	async with aiohttp.ClientSession() as session:
		response = await fetch(
			session,
			'https://api.modrinth.com/v2/projects',
			params={'ids': json.dumps(project_ids)}
		)

		for project in response:
			if 'body' in project:
				del project['body']
			projects[project['id']] = Project(**project)

	return projects
