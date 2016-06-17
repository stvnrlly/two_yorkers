import requests, html, json, tweepy

with open("creds.json") as f:
    creds = json.load(f)

consumer_key = creds["consumer_key"]
consumer_secret = creds["consumer_secret"]
access_token = creds["access_token"]
access_token_secret = creds["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

image_src = requests.get("http://www.newyorker.com/cartoons/random/randomAPI1").json()[0]["src"]
caption = requests.get("http://www.newyorker.com/cartoons/random/randomAPI1").json()[0]["caption"]
if 140 > len(caption) > 0 :
    filename = "temp.jpg"
    image = requests.get(image_src, stream=True)
    with open(filename, "wb") as i:
        for chunk in image:
            i.write(chunk)
    api.update_with_media(filename, html.unescape(caption))
