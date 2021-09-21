import git
from git import Repo
import os

def is_repository(repo_dir):
    repo_path = os.path.abspath(repo_dir)

    if not os.path.exists(repo_path):
        return False

    try:
        _ = git.Repo(repo_path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False 


def clone_repository(token, url, repo_dir):
    git_url="https://{token}@{url}".format(
        token=token,
	url=url
    )
    
    try:
        Repo.clone_from(git_url, repo_dir)
    except git.exc.GitCommandError:
        raise git.exc.GitCommandError("git Repository konnte nicht geklont werden")


def add_repository(repo_dir, files, commit_msg):
    repo_path = os.path.abspath(repo_dir)

    try:
        repo = Repo(repo_path)
	
        for f in files:
           repo.git.add(os.path.abspath(os.path.join(repo_path, f)))
	   
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
    except git.exc.GitCommandError:
        raise git.exc.GitCommandError("Änderungen konnten nicht hochgeladen werden")


def update_repository(repo_dir):
    repo_path = os.path.abspath(repo_dir)

    repo = Repo(repo_path)
    origin = repo.remote(name='origin')
    origin.pull()