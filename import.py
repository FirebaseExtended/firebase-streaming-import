import ijson
import requests
import argparse
import json
import sys
import re
import traceback


def main(args):

    parser = ijson.parse(open(args.json_file))
    session = requests.Session()

    for prefix, event, value in parser:
        if value is not None and event != 'map_key':

            # ijson sends the prefix as a string of keys connected by periods,
            # but Firebase uses periods for special values such as priority.
            # 1. Find '..', and store the indexes of the second period
            doublePeriodIndexes = [m.start() + 1 for m in re.finditer('\.\.', prefix)]
            # 2. Replace all '.' with ' '
            prefix = prefix.replace('.', ' ')
            # 3. Use stored indexes of '..' to recreate second periods in the pairs of periods
            prefixList = list(prefix)
            for index in doublePeriodIndexes:
                prefixList[index] = '.'
            prefix = "".join(prefixList)
            # 4. Split on whitespace
            prefixes = prefix.split(' ')
            lastPrefix = prefixes[-1]
            prefixes = prefixes[:-1]

            url = args.firebase_url
            for prefix in prefixes:
                url += prefix + '/'
            url += '.json'
            if args.silent:
                url += '?print=silent'

            if event == 'number':
                dataObj = {lastPrefix: float(value)}
            else:
                dataObj = {lastPrefix: value}

            try:
                if args.auth is not None:
                    authObj = {'auth': args.auth}
                    session.patch(url, data=json.dumps(dataObj), params=authObj)
                else:
                    session.patch(url, data=json.dumps(dataObj))
            except Exception, e:
                print('Caught an error: ' + traceback.format_exc())
                print prefix, event, value

            sys.stdout.write('.')
            sys.stdout.flush()


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Import a large json file into a Firebase via json Streaming.  Uses HTTP PATCH requests.")
    argParser.add_argument('firebase_url', help="Specify the Firebase URL (e.g. https://test.firebaseio.com/dest/path/).")
    argParser.add_argument('json_file', help="The JSON file to import.")
    argParser.add_argument('-a', '--auth', help="Optional Auth token if necessary to write to Firebase.")
    argParser.add_argument('-s', '--silent', action='store_true', help="Silences the server response, speeding up the connection.")
    args = argParser.parse_args()
    main(args)
