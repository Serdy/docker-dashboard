from docker import Client

def docker_name_up(*args):
	docker_urls = ['10.134.2.1', '10.134.3.1', '10.134.130.1', '10.134.131.1', '10.134.132.1']
	# docker_urls = ['10.134.200.1']
	docker_name = []
	for docker_url in docker_urls:
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

	

