import requests as r
import numpy as np
import pandas as pd
import re
import csv
from bs4 import BeautifulSoup


def write_to_file(list):
    with open('/Users/matthewschultz/PycharmProjects/AutoBot/training.csv', 'w') as csvfile:
        fieldnames = ['tag', 'validity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow({'tag': item[0], 'validity': item[1]})


def compare(dic, lis=[]):
    temp = {}
    for k in dic.keys():
        rule = re.match('[A-Za-z]', k)
        boolean = bool(rule)
        if k not in lis:
            if boolean is True:
                temp.update({k: 'yes'})
            else:
                temp.update({k: 'no'})
    final = []
    for k in temp:
        final.append([k, temp.get(k)])
    write_to_file(final)


def filter_for_training(dic):
    try:
        df = pd.read_csv('/Users/matthewschultz/PycharmProjects/AutoBot/training.csv')
        list1 = df.values.tolist()
        compare(dic, list1)
    except Exception:
        compare(dic)


def find_start(string):
    index = string.find('<')
    return index + 1


def find_end(string):
    if ' ' in string:
        index = string.find(' ')
    else:
        index = string.find('>')
    return index


def find_average(values):
    sum = 0
    total = len(values)
    for value in values:
        sum = sum + value
    return (sum / total) / 2


def clean_dict(dic):
    average = find_average(dic.values())
    temp = {}
    for k in dic.keys():
        rule = re.match('[A-Za-z]', k)
        boolean = bool(rule)
        if dic.get(k) >= average and boolean is True:
            temp.update({k: dic.get(k)})
    return temp


def preprocess(processed):
    lis = []
    for i in range(len(processed)):
        if processed[i] == '<':
            temp = []
            while processed[i] != '>' and i <= len(processed):
                temp.append(processed[i])
                if processed[i + 1] == '>':
                    temp.append(processed[i + 1])
                i = i + 1
            tag = "".join(temp).strip()
            if tag[1] == '/':
                continue
            else:
                lis.append(tag)
    return lis


def find_tag(lis):
    count = dict()
    for i in range(len(lis)):
        current = lis[i]
        start_index = find_start(current)
        end_index = find_end(current)
        tag = current[start_index:end_index]
        if tag in count.keys():
            count[tag] = count[tag] + 1
        else:
            count[tag] = 1
    return count


def data_clean(data):
    string = str(data.content)
    processed = string.strip().replace('\n', '')
    lis = preprocess(processed)
    count = find_tag(lis)
    cleaned_count = clean_dict(count)
    list_comp = [(key, value) for key, value in cleaned_count.items()]
    return list_comp


def save_and_analyze(request):
    cleaned_data = data_clean(request)
    array = np.array(cleaned_data)
    df = pd.DataFrame(array, columns=['tags', 'count'])
    return df


def soup(website):
    soup = BeautifulSoup(website, "html.parser")
    sum = soup.findChildren('div')
    lis = []
    for item in sum:
        lis.append(item.get_text())
    return lis


# used recursion because it ha a better time efficiency relative to using a loop
def handoff(links, i=0, websites=[]):
    print(i)
    if i >= len(links) - 30:
        return websites
    else:
        try:
            temp = r.get(links[i])
            website = temp.text
            data = soup(website)
            websites.append(data)
            return handoff(links, i + 1)
        except Exception as e:
            return handoff(links, i + 1)


# after doing some test the time to download some of these files depends about how populated the website is
# and the quality of the wifi connection so that it can make get request
