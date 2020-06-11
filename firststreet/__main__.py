import argparse
import os
import sys

import firststreet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description for my parser")
    parser.add_argument("-p", "--product", help="Example: adaptation_detail", required=True, default="")
    parser.add_argument("-i", "--fsids", help="Example: 28,29", required=False, default="")
    parser.add_argument("-l", "--location", help="Example: property", required=False, default="")
    parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False, default="")

    argument = parser.parse_args()

    fsids = []
    if argument.fsids:
        fsids += list(map(int, argument.fsids.strip().split(",")))

    if argument.file:
        with open("..\\" + argument.file) as fp:
            for line in fp:
                fsids.append(int(line.rstrip('\n')))

    if argument.product:

        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)

        if argument.product == 'adaptation.get_detail':
            fs.adaptation.get_detail(fsids, csv=True)

        elif argument.product == 'adaptation.get_summary':
            fs.adaptation.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'probability.get_depth':
            fs.probability.get_depth(fsids, csv=True)

        elif argument.product == 'probability.get_chance':
            fs.probability.get_chance(fsids, csv=True)

        elif argument.product == 'probability.get_count_summary':
            fs.probability.get_count_summary(fsids, csv=True)

        elif argument.product == 'probability.get_cumulative':
            fs.probability.get_cumulative(fsids, csv=True)

        elif argument.product == 'probability.get_count':
            fs.probability.get_count(fsids, argument.location, csv=True)

        elif argument.product == 'historic.get_event':
            fs.historic.get_event(fsids, csv=True)

        elif argument.product == 'historic.get_summary':
            fs.historic.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'location.get_detail':
            fs.location.get_detail(fsids, argument.location, csv=True)

        elif argument.product == 'location.get_summary':
            fs.location.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'fema.get_nfip':
            fs.fema.get_nfip(fsids, argument.location, csv=True)

        elif argument.product == 'environmental.get_precipitation':
            fs.environmental.get_precipitation(fsids, csv=True)

        else:
            print("Product not found")
