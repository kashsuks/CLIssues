from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, ListView, ListItem, Static
from textual.containers import Vertical
import requests


class GitHubIssuesApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    ListView {
        width: 80%;
        height: 60%;
        margin: 1;
    }
    Input {
        width: 50%;
        margin: 1;
    }
    Button {
        margin: 1;
    }
    Static {
        width: 80%;
        height: auto;
        padding: 1;
        border: round green;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Input(placeholder="Enter GitHub repository (owner/repo)", id="repoInput"),
            Button("Fetch Issues", id="fetchButton"),
            ListView(id="issuesList"),
            Static("Select an issue to view details", id="issueDetails"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#fetchButton").disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "fetchButton":
            self.fetchIssues()

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self.showIssueDetails()

    def fetchIssues(self) -> None:
        repo = self.query_one("#repoInput").value.strip()
        if not repo:
            return

        url = f"https://api.github.com/repos/{repo}/issues"
        response = requests.get(url)

        if response.status_code == 200:
            issues = response.json()
            listView = self.query_one("#issuesList")
            listView.clear()
            for issue in issues:
                item = ListItem(Static(issue["title"]))
                item.data = issue
                listView.append(item)
        else:
            self.query_one("#issueDetails").update(f"Error: {response.status_code} - {response.json().get('message')}")

    def showIssueDetails(self) -> None:
        listView = self.query_one("#issuesList")
        if not listView.highlighted_child:
            return

        selectedItem = listView.highlighted_child
        if not hasattr(selectedItem, 'data'):
            return

        issue = selectedItem.data
        comments = requests.get(issue["comments_url"]).json() if "comments_url" in issue else []
        commentsText = "\n".join(f"{c['user']['login']}: {c['body']}" for c in comments) if comments else "No comments."

        details = (
            f"[bold]Title:[/bold] {issue['title']}\n"
            f"[bold]Status:[/bold] {issue['state']}\n"
            f"[bold]Author:[/bold] {issue['user']['login']}\n"
            f"[bold]URL:[/bold] {issue['html_url']}\n\n"
            f"[bold]Comments:[/bold]\n{commentsText}"
        )
        self.query_one("#issueDetails").update(details)

if __name__ == "__main__":
    GitHubIssuesApp().run()