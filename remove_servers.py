#!/usr/bin/env python3
import sys
import copy

class prod_server():
	hostname = ''
	service = ''
	rack_id = ''
	rack_index = 0

	def __init__(self, hostname, service, rack_id, rack_index):
		self.hostname = hostname
		self.service = service
		self.rack_id = rack_id
		self.rack_index = rack_index

class prod_rack():
	rack_id = ''
	servers = []
	empties = None # num of empty servers
	to_remove = None # num to remove until empty

	def __init__(self, rack_id, servers, empties):
		self.rack_id = rack_id
		self.servers = copy.deepcopy(servers)
		self.empties = empties

def free_space(input_hosts, max_removes):
	racks = {}
	for host in input_hosts:
		hostname = host.split(' ')[0]
		service = host.split(' ')[1]
		rack_id = hostname.split('.')[0].split('-')[0]
		rack_index = hostname.split('.')[0].split('-')[1]
		if rack_id not in racks.keys():
			racks[rack_id] = []
		racks[rack_id].append(prod_server(hostname, service, rack_id, rack_index))
	
	valid_racks = []
	for rack in racks:
		# determine valid racks (only our team, and empty)
		valid = True
		current_empties = 0
		for server in racks[rack]:
			if (server.service != 'empty') and (server.service != 'timeline'):
				valid = False					
				break
			elif server.service == 'empty':
				current_empties += 1
		if valid:
			new_rack = prod_rack(rack, racks[rack], current_empties) # initialize new rack object
			new_rack.to_remove = len(new_rack.servers) - new_rack.empties # calculate num to remove
			valid_racks.append(new_rack)
	valid_racks.sort(key=lambda x: x.to_remove) # sort by to_remove
	remove_hosts = []
	num_removed = 0
	for rack in valid_racks:
		for server in rack.servers:
			if num_removed >= max_removes:
				break
			if server != 'empty':
				remove_hosts.append(server.hostname)
				num_removed += 1

	return(remove_hosts)


def main():
	max_removes = 5
	input_hosts = [
		'aaa-01.twttr.prod.net empty',
		'aaa-02.twttr.prod.net revenue',
		'aaa-03.twttr.prod.net empty',
		'aaa-04.twttr.prod.net revenue',
		'aab-01.twttr.prod.net timeline',
		'aab-02.twttr.prod.net empty',
		'aab-03.twttr.prod.net empty',
		'aab-04.twttr.prod.net empty',
		'aab-05.twttr.prod.net revenue',
		'aac-01.twttr.prod.net timeline',
		'aac-02.twttr.prod.net empty',
		'aac-03.twttr.prod.net empty',
		'aad-01.twttr.prod.net empty',
		'aad-02.twttr.prod.net revenue',
		'aad-03.twttr.prod.net empty',
		'aad-04.twttr.prod.net revenue',
		'aae-01.twttr.prod.net timeline',
		'aae-02.twttr.prod.net empty',
		'aae-03.twttr.prod.net empty',
		'aae-04.twttr.prod.net timeline',
		'aaf-01.twttr.prod.net empty',
		'aaf-02.twttr.prod.net empty',
		'aaf-03.twttr.prod.net timeline',
		'aag-01.twttr.prod.net empty',
		'aag-02.twttr.prod.net empty',
		'aag-03.twttr.prod.net timeline',
		'aag-04.twttr.prod.net timeline',
		'aag-05.twttr.prod.net timeline',
		'aag-06.twttr.prod.net timeline',
	]
	print(free_space(input_hosts, max_removes))

main()