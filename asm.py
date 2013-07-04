#!/bin/python

import urllib2, json, base64, datetime, dateutil.parser

class Task:
	def __init__(self, **entries): 
		self.__dict__.update(entries)

	def __str__(self):
		self.url = "https://app.asana.com/0/%s/%s" % (task.user_id, task.id)
		return u"%s : %s" % (self.url, self.name)

def get_tasks(user_id, workspace):
	authorization = "%s:" % api_key
	request_headers = dict()
	request_headers["Authorization"] = "Basic %s" % base64.b64encode(authorization)
	opener = urllib2.build_opener()
	opener.addheaders = request_headers.items()
	query_url = "https://app.asana.com/api/1.0/tasks?workspace=%s&assignee=%s&opt_fields=id,name,completed,projects,completed_at,tags,assignee_status" % (workspace, user_id)
	data = opener.open(query_url)
	data = data.read()
	full_tasks_list = json.loads(data)['data']
	return full_tasks_list

config = json.loads( open("config.json").read() )
users = json.loads( open("users_list.json").read() )

workspace = config['workspace']
in_progress_tag_id = config['in_progress_tag_id']
api_key = config['api_key']

for user in users:

	filtered_tasks = {'yesterday': list(), 'on_it': list()}

	for task_dict in get_tasks(user['id'], workspace):

		task = Task(**task_dict)
		task.user_id = user['id']

		if task.completed_at:
			completed_at = dateutil.parser.parse(task.completed_at).replace(hour=0, minute=0, second=0, microsecond=0)
			now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=completed_at.tzinfo)
			yesterday = now - datetime.timedelta(days=1)
			if task.completed and completed_at == yesterday:
				filtered_tasks['yesterday'].append(task)

		if not task.completed:
			added = False

			if task.tags:
				for tag in task.tags:
					if tag['id'] == in_progress_tag_id:
						filtered_tasks['on_it'].append(task)
						added = True
						break

			if not added and task.assignee_status == 'today':
				filtered_tasks['on_it'].append(task)
				added = True

	print u"%s's tasks:" % (user['name'])
	print u"Tasks you've completed yesterday:"
	for task in filtered_tasks['yesterday']:
		print task
	print u""
	print u"Tasks you are doing:"
	for task in filtered_tasks['on_it']:
		print task
	print u""
	print u"---"
	print u""
