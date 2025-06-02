from jira import JIRA

jira = JIRA(
    server='https://angearenza.atlassian.net',
    basic_auth=('ton.email@domaine.com', 'TON_TOKEN_API')
)
