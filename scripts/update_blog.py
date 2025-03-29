import feedparser
import git
import os

rss_url = 'https://api.velog.io/rss/@uranus020'
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

repo = git.Repo(repo_path)

# Git config 설정
repo.git.config('--global', 'user.name', 'github-actions[bot]')
repo.git.config('--global', 'user.email', 'github-actions[bot]@users.noreply.github.com')

feed = feedparser.parse(rss_url)

has_changes = False

for entry in feed.entries:
    file_name = entry.title.replace('/', '-').replace('\\', '-') + '.md'
    file_path = os.path.join(posts_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')
        has_changes = True

# 변경이 있을 경우에만 push
if has_changes:
    token = os.environ.get("GH_TOKEN")
    origin = repo.remote(name='origin')
    origin.set_url(f'https://x-access-token:{token}@github.com/Uranus020/velog.git')
    repo.git.push()
