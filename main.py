import argparse
import urllib.request
import csv
import io
import re


def downloadData(url):
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    return response


def process_url(data):
    image_hits = 0

    browser_dict = {
        'IE': 0,
        'Safari': 0,
        'Chrome': 0,
        'Firefox': 0
    }

    csv_data = csv.reader(io.StringIO(data))
    for i, row in enumerate(csv_data):
        path_to_file = row[0]
        browser = row[2]

        if re.search("gif|jpg", path_to_file.lower()):
            image_hits += 1
        if re.search("Chrome", browser):
            browser_dict['Chrome'] += 1
        elif re.search("Firefox", browser):
            browser_dict['Firefox'] += 1
        elif re.search("Safari", browser) and not re.search("Chrome", browser):
            browser_dict['Safari'] += 1

    image_cal = image_hits / (i + 1) * 100
    top_browsed = [max(b for b in browser_dict.items())]
    resultname = top_browsed[0][0]
    resultnum = top_browsed[0][1]

    report = ("There's a total of {} page hits today.\n"
              "Images account for {} % percent of all requests.\n"
              "{} is browser top used with {} hits.").format(image_hits,
                                                             image_cal,
                                                             resultname,
                                                             resultnum)
    print(report)


def main(url):
    data = downloadData(url)
    process_url(data)
    # print(data)


if __name__ == "__main__":
    url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"
    my_parser = argparse.ArgumentParser(description='Assignment2 Parser')
    my_parser.add_argument('--url', type=str, required=True, help='The URL we want to download')
    args = my_parser.parse_args()
    main(url)
