from nltk.tokenize import LineTokenizer


def strip_line(line):
    temp_lis = []
    for i in line:
        temp = i.strip().lower()
        temp_lis.append(temp)
    return temp_lis


def clean_out_line(corpus):
    structured_list = []
    for item in corpus:
        for line in item:
            new_line = LineTokenizer(blanklines='discard').tokenize(line)
            final = strip_line(new_line)
            structured_list.append(final)
    return structured_list


def remove_duplicates(filtered):
    found_lines = []
    for item in filtered:
        if item not in found_lines:
            found_lines.append(item)
    return found_lines


def container(webpages):
    cleaned = clean_out_line(webpages)
    remove_duplicates(cleaned)

