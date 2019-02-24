import requests
import xml.etree.ElementTree as ET

def read(url='https://jobs.marketinghire.com/jobs/?&ss=1&display=rss', num_jobs=None):
    '''
    This function crawls and creates a dictionary of jobs from a xml job feed
    As an example we parse jobs from marketinghire.com

    Args:
        num_jobs: Number of jobs you want to parse

    Returns:
        A dictionary of all the jobs with the job id as the key
    '''
    response = requests.get(url, verify=False)
    root = ET.fromstring(response.text)
    print(root.tag, root.attrib)
    items = [item for item in root[0].findall('item')]
    jobs = {}
    for item in items:
        job = {}
        job['Link'] = item.find('link').text
        job['Title'] = item.find('title').text
        job['Id'] = item.find('guid').text
        job['JobDescription'] = item.find('description').text
        job['Date'] = item.find('pubDate').text
        print(job['JobDescription'], job['Date'])
        jobs[job.get('Id','')] = job
    return jobs

if __name__ =="__main__":
    read()
