#!/usr/bin/env python3


import requests
import argparse


parser = argparse.ArgumentParser(description="List all repositories and tags in the docker registry")
parser.add_argument('--url', type=str, default='https://10.0.0.161:5000', help='Docker registry URL')
args = parser.parse_args()


class str_obj:
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

    def __self__(self):
        return self.value


def show(data):
    result = []
    equals = str_obj('=')
    dashes = str_obj('-')

    result.append(equals)
    result.append('Registry URL: {}'.format(args.url))
    result.append('{}:{}'.format('Repository', 'Tags'))
    result.append(equals)
    repos = sorted(data.keys())
    for repo in repos:
        tags = sorted(data[repo])
        first_tag = True
        for tag in tags:
            result.append('{}:{}'.format(repo, tag))
        result.append(dashes)
    result.append(equals)

    max_len = 0
    for r in result:
        if len(r) > max_len:
            max_len = len(r)

    equals.value = max_len * '='
    dashes.value = max_len * '-'

    output = '\n'.join(map(str, result))
    print(output)


def list_all():

    requests.urllib3.disable_warnings()
    data = {}

    url = args.url + '/v2/_catalog'
    response = requests.get(url, verify=False)
    repos = response.json()['repositories']
    for repo in repos:
        url = args.url + '/v2/{}/tags/list'.format(repo)
        response = requests.get(url, verify=False)
        response_json = response.json()
        if 'errors' not in response_json:
            tags = response_json['tags']
            data[repo] = tags

    show(data)

if __name__ == '__main__':
    list_all()

