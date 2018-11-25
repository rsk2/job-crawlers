import requests
from bs4 import BeautifulSoup
import json
import urllib

def read( num_jobs=None):
    '''
    This function crawls and creates a dictionary of jobs from Caesars Entertainment company
    You can view the jobs on their careers page: https://caesars.taleo.net/careersection/czr_ext_cs/jobsearch.ftl?lang=en&portal=8100120159

    Args:
        num_jobs: Number of jobs you want to parse

    Returns:
        A dictionary of all the jobs with the job id as the key
    '''
    url = "https://caesars.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=8100120159"
    print('reading from url [' + str(url) + ']')
    job_desc_url = 'https://caesars.taleo.net/careersection/czr_ext_cs/jobdetail.ftl'
    jobs = {}
    page_number = 1
    count = 0
    while(True):
        payload = {
                   "multilineEnabled":True,
                   "sortingSelection":{
                        "sortBySelectionParam":"3",
                        "ascendingSortingOrder":"false"
                    },
                   "fieldData":{
                        "fields":{
                            "LOCATION":"",
                            "CATEGORY":""
                                },
                        "valid":True
                    },
                    "filterSelectionParam":{
                        "searchFilterSelections":[
                            {
                                "id":"LOCATION",
                                "selectedValues":[]
                            },
                            {
                                "id":"JOB_FIELD",
                                "selectedValues":[]
                            }
                            ]
                    },
                    "advancedSearchFiltersSelectionParam":{
                        "searchFilterSelections":[
                            {
                                "id":"KEYWORD",
                                "selectedValues":[]
                            },
                            {
                                "id":"JOB_FIELD",
                                "selectedValues":[]
                            },
                            {
                                "id":"LOCATION",
                                "selectedValues":[]
                            },
                            {
                                "id":"EMPLOYEE_STATUS",
                                "selectedValues":[]
                            },
                            {
                                "id":"JOB_LEVEL",
                                "selectedValues":[]
                            },
                            {
                                "id":"JOB_SCHEDULE",
                                "selectedValues":[]
                            },
                            {
                                "id":"JOB_TYPE",
                                "selectedValues":[]
                            },
                            {
                                "id":"WILL_TRAVEL",
                                "selectedValues":[]
                            },
                            {
                                "id":"POSTING_DATE",
                                "selectedValues":[]
                            }
                        ]
                    },
                    "pageNo":page_number
                }
        response = requests.post(url, data=json.dumps(payload), headers={"Content-Type":"application/json", "tz" : "GMT-5:30"})
        json_data = response.json()
        total_count = json_data["pagingData"]["totalCount"]
        if (response.status_code == 200):
            if len(json_data["requisitionList"]) > 0:
                for item in json_data["requisitionList"]:
                    job = {}
                    job['ExternalOrganization'] = 'Caesars Entertainment'
                    job['JobTitle'] = item["column"][0]
                    print(job['JobTitle'])
                    job['ExternalId'] = item["column"][1]
                    print(job['ExternalId'])
                    job['ExternalUrl'] = job_desc_url + "?job=" + job['ExternalId']
                    job['Location'] = item["column"][2].replace("[","").replace("]","").replace("\"","")
                    print(job['Location'])
                    count += 1
                    desc_response = requests.get(job['ExternalUrl'], verify=False)
                    page_soup = BeautifulSoup(desc_response.text, "html.parser")
                    desc_tag = page_soup.find("input", {"id":"initialHistory"})
                    if desc_tag is not None:
                        desc_value = desc_tag['value']
                        words = desc_value.split("|")
                        desc = "<strong>Description</strong><br/><br/>"
                        #removing unnecessary characters and appending to the description
                        desc += urllib.parse.unquote(words[17]).replace("!!*!","").replace("!!!*!","").replace("\\","")[:-1]
                        desc += "<br/><strong>Qualifications</strong><br/>"
                        desc += urllib.parse.unquote(words[19]).replace("*","").replace("!","")
                        desc += "<br/><strong>Primary Location: </strong>"
                        desc += urllib.parse.unquote(words[21]).replace("!","")
                        desc += "<br/><strong>Employee Status: </strong>"
                        desc += urllib.parse.unquote(words[23]).replace("!","")
                        job['JobDescription'] = desc
                    else:
                        job['JobDescription'] = "<strong>This job is no longer available or doesn't have a description. Please confirm by viewing the job on the website</strong><br/>"
                    #add the new job to the jobs dictionary
                    jobs[job.get('ExternalId', '')] = job
                if num_jobs is not None and count >= num_jobs:
                    break
                else:
                    page_number += 1
            else:
                #no jobs found and hence stop the loop
                break
            if count >= total_count:
                #this means we have parsed all jobs and hence stop the loop
                break
    return jobs

if __name__ == "__main__":
        read()
