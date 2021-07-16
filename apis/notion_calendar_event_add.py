import requests, json
import os
NOTION_API_KEY='secret_QGnRiFqCpdqfaTgnkDqbNvffMxpNcwLiJZrBzW9Al6D' 
DATABASE_ID='d714a888485f406697c049e50977212b' 
#NOTION_API_KEY = os.environ['NOTION_API_KEY']
#DATABASE_ID = os.environ['DATABASE_ID']

# post
def notion_calendar_push(input_data):
    url = 'https://api.notion.com/v1/pages'
    header = {
        'Authorization':'Bearer ' + NOTION_API_KEY, # + os.environ['NOTION_API_KEY'], 
        'Content-Type' : 'application/json',
        'Notion-Version' : '2021-05-13'
    }
    data = convert_json(input_data).encode('utf8')
    
    requests.post(url, headers=header, data=data)
    print('notion calendar - 추가 완료')

# data jsonify
def convert_json(data):
    name = {'title' : [{'text' : {'content' : data['name']}}]}
    date = {'date' : {
        'start' : data['start_date'],
        'end' : data['end_date']
    }}
    select = {'select' : {
        'name' : data['place']
    }}

    result = {}
    result['parent'] = {'database_id' : DATABASE_ID} # os.environ['DATABASE_ID']  } 
    result['properties'] = {
        'Name' : name,
        'Date' : date,
        'Place' : select
    }
    return json.dumps(result, ensure_ascii=False)