from datetime import datetime
from dateutil import relativedelta
import requests
import os

token = os.environ['ACCESS_TOKEN']

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


def getGitStats(token, url):
    headers = {'Authorization': 'Bearer '+token}
    query = """
        query {
          viewer {
            repositories(first: 1000, isFork: false) {
              totalCount
              edges {
                node {
                  stargazers {
                    totalCount
                  }
                  refs(refPrefix: "refs/heads/", first: 100) {
                    totalCount
                    nodes {
                      name
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
        }
    """


    headers = {'Authorization': 'Bearer '+token}
    response = requests.post(url, json={'query': query}, headers=headers)

    data = response.json()['data']['viewer']['repositories']['edges']

    repo_count = sum(1 for _ in data)
    star_count = sum(edge['node']['stargazers']['totalCount'] for edge in data)
    commit_count = sum(edge['node']['defaultBranchRef']['target']['history']['totalCount'] for edge in data)

    return repo_count, star_count, commit_count





def readmeoverwrite():
  url = 'https://api.github.com/graphql'
  repo_count, star_count, commit_count = getGitStats(token, url)

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
