import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
	result = requests.get(url)
	soup = BeautifulSoup(result.text, 'html.parser')
	pages = soup.find('div', {'class': 's-pagination'})
	if pages:
		pages = pages.find_all('a')
	else:
		return -1
	last_pages = pages[-2].get_text(strip = True)
	return int(last_pages)

def extract_job(html):
	title = html.find('a', {'class': 's-link'})['title']
	company, location = html.find('h3', {'class': 'fs-body1'}).find_all('span', recursive = False)
	job_id = html['data-jobid']
	return {'title': title, 'company': company.get_text(strip=True), 'location': location.get_text(strip=True), 'apply_link': f'https://stackoverflow.com/jobs/{job_id}'}

def extract_jobs(last_page, url):
	jobs = []
	for page in range(1, last_page+1):
		print(f'Scrapping SO: Page {page}')
		result = requests.get(f'{url}&pg={page}')
		soup = BeautifulSoup(result.text, 'html.parser')
		results = soup.find_all('div', {'class': '-job'})
		for page in results:
			job = extract_job(page)
			jobs.append(job)
	return jobs

def get_jobs(word):
	url = f'https://stackoverflow.com/jobs?q={word}'
	last_page = get_last_page(url)
	if last_page == -1:
		return [{'title': 'Not found', 'company': 'Not found', 'location': 'Not found', 'link': '/'}]
	jobs = extract_jobs(last_page, url)
	return jobs