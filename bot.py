import requests, html, json, tweepy

# Get credits from a local file
with open("creds.json") as f:
    creds = json.load(f)

# Start up tweepy
consumer_key = creds["consumer_key"]
consumer_secret = creds["consumer_secret"]
access_token = creds["access_token"]
access_token_secret = creds["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

while True:
    # Grab one random cartoon and keep the image URL, then another and keep the caption
    # Luckily, the random cartoon API returns two cartoons
    r = requests.get("https://www.newyorker.com/cartoons/random/randomAPI").json()
    image_src = r[0]["src"]
    caption = r[1]["caption"]

    # Unescape the HTML to convert curly quotes and such
    caption = html.unescape(caption)

    # Only tweet if a caption actually exists
    if 140 > len(caption) > 1 : # use 1 instead of 0 since there's the occasional single quote caption
        filename = "temp.jpg"
        image = requests.get(image_src, stream=True)
        with open(filename, "wb") as i:
            for chunk in image:
                i.write(chunk)
        api.update_with_media(filename, caption)
        break
