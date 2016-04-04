__author__ = 'amrit'

import csv

'''/home/amrit/GITHUB/vcl_logs/pitsA.csv
/home/amrit/GITHUB/vcl_logs/pitsB.csv
/home/amrit/GITHUB/vcl_logs/pitsC.csv
/home/amrit/GITHUB/vcl_logs/pitsD.csv
/home/amrit/GITHUB/vcl_logs/pitsE.csv
/home/amrit/GITHUB/vcl_logs/pitsF.csv'''

fo=open('pitsF_1.txt','w')
f1=open('pitsF_2.txt','w')

files=['pitsE.csv']#,'pitsB.csv','pitsC.csv','pitsD.csv','pitsE.csv','pitsF.csv']
for i in files:
    print(i)
    with open('/home/amrit/GITHUB/vcl_logs/'+i,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Severity'] == '2':
                fo.write(row['Subject'] + ' ' + row['Description']+'\n' )
            if row['Severity'] == '1':
                fo.write(row['Subject'] + ' ' + row['Description']+'\n' )
            if row['Severity'] == '3':
                f1.write(row['Subject'] + ' ' + row['Description']+'\n' )
            if row['Severity'] == '4':
                f1.write(row['Subject'] + ' ' + row['Description']+'\n' )
            if row['Severity'] == '5':
                f1.write(row['Subject'] + ' ' + row['Description']+'\n' )
fo.close()