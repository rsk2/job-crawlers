import re
import requests
from alladin.core.log import Log
from alladin.jobspider.crawl import Data, XmlParser, BaseParser
from xml.dom.minidom import parseString
from xml.etree.ElementTree import ElementTree


def read(self, url, tenantid, num_jobs=None):
    '''
    This function crawls and creates a dictionary of jobs from any xml job feed

    Args:
        num_jobs: Number of jobs you want to parse

    Returns:
        A dictionary of all the jobs with the job id as the key
    '''
    response = requests.get(url, verify=False)
    tree = ElementTree()
    root = tree.parse("assets.xml")

    items = [item for item in parser.get_elements(parser.dom, 'entry')]
    if (num_jobs is not None):
        items = items[0:num_jobs]
    for item_e in items:
        job = {}
        job['ExternalId'] = parser.get_element_text(parser.get_first_element(item_e, 'id'))
        job['JobTitle'] = parser.get_element_text(parser.get_first_element(item_e, 'title'))
        job['IsNew'] = False
        if (job['ExternalId'] not in data.JOBS):
            Log('Extracting job: ['+ str(job['JobTitle']) +", "+ str(job.get('ExternalId', '')) + ']')
            job['tenant_id'] = tenantid
            job['ExternalOrganization'] = ''
            job['JobDescription'] = parser.get_element_text(parser.get_first_element(item_e, 'content'))
            for category_e in parser.get_elements(item_e, 'category'):
                scheme = parser.get_attribute(category_e, 'scheme')
                if (re.search('location', scheme)):
                    job['Location'] = parser.get_attribute(category_e, 'term')
                if (re.search('job_type', scheme)):
                    job_type_parsed = parser.get_attribute(category_e, 'term')
            links_e = parser.get_elements(item_e, 'link')
            link_e = next(iter(links_e))
            job['ExternalUrl'] = parser.get_attribute(link_e, 'href')
            link_e = next(iter(links_e))
    return jobs
