from datetime import datetime
from dateutil import relativedelta
import requests
from config import token

birthDate = datetime(2002, 7, 28)
now = datetime.today()
currentDate = datetime(now.year, now.month, now.day)

diff = relativedelta.relativedelta(currentDate, birthDate)

years = diff.years
months = diff.months
days = diff.days


def updateUptime():
    if years > 85:
        return 'null. I am dead. Go out there and enjoy life.'
    elif days == 1:
        if months == 1:
            return '{} years, {} month, {} day'.format(years, months, days)
        else:
            return '{} years, {} months, {} day'.format(years, months, days)
    elif months == 1:
        return '{} years, {} month, {} days'.format(years, months, days)
    elif days == 0:
        if months == 0:
            return '{} years"'.format(years)
        else:
            return '{} years, {} months'.format(years, months, days)
    elif months == 0:
        return '{} years, {} days"'.format(years, days)
    else:
        return '{} years, {} months, {} days'.format(years, months, days)


def converttuple(tup):
    con = ''.join(tup)
    return con


def getGitStats(token):
    headers = {'Authorization': f'token {token}'}
    query = """
    query {
      viewer {
        repositories {
          totalCount
          edges {
            node {
              stargazers {
                totalCount
              }
              languages {
                edges {
                  node {
                    name
                  }
                }
              }
              object(expression: "master") {
                ... on Commit {
                  history {
                    totalCount
                  }
                }
              }
              ref(qualifiedName: "master") {
                target {
                  ... on Commit {
                    history {
                      totalCount
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    data = response.json()['data']['viewer']['repositories']['edges']
    repo_count = len(data)
    star_count = sum([d['node']['stargazers']['totalCount'] for d in data])
    code_count = sum([d['node']['object']['history']['totalCount'] for d in data])
    commit_count = sum([d['node']['ref']['target']['history']['totalCount'] for d in data])
    return repo_count, star_count, code_count, commit_count


def readmeoverwrite():
    repo_count, star_count, code_count, commit_count = getGitStats(token)
    with open("README.md", "r") as file:
        data = file.readlines()
        line4 = ('                 P@@@@@@@@@@@@@@G.                      uptime: ', updateUptime(), "\n")
        line19 = ('   7@@@@@@@5~         :JJ~.  ..  .G@@@@57J&@@@@@@@      Repos: {} | Commits: {} | Stars: {} \n'.format(repo_count, commit_count, star_count))
        line20 = ('   !@@@&@@@@&Y!~^:.         .:  .G@@@@@!@@@@@@@@@@      Lines of code written: {}'.format(code_count))

    tup2str4 = converttuple(line4)
    tup2str19 = converttuple(line19)
    tup2str20 = converttuple(line20)
    data[3] = tup2str4
    data[18] = tup2str19
    data[19] = tup2str20

    with open('README.md', 'w') as file:
        file.writelines(data)


if __name__ == '__main__':
    readmeoverwrite()
