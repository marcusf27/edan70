from requests_html import HTMLSession 

session = HTMLSession()

url = 'https://nordiskfamiljebok.dh.gu.se/article/1/1'

response = session.get(url)
response.html.render()