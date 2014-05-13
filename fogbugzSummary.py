import requests
from bs4 import BeautifulSoup
import csv


class FS:
    def __init__(self):
        self.url = 'https://enstratus.fogbugz.com/api.asp?'
        self.token_string = 'ENTER TOKEN STRING HERE'

        self.bugs_qstrings_curent = {
            'Total Open Bugs': 'category:"Bug" Status:"Active"',
            'Total Resolved Bugs': 'category:"Bug" Status:"Resolved"',
            'Total Closed Bugs': 'category:"Bug" Status:"Closed"',
        }
        self.bugs_qstrings_past = {
            'Total Opened Bugs': 'category:"Bug" opened:',
            'Total Closed Bugs': 'category:"Bug" closed:',
            'Total Resolved Bugs': 'category:"Bug" resolved:',
        }

    def get_cases_query(self,qString):
        request_string = 'https://enstratus.fogbugz.com/api.asp?token=%s&cmd=search&q=%s&cols=sPriority' % (self.token_string,qString)
        #print(request_string)
        return requests.get(request_string)

    def query_summary(self,range):

        _rows = []

        _fieldnames=['Summary','Total','Blocker','Critical','Major', 'Minor']
        sortindex = _fieldnames.index('Total')
        fileprefix='summary'
        if (range=='0'):
            iterator = self.bugs_qstrings_curent.items()
        else:
            iterator = self.bugs_qstrings_past.items()

        pathname = 'app/static/data/' #ADJUST PATH
        filename='%s%s.csv' % (fileprefix,range)
        csvfile = open(filename, 'w')
        caseswriter = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        caseswriter.writerow(_fieldnames)


        for k, v in iterator:
            total_count = 0
            blocker_count = 0
            critical_count = 0
            major_count = 0
            minor_count = 0
            query=v
            if range=='1':
                query=query+'"-1w.."'
            elif range=='2':
                query=query+'"-4w.."'
            elif range=='3':
                query=query+'"1/1/2014..now"'
            elif range=='4':
                query=query+'"-365d.."'

            cases = self.get_cases_query(query)
            soup = BeautifulSoup(cases.text, "xml")
            for message in soup.findAll('cases'):
                total_count = message.attrs['count']
                all_cases = message.findAll('case')
                for case in all_cases:
                    if case.find('sPriority').text == 'Blocker':
                        blocker_count += 1
                    elif case.find('sPriority').text == 'Critical':
                        critical_count += 1
                    elif case.find('sPriority').text == 'Major':
                        major_count += 1
                    elif case.find('sPriority').text == 'Minor':
                        minor_count += 1
            _rows.append([k, int(total_count), blocker_count, critical_count, major_count,minor_count])


        rows = [[row[sortindex]]+row for row in _rows]
        rows.sort(reverse=True, key=(lambda x: x))
        rows = [row[1:] for row in rows]
        for ii in rows:
            caseswriter.writerow(ii)
        csvfile.close()
        return rows

fs = FS()
for ii in ('0','1', '2', '3', '4'):
    fs.query_summary(ii)
