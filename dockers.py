from docker import Client

def docker_urls():
	with open('cluster') as f:
		docker_urls = []
		for x in f.readlines():
			if x[-1:] == "\n":
				docker_urls.append(x[:-1])
			else:
				docker_urls.append(x)
		return docker_urls
			

def docker_name_up(*args):
	docker_name = []
	for docker_url in docker_urls():
		cli = Client(base_url='tcp://' + docker_url + ':2375')
		for x in cli.containers(all=True):
			id = (x['Id'][:12])
			status =  (x['Status'])
			name = (x['Names'][0][1:])
			ip = (x['NetworkSettings']['Networks']['bridge']['IPAddress'])
			dockers = { 'Id': id, 'Status': status, 'Name': name, 'ip': ip, 'Docker_host_ip': docker_url }
			docker_name.append(dockers)
	return docker_name


def search_docker(docker_name_up, search):
	docker_name = []
	for resuts_search in (x for x in docker_name_up if search in x['Name']):
		docker_name.append(resuts_search)
	return docker_name

# print(docker_urls())	
# print(docker_name_up())
