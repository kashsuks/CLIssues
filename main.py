import requests
import argparse

def getGithubIssues(repo):
    url = f"https://api.github.com/repos/{repo}/issues"
    response = requests.get(url)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            print(f"#{issue['number']} - {issue['title']} (Status: {issue['state']})")
    else:
        print(f"Error: {response.status_code} - {response.json().get('message')}")
        
# Driver Code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Github Issues From a Public Repository")
    parser.add_argument("repo", help="Repository in the format owner/repo")
    
    args = parser.parse_args()
    getGithubIssues(args.repo)