# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1pE7hTgsZMoH-0xGzXsXK6UOljdGFkyw2
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
HTTPS_PROXY="http://username:password@proxy.example.com:8080"
https_proxy="http://username:password@proxy.example.com:8080"
model_name='bert-base-nli-mean-tokens'
model=SentenceTransformer(model_name)



import re
import requests
import urllib
from bs4 import BeautifulSoup
import pandas as pd

# function to make url. 
def make_url(base_url , comp):
    url = base_url
    for r in comp:
        url = '{}/{}'.format(url, r)
    return url

def scraping_files(year1):
  list_url = []
  # define the urls needed to make the request, let's start with all the daily filings
  base_url = r"https://www.sec.gov/Archives/edgar/full-index"
  # The daily-index filings, requir/e a year and content type (html, json, or xml).
  year_url = make_url(base_url, [year1, 'index.json'])
  # Display the new Year URL
  print('-'*100)
  print('Building the URL for Year: {}'.format(year1))
  print("URL Link: " + year_url)
  # request the content for 2019, remember that a JSON strucutre will be sent back so we need to decode it.
  content = requests.get(year_url,headers=hdr)
  decoded_content = content.json()
  # the structure is almost identical to other json requests we've made. Go to the item list.
  # AGAIN ONLY GRABBING A SUBSET OF THE FULL DATASET 
  for item in decoded_content['directory']['item'][0:4]: 
    # # get the name of the folder
    print('-'*100)
    print('Pulling url for Quarter: {}'.format(item['name']))
    # The daily-index filings, require a year, a quarter and a content type (html, json, or xml).
    qtr_url = make_url(base_url, [year1, item['name'], 'index.json'])
    # print out the url.
    print("URL Link: " + qtr_url)
    # Request, the new url and again it will be a JSON structure.
    file_content = requests.get(qtr_url,headers=hdr)
    decoded_content = file_content.json()
    print('-'*100)
    print('Pulling files')
    # for each file in the directory items list, print the file type and file href.
    # AGAIN DOING A SUBSET
    for file in decoded_content['directory']['item'][0:20]:     
        file_url = make_url(base_url, [year1, item['name'], file['name']])
        list_url.append(file_url)
  return list_url

def parser_idx(url):
  master_data = []
  file_url = r'%s' % url
  # request that new content, this will not be a JSON STRUCTURE!
  content = requests.get(file_url,headers=hdr).content
  # we can always write the content to a file, so we don't need to request it again.
  with open('master_20190102.txt', 'wb') as f:
       f.write(content)
  # let's open it and we will now have a byte stream to play with.
  with open('master_20190102.txt','rb') as f:
     byte_data = f.read()

  # Now that we loaded the data, we have a byte stream that needs to be decoded and then split by double spaces.
  data = byte_data.decode("utf-8").split('  ')

  # We need to remove the headers, so look for the end of the header and grab it's index
  for index, item in enumerate(data):
    if "ftp://ftp.sec.gov/edgar/" in item:
      start_ind = index

  # define a new dataset with out the header info.
  data_format = data[start_ind + 1:]
  # now we need to break the data into sections, this way we can move to the final step of getting each row value.
  for index, item in enumerate(data_format):
    
    # if it's the first index, it won't be even so treat it differently
    if index == 0:
        clean_item_data = item.replace('\n','|').split('|')
        clean_item_data = clean_item_data[8:]
    else:
        clean_item_data = item.replace('\n','|').split('|')
        
    for index, row in enumerate(clean_item_data):
        
        # when you find the text file.
        if '.txt' in row:

            # grab the values that belong to that row. It's 4 values before and one after.
            mini_list = clean_item_data[(index - 4): index + 1]
            # l1=mini_list[1].split(',')
            # if len(mini_list) != 0 and (mini_list[1] in companies_name_list) :
            if len(mini_list) != 0 and (mini_list[2] in form_type) :
                mini_list[4] = "https://www.sec.gov/Archives/" + mini_list[4]
                master_data.append(mini_list)
  return master_data  

# # # # # # # # # Function to clean the dataframes extracted # #  # # # # # # 
def data_cleaning(income_df):
    for  i in income_df.columns:
        # print(i)
        l1=income_df[i].unique().tolist()
#         print(l1," ",len(income_df))
        if len(l1)<(len(income_df)/2):
            income_df.drop(columns=[i],inplace=True)
    return income_df


def master_reports(base_url):
  

    base_url = i['file_url']
    base_url1=base_url.replace('FilingSummary.xml','')
    master_report=[]
    # request and parse the content
    content = requests.get(base_url,headers=hdr).content
    soup = BeautifulSoup(content, 'lxml')

    # find the 'myreports' tag because this contains all the individual reports submitted.
    reports = soup.find('myreports')

    # I want a list to store all the individual components of the report, so create the master list.
    # master_reports = []

    # loop through each report in the 'myreports' tag but avoid the last one as this will cause an error.
    for report in reports.find_all('report')[:-1]:

        # let's create a dictionary to store all the different parts we need.
        report_dict = {}
        report_dict['name_short'] = report.shortname.text
        report_dict['name_long'] = report.longname.text
        report_dict['position'] = report.position.text
        report_dict['category'] = report.menucategory.text
        report_dict['url'] = base_url1 + report.htmlfilename.text

        # append the dictionary to the master list.
        master_report.append(report_dict)

        # print the info to the user.
        # print('-'*100)
        # print(base_url + report.htmlfilename.text)
        # print(report.longname.text)
        # print(report.shortname.text)
        # print(report.menucategory.text)
        # print(report.position.text)
    return master_report

def extraction_10K(master_report):
  # create the list to hold the statement urls
  statements_url = []
  for report_dict in master_report:
    # define the statements we want to look for.
    item1 = "consolidated balance sheets"
    item9 = 'condensed consolidated statements of operations'
    item10= 'condensed consolidated statements of cash flows'
    item2 = "consolidated statements of operations and comprehensive income (Loss)"
    
    item4 = "consolidated statements of stockholder's (deficit) equity"
    item6 = "consolidated statements of stockholders' equity"
    # store them in a list.
    report_list = [item1, item2, item4, item6,item9,item10]
    
    # if the short name can be found in the report list.
    if report_dict['name_short'].lower() in report_list:
        print(report_dict['name_short'])
        
        # print some info and store it in the statements url.
        # print('-'*100)
        # print(report_dict['name_short'])
        # print(report_dict['url'])
        statements_url.append(report_dict['url'])
    else:
        report_list.insert(0,report_dict['name_short'])
        vec_report=model.encode(report_list)
        cos_array=cosine_similarity([vec_report[0]], vec_report[1:])
        cos_list=cos_array.tolist()
        if max(cos_list[0])>0.8:
            statements_url.append(report_dict['url'])
  return statements_url

    
def statement_extraction(statements_url):
  # let's assume we want all the statements in a single data set.
  statements_data = []

  # loop through each statement url
  for statement in statements_url:
    
      # define a dictionary that will store the different parts of the statement.
      statement_data = {}
      statement_data['headers'] = []
      statement_data['sections'] = []
      statement_data['data'] = []
      
      # request the statement file content
      content = requests.get(statement,headers=hdr).content
      report_soup = BeautifulSoup(content, 'html')

      # find all the rows, figure out what type of row it is, parse the elements, and store in the statement file list.
      for index, row in enumerate(report_soup.table.find_all('tr')):
          
          # first let's get all the elements.
          cols = row.find_all('td')
          
          # if it's a regular row and not a section or a table header
          if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
              reg_row = [ele.text.strip() for ele in cols]
              statement_data['data'].append(reg_row)
              
          # if it's a regular row and a section but not a table header
          elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
              sec_row = cols[0].text.strip()
              statement_data['sections'].append(sec_row)
              
          # finally if it's not any of those it must be a header
          elif (len(row.find_all('th')) != 0):            
              hed_row = [ele.text.strip() for ele in row.find_all('th')]
              statement_data['headers'].append(hed_row)
              
          else:            
              print('We encountered an error.')

      # append it to the master list.
      statements_data.append(statement_data)
    #   print(statements_data)
  return statements_data

def transform(statements_data):
  # Grab the proper components
    frames=[]
    for i in range(len(statements_data)):
      l1=len(statements_data[i]['headers'])
      income_header =  statements_data[i]['headers'][1:l1]
      income_data = statements_data[i]['data']

      # Put the data in a DataFrame
      income_df = pd.DataFrame(income_data)


      # Define the Index column, rename it, and we need to make sure to drop the old column once we reindex.
      income_df.index = income_df[0]
      income_df.index.name = 'Category'
      income_df = income_df.drop(0, axis = 1)

      # Get rid of the '$', '(', ')', and convert the '' to NaNs.
      income_df = income_df.replace('[\$,)]','', regex=True )\
                          .replace( '[(]','-', regex=True)\
                          .replace( '', 'NaN', regex=True)

      # everything is a string, so let's convert all the data to a float.
    #       income_df.columns=income_header

      # Change the column headers
      # income_df.columns = ['', '', '', '', '','','',]

      frames.append(income_df)
    
    return frames


def header2(statements_data):
    final_list=[]
    for i in range(len(statements_data)):
      l1=len(statements_data[i]['headers'][1])
      list2=statements_data[i]['headers'][1]
      for i in list2:
        if(len(i)<8):
            list2.remove(i)
      final_list.append(list2)
    return final_list


def header(statements_data):
    final_list=[]
    for i in range(len(statements_data)):
      l1=len(statements_data[i]['headers'][0])
      list2=statements_data[i]['headers'][0]
      for i in list2:
        if(len(i)<8):
            list2.remove(i)
      final_list.append(list2)
    return final_list

  
#put years for which forms are to be scraped. 
year_list=['2019']
hdr= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
# list_url=[]

Master_list_url = []

for i in year_list:
  Master_list_url.append(scraping_files(i))

df=pd.read_excel("./Company.xlsx")
companies_name_list=df['Company'].tolist()
company_first=[]
for i in companies_name_list:
  l1=i.split(' ')
  company_first.append(l1[0])
form_type=['10-K','8-K','10-Q']


"""#### Master list to store the url of required companies and the element is of the form ( CIK, Company Name, Form Type, Year and Quarter, url)

> Indented block


"""

 
  

Master_data_Final = []
for j in Master_list_url:
  for i in j:
    i_length=len(i)
    if i[i_length-10:i_length]=="master.idx":
      try:
        Master_data_Final.append(parser_idx(i))
      except:
        pass

"""### Master list to store the data. Each element is in the form (CIK, Company Name, Form Type, Date, URL for file)"""

master_dir=[]
for j in Master_data_Final:
  for i in j:
    if i[1] in company_first or i[1] in companies_name_list:
      master_dir.append(i)

for index, document in enumerate(master_dir):
    
    # create a dictionary for each document in the master list
    document_dict = {}
    document_dict['cik_number'] = document[0]
    document_dict['company_name'] = document[1]
    document_dict['form_id'] = document[2]
    document_dict['date'] = document[3]
    document_dict['file_url'] = document[4]
    if document[1] in companies_name_list or document[1] in company_first:
      master_dir[index] = document_dict

for i in Master_data_Final:
  if i[2] not in form_type:
    Master_data_Final.remove(i)



# convert a normal url to a document url
for i in master_dir:
  normal_url=i['file_url']
  normal_url = normal_url.replace('-','').replace('.txt','/FilingSummary.xml')
  i['file_url']=normal_url
     


for i in master_dir:
  if i['form_id']=="10-K" or i['form_id']=="10-Q":
    print('Company name : ' + i['company_name'])
    print('Company CIK number : ' + i['cik_number'])
    # print('Company Ticket Number : ' + i['company_name'])
    filename=i['cik_number']+'_'+i['form_id']+'_'+i['date']
    base_url=i['file_url'""]
    master_rep=master_reports(base_url)
    statements_url=extraction_10K(master_rep)
#     print(master_rep)
    statements_data=statement_extraction(statements_url)
#     print(statements_data)
    p=transform(statements_data)
    final_header=header(statements_data)
    for i in range(len(p)):
        try:
            m1=final_header[i]
            income_df=data_cleaning(p[i])
            print(income_df)
            print(income_df.columns,"    " ,m1[1:])
            income_df.columns=m1[1:]
        except:
            try:
                final_header1=header2(statements_data)
                m1=final_header1[i]
                income_df=data_cleaning(p[i])
                print(income_df)
                print(income_df.columns,"    " ,m1[1:])
                income_df.columns=m1[1:]
            except:
                pass

        file=filename+'_'+str(i)+'.csv'
        income_df.to_csv(file)

    
  
