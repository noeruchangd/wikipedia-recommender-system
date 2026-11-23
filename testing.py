import requests
params = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Category:Featured_articles",
    "cmlimit": 500,
    "format": "json"
}
resp = requests.get("https://en.wikipedia.org/w/api.php",
                    headers={"User-Agent": "wiki-recommender/1.0 (noeruchangd@gmail.com)"}, params=params).json()
if "continue" in resp:
    print('wazoo!')
    print(resp['continue']['cmcontinue'])