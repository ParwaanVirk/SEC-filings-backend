from company.models import CompanyS, Metrics, Performance
import os
import csv


def fetch_metric_from_form(metric_name, form_type, cik):
    current_dir = os.path.dirname(__file__)
    dir_name = os.path.join(current_dir, '../scraping')
    metrics = {}

    for filename in os.scandir(dir_name):
        if filename.is_file():
            if filename.name.find(cik + '_' + form_type) != -1:
                with open(os.path.join(dir_name, filename.name)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    count = 0
                    link = ''
                    for row in csv_reader:
                        if count == 0:
                            link = row[0]
                            count = count + 1
                            continue
                

                        if row[0].lower().strip() == metric_name:
                            
                            if row[0].lower().strip() in metrics:
                                metrics[row[0].lower().strip()]['data'].append(row[1].strip())
                                for i in range(2, len(row)):
                                    metrics[row[0].lower().strip()]['data'].append(row[i])
                            else:
                                metrics[row[0].lower().strip()] = {
                                    'year': filename.name.split('_')[2],
                                    'data': [row[1].strip()],
                                    'link': link
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
            if element == 'NaN':
                element = -1
            
            Metrics.objects.create(
                Metric_Type = metric_type,
                Value = element,
                Filing_Date = data_dict['year'],
                Filing_Type = "10k",
                CompanyS = company,
                Source_Link = data_dict['link']
            )

def performance_seeder(cik):

    company = CompanyS.objects.filter(CIK_Number = cik)[0]
    company_metrics = Metrics.objects.filter(CompanyS__CIK_Number = cik)
    total_reveue_metrics = []
    total_profitability_metrics = []
    for metric in company_metrics:
        if metric.Metric_Type == 'annual revenue':
            total_reveue_metrics.append(metric.Value)
        if metric.Metric_Type == 'annual profit':
            total_profitability_metrics.append(metric.Value)

    if len(total_reveue_metrics) < 2:
        growth = 100
    else:
        growth = (max(total_reveue_metrics) - min(total_reveue_metrics)) / min(total_reveue_metrics) * 100

    if len(total_profitability_metrics) < 2:
        profitability = 100
    else:
        profitability = (max(total_profitability_metrics) - min(total_profitability_metrics)) / min(total_profitability_metrics) * 100

    if len(total_profitability_metrics) > 1 and len(total_reveue_metrics) > 1:
        investability = (growth + profitability) / 2
    else:
        investability = 100

    Performance.objects.create(
        Growth = round(growth, 2),
        Profitability = round(profitability, 2), 
        Investibility = round(investability, 2),
        CompanyS = company
    )

def seeder_10k():
    company_list = CompanyS.objects.all()
    for company in company_list:
        
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

        performance_seeder(company.CIK_Number)






        
