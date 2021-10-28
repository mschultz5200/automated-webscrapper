import requests as r
import numpy as np
import pandas as pd
import re
import csv
from selenium import webdriver


def write_to_file(list):
    print('yo')
    with open('/Users/matthewschultz/PycharmProjects/testsplit/training.csv', 'w') as csvfile:
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
        df = pd.read_csv('/Users/matthewschultz/PycharmProjects/testsplit/training.csv')
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


def clean_dict(dic):
    temp = {}
    for k in dic.keys():
        if dic.get(k) != 1:
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


def save_and_analyze(request):
    string = str(request.content)
    processed = string.strip().replace('\n', '')
    lis = preprocess(processed)
    count = find_tag(lis)
    cleaned_count = clean_dict(count)
    filter_for_training(cleaned_count)
    list_comp = [(key, value) for key, value in cleaned_count.items()]
    array = np.array(list_comp)
    df = pd.DataFrame(array, columns=['tags', 'count'])
    print(df)


def links(request):
    PATH = "/Users/matthewschultz/Desktop/CD/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get(request)
    links = []
    elems = driver.find_elements_by_tag_name('a')
    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None:
            links.append(href)
    driver.quit()


def handoff(url):
    request = r.get(url)
    links(url)
    save_and_analyze(request)
