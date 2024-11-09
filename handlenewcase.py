import csv
from urls import HOST
from requests import post
from dbcontrol import base_add

def add_case(fp: str):
    with open(fp, 'r') as file:
        case_d = file.read()
    
    case = [x.split(',') for x in case_d.split('\n')]
    
    content = {}
    chance = {}
    
    for i in case:
        content[i[0]]=i[2]
        
    for i in case:
        chance[i[0]]=int(i[1])
    
    base_add('case',{
        'id':0,
        'name':fp.replace('case_handle/','').replace('.csv',''),
        'content':content,
        'chance':chance,
        'photo':''
    })
    
    print('Кейс добавлен')
if __name__ == "__main__":
    add_case('static/case_handle/test.csv')
