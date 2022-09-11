from flask import Flask, request
import requests, json
from bs4 import BeautifulSoup
from numerize import numerize

app = Flask(__name__)

@app.route('/', methods=['GET']) 
def get_instagram_followers():
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

    except:
        response = {
            'user': user,
            'follower_count': 'Unknown'
        }
        
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)