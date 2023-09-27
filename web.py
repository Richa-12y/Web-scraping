
from bs4 import BeautifulSoup
import requests
import time

print('Put some skill that you are not familer with')
unfamiliar_skill=input('>')
print(f'Filtering out:{unfamiliar_skill}')


def find_jobs():
    url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation="
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    jobs=soup.find_all('li',class_='clearfix job-bx wht-shd-bx')

    for index,job in enumerate(jobs):
        published_date=job.find('span',class_='sim-posted').span.text
        if 'few' in published_date:
            compony_name=job.find('h3',class_='joblist-comp-name').text.replace(' ','')
            skills=job.find('span',class_='srp-skills').text.replace(' ','')
            more_info=job.header.h2.a['href']
            if unfamiliar_skill not in skills:
                with open(f'post/{index}.txt','w') as f:
                    f.write(f"Company Name:{compony_name.strip()} \n")
                    f.write(f"KeySkills:{skills.strip()} \n")
                    f.write(f"MoreInfo:{more_info}")

                print(f'File Save:{index}')
                    # print(f"Company Name:{compony_name.strip()}")
                    # print(f"KeySkills:{skills.strip()}")
                    # print(f"MoreInfo:{more_info}")
                    
                    # print('')

if __name__=='__main__':
    while True:
        find_jobs()
        time_wait=10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)