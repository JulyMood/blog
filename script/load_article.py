import random
from datetime import datetime, timedelta

import requests
import base64
from app.services import article_service


# 替换为你的GitHub个人访问令牌
token = '*'
# GitHub组织名
org_names = [('langchain-ai', 'LangChain'), ('THUDM', '智谱'), ('datawhalechina', '机器学习'), ('baichuan-inc', '百川')]

# 设置请求头，包括认证信息
headers = {'Authorization': f'token {token}'}

for org_name, _type in org_names:
    # 获取组织的仓库列表
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    repos_response = requests.get(repos_url, headers=headers)

    if repos_response.status_code == 200:
        repos = repos_response.json()
        for repo in repos:
            # 获取每个仓库的README URL
            readme_url = f"https://api.github.com/repos/{org_name}/{repo['name']}/readme"

            readme_response = requests.get(readme_url, headers=headers)
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                # 解码README内容
                readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
                print(f"README for {repo['name']}:\n{readme_content}\n\n")
                create_time = datetime.now() - timedelta(days=random.randint(0, 60))
                article_service.create_article(repo['name'], _type, readme_content, create_time)
            else:
                print(f"Failed to retrieve README for {repo['name']}. Status code: {readme_response.status_code}")
    else:
        print('Failed to retrieve repositories. Status code:', repos_response.status_code)
