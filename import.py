import ijson
import requests
import argparse
import json
import sys


def main(args):

    parser = ijson.parse(open(args.json_file))
    for prefix, event, value in parser:
        if value is not None and event != 'map_key':

            prefixes = prefix.split('.')
            newURL = args.firebase_url
            lastPrefix = prefixes[-1]
            prefixes = prefixes[:-1]
            for prefix in prefixes:
                newURL += prefix + '/'
            newURL += '.json?print=silent'

            if event == 'number':
                dataObj = {lastPrefix: int(value)}
            else:
                dataObj = {lastPrefix: value}
            if args.auth is not None:
                authObj = {'auth': args.auth}
                requests.patch(newURL, data=json.dumps(dataObj), params=authObj)
            else:
                requests.patch(newURL, data=json.dumps(dataObj))

            sys.stdout.write('.')
            sys.stdout.flush()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Import a large json file into a Firebase via json Streaming.")
    argParser.add_argument('firebase_url', help="Specify the Firebase URL (e.g. https://test.firebaseio.com/dest/path).")
    argParser.add_argument('json_file', help="The JSON file to import.")
    argParser.add_argument('-a', '--auth', help="Optional Auth token if necessary to write to Firebase.")
    args = argParser.parse_args()
    main(args)
