import requests


ARCHIVE_URL = 'https://github.com/{user}/{repo}/archive/master.zip'
API_BASE = 'https://api.github.com/repos'


def _get(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    return r

def get_archive(user, repo):
    url = ARCHIVE_URL.format(user=user, repo=repo)
    return _get(url).content

def get_attrs(user, repo):
    url = API_BASE + '/{user}/{repo}'.format(user=user, repo=repo)
    data = _get(url).json()
    return {
        'name': data['name'],
        'description': data['description'],
        'url': data['html_url'],
        'size': data['size'],
        'stars': data['stargazers_count'],
        'forks': data['forks'],
        'watchers': data['watchers'],
    }

def get_languages(user, repo):
    url = API_BASE + '/{user}/{repo}/languages'.format(user=user, repo=repo)
    return _get(url).json()
