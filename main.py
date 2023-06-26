from jira import JIRA
import os
import pandas as pd
import csv
KEY_LIST=[]
HEADER_LIST = ['#OF_RECORDS','KEY','STATUS']
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")
EDG_PMO_PROJECTS_NAME = 'EDG PMO Projects'
EDG_PMO_PROJECTS_ID = '16901'
EDG_QA_PROJECTS_NAME = 'EDG - QA Projects'
EDG_QA_PROJECTS_ID = '22400'
EDG_QA_TCS = 'EDG - QA Transaction TCS'
EDG_QA_TCS_ID = '21900'
EDG_QA_CTS_NAME = 'EDG - Transactions QA CTS'
EDG_QA_CTS_ID = '21300'
OPEN_STATUS_ID = '11'
CLOSED_STATUS_ID = '61'
def start_connection():
    '''Jira Server Connection'''
    jiraOptions = {'server': "https://jira-corelogic.valiantys.net"}
    jira = JIRA(options=jiraOptions, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
    return jira

def get_edg_project_list(jira:JIRA):
    projects = jira.projects()
    project_list = []
    for project in projects:
        project_dict = {}
        if 'EDG' in project.name:
            project_dict["name"] = project.name
            project_dict["id"] = project.id
            project_list.append(project_dict)


def get_transition_name_list(jira:JIRA, issue):
    transitions = jira.transitions(issue)
    transition_list = [t['name'] for t in transitions]
    return transition_list

def get_transition_id_by_name(jira: JIRA, issue, name: str):
    transitions = jira.transitions(issue)
    transition_list = [(t['id'], t['name']) for t in transitions]
    print(transition_list)
    transition_list_iterator = filter(lambda x: (x[1] == name), transition_list)
    filtered_transition_list = list(transition_list_iterator)
    print(filtered_transition_list)
    return filtered_transition_list[0][0]




def create_single_issue(jira:JIRA,project_id,summary,description,issuetype):
    jira.create_issue(project=project_id,summary = summary,description=description,issuetype=issuetype)


def create_bulk_issues(jira:JIRA,issue_value_list):
    new_issues = jira.create_issues(field_list=issue_value_list)
    global KEY_LIST
    num_of_errors=0
    for issue in new_issues:
        if issue['status'] == 'Success':
            KEY_LIST.append(issue['issue'].key)
        else:
            num_of_errors +=1
    print(f"Number of errors while creating the jira issues are:{num_of_errors} ")
    print(KEY_LIST)
    return KEY_LIST

def set_issue_statuses_by_name(jira:JIRA,keys_list,name):
    for key in keys_list:
        iss = jira.issue(key)
        if name.lower() == 'open':
            jira.transition_issue(iss,transition='OPEN')
        elif name.lower() == 'closed':
            jira.transition_issue(iss,transition='Closed')

def read_exc_and_return_status_list(file_name,sheet_name):
    df_sheet_name = pd.read_excel(str(file_name), sheet_name=str(sheet_name))
    status_list = df_sheet_name.get(key='Status').values.tolist()
    return status_list

def create_status_csv(header_list,key_list,status_list):
    len_list = int(len(key_list))
    num_list = []
    for i in range(len_list):
        num_list.append(i + 1)

    zipped_list = list(zip(num_list, key_list, status_list))
    with open('out2.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(header_list)
        write.writerows(zipped_list)


def read_csv_to_update_stat(jira:JIRA,filename):
    with open(filename, "r") as my_file:
        # pass the file object to reader()
        file_reader = csv.reader(my_file)
        # do this for all the rows
        for i in file_reader:
            if i == [] or i == ['#OF_RECORDS', 'KEY', 'STATUS']:
                continue
            iss = jira.issue(str(i[1]))
            if i[2].lower() == 'open':
                jira.transition_issue(iss,transition='OPEN')
            elif i[2].lower() == 'closed':
                jira.transition_issue(iss, transition='Closed')
#Example Issue List
QA_Regular_Format1_3072 = [
{
    'project': {'id': '21300'},
    'summary': 'TestSinan',#summary
    'description': 'This is a test one',
    'issuetype': {'name': 'Defect'},
    'customfield_24512': {'value': '33_Lot (length is actually 5 bytes with byte 345 as filler)'}, #3072
    'customfield_29815' : '9999999', #RecordID
    'customfield_24502' : {'value': 'Transaction QA'},#Project
    'customfield_24513' : {'value': 'Cognizant'},#Vendor
    'customfield_18909' : {'value': 'WI'}, #State
    'customfield_25100' : {'value':'MILWAUKEE'},#County
    'customfield_24519' : '99999',#Doc Number
    'customfield_26900' : '123',#Recording Book
    'customfield_27309' : '456',#Recording Page
    'customfield_24526' : '2023-06-01',#Recording Date,watch out for the format
    'customfield_26002' : '2023',#DocYear
    'customfield_24501' : {'value': 'T'},#DeedCategory
    'customfield_24511' : {'value': 'MG'},#DAMAR
    #'customfield_24508' : {'value' : ''},#ADC
    'customfield_24505' : {'value': 'Keying error'},#TypeofError
    'customfield_24517' : {'name': 'aalaguvairamani@corelogic.com'},#DetectedBy
    'customfield_24529' : '2023-06-13',#DetectedDate
    'customfield_14991' : {'value': 'Severity 2'},#Severity
    'customfield_24504' : {'value': 'Missed defect'},#Target Cycle/ Values might be out of dropdown. Use f string for all
    'customfield_24528' : '01/01 to 01/08',#Sample Data
    'customfield_24506' : {'value': 'Critical'},#Critical
    'customfield_24515' : '2022-12-28'#Batch Date but pay attention to the format in excel
},

{
    'project': {'id': '21300'},
    'summary': 'TestSinan',#summary
    'description': 'This is a test one',
    'issuetype': {'name': 'Defect'},
    'customfield_24512': {'value': '33_Lot (length is actually 5 bytes with byte 345 as filler)'}, #3072
    'customfield_29815' : '9999999', #RecordID
    'customfield_24502' : {'value': 'Transaction QA'},#Project
    'customfield_24513' : {'value': 'Cognizant'},#Vendor
    'customfield_18909' : {'value': 'WI'}, #State
    'customfield_25100' : {'value':'MILWAUKEE'},#County
    'customfield_24519' : '99999',#Doc Number
    'customfield_26900' : '123',#Recording Book
    'customfield_27309' : '456',#Recording Page
    'customfield_24526' : '2023-06-01',#Recording Date,watch out for the format
    'customfield_26002' : '2023',#DocYear
    'customfield_24501' : {'value': 'T'},#DeedCategory
    'customfield_24511' : {'value': 'MG'},#DAMAR
    #'customfield_24508' : {'value' : ''},#ADC
    'customfield_24505' : {'value': 'Keying error'},#TypeofError
    'customfield_24517' : {'name': 'aalaguvairamani@corelogic.com'},#DetectedBy
    'customfield_24529' : '2023-06-13',#DetectedDate
    'customfield_14991' : {'value': 'Severity 2'},#Severity
    'customfield_24504' : {'value': 'Missed defect'},#Target Cycle/ Values might be out of dropdown. Use f string for all
    'customfield_24528' : '01/01 to 01/08',#Sample Data
    'customfield_24506' : {'value': 'Critical'},#Critical
    'customfield_24515' : '2022-12-28'#Batch Date but pay attention to the format in excel
},
{
    'project': {'id': '21300'},
    'summary': 'TestSinan',#summary
    'description': 'This is a test one',
    'issuetype': {'name': 'Defect'},
    'customfield_24512': {'value': '33_Lot (length is actually 5 bytes with byte 345 as filler)'}, #3072
    'customfield_29815' : '9999999', #RecordID
    'customfield_24502' : {'value': 'Transaction QA'},#Project
    'customfield_24513' : {'value': 'Cognizant'},#Vendor
    'customfield_18909' : {'value': 'WI'}, #State
    'customfield_25100' : {'value':'MILWAUKEE'},#County
    'customfield_24519' : '99999',#Doc Number
    'customfield_26900' : '123',#Recording Book
    'customfield_27309' : '456',#Recording Page
    'customfield_24526' : '2023-06-01',#Recording Date,watch out for the format
    'customfield_26002' : '2023',#DocYear
    'customfield_24501' : {'value': 'T'},#DeedCategory
    'customfield_24511' : {'value': 'MG'},#DAMAR
    #'customfield_24508' : {'value' : ''},#ADC
    'customfield_24505' : {'value': 'Keying error'},#TypeofError
    'customfield_24517' : {'name': 'aalaguvairamani@corelogic.com'},#DetectedBy
    'customfield_24529' : '2023-06-13',#DetectedDate
    'customfield_14991' : {'value': 'Severity 2'},#Severity
    'customfield_24504' : {'value': 'Missed defect'},#Target Cycle/ Values might be out of dropdown. Use f string for all
    'customfield_24528' : '01/01 to 01/08',#Sample Data
    'customfield_24506' : {'value': 'Critical'},#Critical
    'customfield_24515' : '2022-12-28'#Batch Date but pay attention to the format in excel
}

]

jira =start_connection()
issue = jira.issue('ETQT-8608')
print(issue.raw['fields']['customfield_24512']['value'])
print(issue.raw['fields'])
print(issue.raw['fields']['issuetype'])
all_fields = jira.fields()
#print(all_fields)
nameMap = {field['id']:field['name'] for field in all_fields}


#getattr(issue.fields,nameMap["customfield_25100"])
#print(nameMap)
#print(issue)
#create_single_issue(jira=jira,project_id='21300',summary='TestSinan',description='This is a test defect',issuetype={'name': 'Defect'})
create_bulk_issues(jira=jira, issue_value_list=QA_Regular_Format1_3072 )
stat_list = read_exc_and_return_status_list(file_name='Example1.xlsx',sheet_name='3072 QA-Regular -CTS')
if len(stat_list) == len(KEY_LIST):
    create_status_csv(HEADER_LIST,key_list=KEY_LIST,status_list=stat_list)
    read_csv_to_update_stat(jira=jira,filename="out2.csv")
else:
    print("Different num of keys and status")
#set_issue_statuses_by_name(jira=jira,keys_list=KEY_LIST,name='Closed')
#print(jira.createmeta())

#print(project_list)


#print(projects)

#print(all_fields)