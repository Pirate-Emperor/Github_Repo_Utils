import os
import requests

username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')
print(f"Username: {username}\nToken: {token}")
# Retrieve repositories
def get_repositories():
    url = f'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    repositories = []
    while url:
        response = requests.get(url, headers=headers)
        repositories.extend(response.json())
        url = None
        if 'Link' in response.headers:
            links = response.headers['Link'].split(', ')
            for link in links:
                if 'rel="next"' in link:
                    url = link.split(';')[0][1:-1]
    return repositories

# Make repositories public
def make_public(repositories):
    for repo in repositories:
        repo_name = repo['name']
        url = f'https://api.github.com/repos/{username}/{repo_name}'
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'private': False
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Repository '{repo_name}' is now public.")
        else:
            print(f"Failed to make repository '{repo_name}' public.")

if __name__ == '__main__':
    repositories = get_repositories()
    print(f"Repo Count: {len(repositories)}")
    make_public(repositories)
