# import requests
# api_key = '2961dcb2e4336ffa43975ece6fdaec32'
# url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={api_key}'
# param = {'movieNm': 'Kill Bill: Vol. 1'}
# response = requests.get(url, params=param).json() 
# print(response['movieListResult']['movieList'][0]['movieNmEn'])

from bs4 import BeautifulSoup
import requests
from pprint import pprint
# api_key = '2961dcb2e4336ffa43975ece6fdaec32'
# url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={api_key}'
# param = {'peopleNm': '주진모'}
# response = requests.get(url, params=param).json() 
# print(response)

response_forko = requests.get(f'https://www.google.com/search?q=johnny depp&ie=UTF-8')
html = response_forko.text
soup = BeautifulSoup(html, 'html.parser')
my_site = soup.select('#rhs > div > div.EyBRub.kp-blk.knowledge-panel.Wnoohf.OJXvsb > div.xpdopen > div.ifM9O > div > div.kp-header > div:nth-child(2) > div.kp-hc > div > div > div.SPZz6b > div.kno-ecr-pt.PZPZlf.gsmt > span')
pprint(my_site)
