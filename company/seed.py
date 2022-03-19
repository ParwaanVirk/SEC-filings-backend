from sre_constants import LITERAL
from company.models import CompanyS, Metric_type, Metrics
import os
import csv
from dateutil import parser
# class KeyObject():
#     param


# Total Liabliitie
# Gross Profit
# Total Revenus
#Stock holder liabilities
# Net Income/Assets. 


def fetch_metric_from_form(metric_name, form_type, cik):
    # for company in company_list:
    current_dir = os.path.dirname(__file__)
    dir_name = os.path.join(current_dir, '../ScrapeCSV')
    metrics = {}
    for filename in os.scandir(dir_name):
        if filename.is_file():
            if filename.name.find(cik + '_' + form_type) != -1:
                with open(os.path.join(dir_name, filename.name)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        # print(row[0].lower().strip())
                        if row[0].lower().strip() == metric_name:
                            # print(row[0] + ' : ' + row[1])
                            if row[0].lower().strip() in metrics:
                                metrics[row[0].lower().strip()]['data'].append(row[1].strip())
                                for i in range(2, len(row)):
                                    metrics[row[0].lower().strip()]['data'].append(row[i])
                            else:
                                metrics[row[0].lower().strip()] = {
                                    'year': filename.name.split('_')[2],
                                    'data': [row[1].strip()]
                                }
                                for i in range(2, len(row)):
                                    metrics[row[0].lower().strip()]['data'].append(row[i])

    if metric_name in metrics:
        return metrics[metric_name]
    else:
        return {}


def Feeder(data_dict, company, metric_type):
    if 'data' in data_dict:
            for element in data_dict['data']:
                print(element)
                if element == 'NaN':
                    element = -1
                
                Metrics.objects.create(
                    Metric_Type = metric_type,
                    Value = element,
                    Filing_Date = data_dict['year'],
                    Filing_Type = "10k",
                    CompanyS = company,
                    Source_Link = "https://www.sec.gov/edgar/searchedgar/companysearch.html"
                )



def seeder_10k():
    company_list = CompanyS.objects.all()
    for company in company_list:
        print('Processing CIK '+ company.CIK_Number)
        total_revenue = fetch_metric_from_form('total revenue', '10-K', company.CIK_Number)
        quarterly_revenue = fetch_metric_from_form('revenue', '10-Q', company.CIK_Number)
        total_liabilities = fetch_metric_from_form('total liabilities', '10-K', company.CIK_Number)
        quarterly_liabilities = fetch_metric_from_form('total liabilities', '10-Q', company.CIK_Number)
        annual_gross_profit = fetch_metric_from_form('gross profit', '10-K', company.CIK_Number)
        quarterly_gross_profit = fetch_metric_from_form('gross profit', '10-Q', company.CIK_Number)
        annual_net_income = fetch_metric_from_form('net income', '10-K', company.CIK_Number)
        quarterly_net_income = fetch_metric_from_form('net income', '10-Q', company.CIK_Number)
        annual_total_assets = fetch_metric_from_form('total assets', '10-K', company.CIK_Number)
        quarterly_total_assets = fetch_metric_from_form('total assets', '10-Q', company.CIK_Number)

        Feeder(total_revenue, company, 'annual revenue')
        Feeder(quarterly_revenue, company, 'quarterly revenue')
        Feeder(total_liabilities, company, 'annual liabilities')
        Feeder(quarterly_liabilities, company, 'quarterly liabilities')
        Feeder(annual_gross_profit, company, 'annual profit')
        Feeder(quarterly_gross_profit, company, 'quarterly profit')
        Feeder(annual_net_income, company, 'annual net income')
        Feeder(quarterly_net_income, company, 'quarterly net income')
        Feeder(annual_total_assets, company, 'annual assets')
        Feeder(quarterly_total_assets, company, 'quarterly assets')


        # print(total_revenue)
        # print(quarterly_revenue)
        # print(total_liabilities)
        # print(quarterly_liabilities)
        # print(annual_gross_profit)
        # print(quarterly_gross_profit)
        # print(annual_net_income)
        # print(quarterly_net_income)
        # print(annual_total_assets)
        # print(quarterly_total_assets)
        print('\n' * 3)
