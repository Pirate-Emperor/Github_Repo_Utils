import os
import time
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

# Configuration: Specify the root directory containing all your repositories
ROOT_DIRECTORY = "D:/Z_PROJECTS/Personal_Projects/Completed"
BRANCH = "main"  # Change to your default branch if different
CHECK_INTERVAL = 24 * 60 * 60  # Interval for checking new repos (in seconds), here it's 1 day

class GitSyncHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def sync_repo(self):
        try:
            # Pull latest changes from remote
            print(f"Pulling changes for {self.repo_path}")
            self.repo.git.pull('origin', BRANCH)

            # Stage all changes
            print(f"Staging changes for {self.repo_path}")
            self.repo.git.add(A=True)

            # Commit changes if there are any
            if self.repo.is_dirty():
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Committing changes for {self.repo_path}")
                self.repo.index.commit(f"Auto-sync commit at {now}")

                # Push changes to remote
                print(f"Pushing changes for {self.repo_path}")
                self.repo.git.push('origin', BRANCH)

        except Exception as e:
            print(f"Failed to sync {self.repo_path}: {str(e)}")

    def on_any_event(self, event):
        if not event.is_directory:
            print(f"Change detected in {self.repo_path}")
            self.sync_repo()

def find_git_repositories(root_directory):
    repos = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if '.git' in dirnames:
            repo_path = os.path.abspath(dirpath)
            print(f"Repostiory Found: {repo_path}")
            repos.append(repo_path)
    return repos

def monitor_repositories(repositories, observers):
    for repo_path in repositories:
        if repo_path not in observers:
            print(f"Starting to monitor {repo_path}")
            event_handler = GitSyncHandler(repo_path)
            observer = Observer()
            observer.schedule(event_handler, path=repo_path, recursive=True)
            observer.start()
            observers[repo_path] = observer

def dynamic_addition_monitor(root_directory, observers):
    while True:
        print("Checking for new repositories...")
        repos = find_git_repositories(root_directory)
        monitor_repositories(repos, observers)
        print(f"Next check in {CHECK_INTERVAL // 3600} hours.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    observers = {}
    repos = find_git_repositories(ROOT_DIRECTORY)
    monitor_repositories(repos, observers)

    # Start a separate thread for dynamic addition
    thread = threading.Thread(target=dynamic_addition_monitor, args=(ROOT_DIRECTORY, observers))
    thread.daemon = True
    thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers.values():
            observer.stop()
        for observer in observers.values():
            observer.join()
