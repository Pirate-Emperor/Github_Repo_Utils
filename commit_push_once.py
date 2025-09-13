import os
import subprocess
import random
from datetime import datetime, timedelta

COMMIT_DATE = "Thu Oct 31 11:30 2024 +0100"
total_minutes = 0
max_daily_minutes = 8 * 60  # 8 hours in minutes
lower_minute = 240
upper_minute = 479

def update_time():
    global COMMIT_DATE, total_minutes
    commit_datetime = datetime.strptime(COMMIT_DATE, "%a %b %d %H:%M %Y %z")
    added_minutes = random.randint(lower_minute, upper_minute)

    # Update the datetime and total minutes
    commit_datetime += timedelta(minutes=added_minutes)
    total_minutes += added_minutes

    # If total_minutes exceeds the daily limit, move to the next day
    if total_minutes > max_daily_minutes:
        overflow_minutes = total_minutes - max_daily_minutes
        commit_datetime += timedelta(minutes=overflow_minutes)
        total_minutes = overflow_minutes  # Carry over the extra time to the next day

    COMMIT_DATE = commit_datetime.strftime("%a %b %d %H:%M %Y %z")
    print("Updated COMMIT_DATE:", COMMIT_DATE)


def is_git_initialized():
    """Check if the current directory is a Git repository."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Git is already initialized.")
        return True
    except subprocess.CalledProcessError:
        print("Git is not initialized.")
        return False

def initialize_git():
    """Initialize a new Git repository."""
    try:
        subprocess.run(["git", "init"], check=True)
        print("Initialized a new Git repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Git: {e}")

def is_remote_connected():
    """Check if there's a remote named 'origin' connected."""
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Remote 'origin' is already set to: {result.stdout.decode().strip()}")
        return True
    except subprocess.CalledProcessError:
        print("No remote 'origin' found.")
        return False
def amend_commit_date(is_empty = False):
    try:
        cmd_list = ["git", "commit", "--amend", f"--date={COMMIT_DATE}", "--no-edit"]
        if is_empty:
            cmd_list.insert(2, "--allow-empty")
        subprocess.run(
            cmd_list,
            check=True
        )
        print("First command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error in first command: {e}")
    
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = COMMIT_DATE

    try:
        cmd_list = ["git", "commit", "--amend", "--no-edit"]
        if is_empty:
            cmd_list.insert(2, "--allow-empty")
        subprocess.run(
            cmd_list,
            check=True,
            env=env
        )
        print("Second command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error in second command: {e}")

def set_remote_origin(github_repo_url):
    """Set the remote 'origin' to the provided GitHub repository URL."""
    try:
        subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)
        print(f"Remote 'origin' set to {github_repo_url}.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting remote 'origin': {e}")

def set_upstream_branch():
    """Set the upstream branch to origin/main."""
    try:
        subprocess.run(["git", "commit", "--allow-empty", "-m", "Init Git"], check=True)
        amend_commit_date(is_empty=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", "main"], check=True)
        print("Upstream branch set to 'origin/main'.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting upstream branch: {e}")

def setup_git_repository(github_repo_url):
    # Check if Git is initialized; if not, initialize it
    if not is_git_initialized():
        initialize_git()

    # Check if a remote 'origin' exists; if not, set it
    if not is_remote_connected():
        set_remote_origin(github_repo_url)

    # Set the upstream branch to 'origin/main'
    set_upstream_branch()

def git_add_commit_push(repo_dir, relative_file_path, commit_message):
    try:
        # Change to the repository directory
        os.chdir(repo_dir)

        # Stage the file
        subprocess.run(['git', 'add', relative_file_path], check=True)

        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if there is any output (indicating staged files)
        if result.stdout.strip():
            # Commit the file
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            amend_commit_date()
            # Push the commit
            subprocess.run(['git', 'push'], check=True)

            print(f"Successfully committed and pushed {relative_file_path}")
            update_time()
        else:
            print("No files are staged for commit.")

       

    except subprocess.CalledProcessError as e:
        print(f"Failed to commit and push {relative_file_path}. Error: {e}")

def traverse_and_commit(repo_dir, ignore_list):
    tree_directory = os.walk(repo_dir)
    for root, dirs, files in tree_directory:
        for file in files:
            # Get the file path relative to the repository root
            relative_file_path = os.path.relpath(os.path.join(root, file), repo_dir)
            if relative_file_path in ignore_list:
                continue
            commit_message = f"Add {relative_file_path}"  # CustomPize your commit message here
            git_add_commit_push(repo_dir, relative_file_path, commit_message)

if __name__ == "__main__":
    github_repo_url = "https://github.com/Pirate-Emperor/CodeMuse.git"
    directory_to_commit = r"D:\Z_PROJECTS\Personal_Projects\Ongoing\CodeMuse"
    COMMIT_DATE = "Sat Aug 27 18:21 2024 +0100"
    lower_minute = 471
    upper_minute = 479
    ignore_list = ["commit_push_once.py"]
    setup_git_repository(github_repo_url)
    traverse_and_commit(directory_to_commit, ignore_list)
