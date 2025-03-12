import requests
import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog


def showBanner():
    banner = """

 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌           ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌          ▐░▌               ▐░▌     ▐░▌          ▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌          
▐░▌          ▐░▌               ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
▐░▌          ▐░▌               ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌          ▐░▌               ▐░▌      ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌
▐░▌          ▐░▌               ▐░▌               ▐░▌          ▐░▌          ▐░▌▐░▌       ▐░▌▐░▌                    ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                                                     
    """
    print(banner)

    
def getGithubIssues(repo):
    url = f"https://api.github.com/repos/{repo}/issues"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json().get('message')}")
        return []
    
def showIssueDetails(issue):
    print("\n" + "="*40)
    print(f"Title: {issue.get("title")}")
    print(f"Title: {issue['title']}")
    print(f"Status: {issue['state']}")
    print(f"Author: {issue['user']['login']}")
    print(f"URL: {issue['html_url']}")
    print("\nComments:\n" + "-"*40)
    
    comments = requests.get(issue['comments_url']).json()
    if comments:
        for comment in comments:
            print(f"{comment['user']['login']}: {comment['body']}\n")
    else:
        print("No comments.")
        
def main():
    os.system("clear" if os.name == "posix" else "cls")
    showBanner()
    
    repo = prompt("Enter GitHub repository (format: owner/repo): ").strip()
    issues = getGithubIssues(repo)

    if not issues:
        print("No issues found.")
        return

    choices = [(str(issue['number']), f"#{issue['number']} {issue['title']} ({issue['state']})") for issue in issues]
    
    selected = radiolist_dialog(
        title="GitHub Issues",
        text="Select an issue to view details:",
        values=choices
    ).run()

    if selected is not None:
        selectedIssue = next(issue for issue in issues if str(issue['number']) == selected)
        showIssueDetails(selectedIssue)

#Driver Code
if __name__ == "__main__":
    main()