import csv

def save_to_file(jobs):
	fp = open('jobs.csv', 'w')
	writer = csv.writer(fp)
	writer.writerow(['Title', 'Company', 'Location', 'Link'])
	print('Starting Writing to CSV')
	for job in jobs:
		writer.writerow(list(job.values()))
	print('Finished Writing to CSV')