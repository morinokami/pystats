import requests
import yaml

url = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'

def main():
    r = requests.get(url)
    data = yaml.load(r.content)

    res = {}
    for lang in data:
        res[lang] = {}
        res[lang]['extensions'] = data[lang].get('extensions', [])
        res[lang]['filenames'] = data[lang].get('filenames', [])
    
    with open('languages.yml', 'w') as f:
        yaml.dump(res, stream=f)

if __name__ == '__main__':
    main()
