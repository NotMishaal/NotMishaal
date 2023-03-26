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
    headers = {"Authorization": f"Bearer {token}"}
    query = """
        query {
          viewer {
            repositories(first: 100) {
              totalCount
              edges {
                node {
                  stargazers {
                    totalCount
                  }
                  object(expression: "master") {
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
    """
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GraphQL query failed with status code {response.status_code}. Response: {response.text}")

    data = response.json()['data']['viewer']['repositories']['edges']
    repo_count = len(data)
    star_count = sum([data[i]['node']['stargazers']['totalCount'] for i in range(repo_count)])
    commit_count = sum([data[i]['node']['object']['history']['totalCount'] for i in range(repo_count) if
                        data[i]['node']['object'] is not None])

    return repo_count, star_count, commit_count


def readmeoverwrite():
    repo_count, star_count, commit_count = getGitStats(token)
    with open("README.md", "r") as file:
        data = file.readlines()
        line4 = ('                 P@@@@@@@@@@@@@@G.                      uptime: ', updateUptime(), "\n")
        line19 = ('   7@@@@@@@5~         :JJ~.  ..  .G@@@@57J&@@@@@@@      Repos: {} | Stars: {} \n'.format(repo_count, star_count))
        line20 = ('   !@@@&@@@@&Y!~^:.         .:  .G@@@@@!@@@@@@@@@@      Commits: {} \n'.format(commit_count))

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
