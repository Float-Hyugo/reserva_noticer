import requests
import urllib.request, urllib.error
import json
import scrape
import datetime,time


def process():
  
  url = 'https://api.line.me/v2/bot/message/broadcast'
  with open('config.json',mode="r") as f:
    access_data = json.load(f)
  token = access_data["settings"]["LINE_channel_access_token"]
  channel_access_token = token

  
  x = scrape.get_today()
  t = ""
  t += x[0] + '\n'
  
  for i in x[1]:
    t += f'{i[0]}:{i[1]}人\n'
  
  data = {
      'messages' : [{
          'type':'text',
          'text':t
      }]
  }
  jsonstr = json.dumps(data).encode('ascii')
  request = urllib.request.Request(url, data=jsonstr)
  request.add_header('Content-Type', 'application/json')
  request.add_header('Authorization', 'Bearer ' + channel_access_token)
  request.get_method = lambda: 'POST'

  response = urllib.request.urlopen(request)

if __name__ == "__main__":
  while True:
    now = datetime.datetime.now().strftime('%H:%M')
    if now == '0:00':
      process()
    time.sleep(60)