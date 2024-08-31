import requests
import os

# Replace with your GitHub username and personal access token
GITHUB_USERNAME = "Pirate-Emperor"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN_META')

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

# Function to get user's public and private repositories
def get_repositories(username):
    url = f"{GITHUB_API_URL}/user/repos"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()

# Function to get user's profile data
def get_user_profile(username):
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()

# Function to count commits for a single repository
def count_commits(username, repo_name):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/commits"
    try:
        response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
        response.raise_for_status()
        return len(response.json())
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Repository not found: {repo_name}")
        else:
            print(f"Error fetching commits for {repo_name}: {e}")
        return 0


# Function to get user's commit count across all repositories
def get_commit_count(username, repos):
    commit_count = 0
    for repo in repos:
        repo_name = repo['name']
        commits = count_commits(username, repo_name)
        commit_count += commits
    return commit_count

# Function to get user's pull requests
def get_pull_requests(username):
    url = f"{GITHUB_API_URL}/search/issues?q=type:pr+author:{username}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()['total_count']

# Function to get user's issues
def get_issues(username):
    url = f"{GITHUB_API_URL}/search/issues?q=type:issue+author:{username}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()['total_count']

# Function to get user's reviews
def get_reviews(username):
    url = f"{GITHUB_API_URL}/search/issues?q=type:pr+reviewed-by:{username}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()['total_count']

# Function to get stars count from user's repositories
def get_stars_count(repos):
    stars_count = sum(repo['stargazers_count'] for repo in repos)
    return stars_count

# Function to get followers count
def get_followers_count(profile_data):
    return profile_data['followers']

# Main function to gather all information
def get_github_profile_info(username):
    # Get user's repositories and profile data
    repos = get_repositories(username)
    profile_data = get_user_profile(username)

    # Get the necessary information
    commit_count = get_commit_count(username, repos)
    pull_requests_count = get_pull_requests(username)
    issues_count = get_issues(username)
    reviews_count = get_reviews(username)
    stars_count = get_stars_count(repos)
    followers_count = get_followers_count(profile_data)

    return {
        "commits": commit_count,
        "pull_requests": pull_requests_count,
        "issues": issues_count,
        "reviews": reviews_count,
        "stars": stars_count,
        "followers": followers_count
    }

# Get GitHub profile information
github_info = get_github_profile_info(GITHUB_USERNAME)

# Print the collected information
print(f"GitHub Information for {GITHUB_USERNAME}:")
print(f"Commits: {github_info['commits']}")
print(f"Pull Requests: {github_info['pull_requests']}")
print(f"Issues: {github_info['issues']}")
print(f"Reviews: {github_info['reviews']}")
print(f"Stars: {github_info['stars']}")
print(f"Followers: {github_info['followers']}")