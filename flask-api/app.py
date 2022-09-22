from flask import Flask, request
import requests, json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from numerize import numerize

app = Flask(__name__)

@app.route('/picuki/profile', methods=['GET']) 
def get_instagram_followers_picuki():
    user = request.args.get('user')

    try:
        if user is None:
            return "Error: invalid request"
        
        page = requests.get('https://www.picuki.com/profile/' + user)
        soup = BeautifulSoup(page.content, 'html.parser')
        follower_count = int((soup.find_all('span', class_='followed_by')[0].get_text()).replace(',',''))
        follower_count_numerize = numerize.numerize(follower_count)
        
        response = {
            'user': user,
            'follower_count': follower_count_numerize
        }
        
        return json.dumps(response)

    except Exception as e:
        print(e)
        response = {
            'user': user,
            'follower_count': 'Unknown'
        }
        
        return json.dumps(response)

@app.route('/instagram/profile', methods=['GET']) 
def get_instagram_followers():
    user = request.args.get('user')

    try:
        if user is None:
            return "Error: invalid request"

        url = 'https://www.instagram.com/' + user

        driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        driver.quit()

        content = soup.find('meta', {'name': 'description'})['content']
        follower_count = content.split(',')[0].split(' ')[0]

        response = {
            'user': user,
            'follower_count': follower_count
        }

        return json.dumps(response)

    except Exception as e:
        print(e)
        response = {
            'user': user,
            'follower_count': 'Unknown'
        }
        
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)