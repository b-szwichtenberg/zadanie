import pandas as pd
import os
import glob
import re
import argparse

#Get data
folder = "./emails"
files_txt = []
files_csv = []
    
files_txt = [pd.read_csv(file, header=None) 
             for file in glob.glob(os.path.join(folder ,"*.txt"))]
files_csv = [pd.read_csv(file, sep=";") 
             for file in glob.glob(os.path.join(folder ,"*.csv"))]
    
df_txt = pd.concat(files_txt)
df_csv = pd.concat(files_csv)
df_csv = df_csv.iloc[:,1]
df = pd.concat([df_txt,df_csv])

correct_mail = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9._%+-]+\.[A-Z|a-z]{1,4}'


#Task 1        
def incorrect_mails():
    count=0
    for index, row in df.itertuples():
        if(re.fullmatch(correct_mail, row)):
            continue
        else:
            count += 1
    print(f'Invalid emails ({count}):')
    
    for index, row in df.itertuples():
        if(re.fullmatch(correct_mail, row)):
            continue
        else:
            print(row)


#Task 2
def emails_by_text(text):
    count=0
    for index, row in df.itertuples():
        if(re.fullmatch(correct_mail, row)):
            if text in row:
                count += 1
            else:
                continue
    print(f'Found emails with \'{text}\' in email ({count}):')

    for index, row in df.itertuples():
        if(re.fullmatch(correct_mail, row)):
            if text in row:
                print(row)
            else:
                continue

#Task 3
def group_mails():
    df_1=df.copy()
    df_1['domena']=df_1[0].astype(str).str.extract(r'(@.+.+)')
    df_1 = df_1.dropna()
    df_1 = df_1.sort_values(['domena',0])
    df_2 = df_1.groupby('domena')['domena'].count()
    df_3 = df_1.groupby('domena')[0].apply(list)
    print(df_2)
    print(df_3)

#parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_incorrect_mails = subparsers.add_parser('incorrect-emails', help='print invalid emails')
parser_incorrect_mails.set_defaults(func=incorrect_mails)

parser_emails_by_text = subparsers.add_parser('search str', help='take a string argument and print found emails one per line')
parser_emails_by_text.set_defaults(func=emails_by_text)

parser_group_mails = subparsers.add_parser('group-by-domain', help='group emails by domain')
parser_group_mails.set_defaults(func=group_mails)

#Call functions
#incorrect_mails()
#emails_by_text("yahoo")
#group_mails()