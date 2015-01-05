import ijson
import requests
import argparse
import json
import sys
import re
import traceback
import pp
import time


def main(args):
    print("started at {0}".format(time.time()))

    parser = ijson.parse(open(args.json_file))
    session = requests.Session()
    parallelJobs = pp.Server()
    parallelJobs.set_ncpus(args.threads)

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

            if not args.priority_mode:
                if lastPrefix == '.priority':
                    continue
            else:
                if lastPrefix != '.priority':
                    continue

            if event == 'number':
                dataObj = {lastPrefix: float(value)}
            else:
                dataObj = {lastPrefix: value}

            try:
                parallelJobs.submit(sendData, (url, dataObj, session, args), (), ("json", "requests"))
            except Exception, e:
                print('Caught an error: ' + traceback.format_exc())
                print prefix, event, value

    # If we don't wait for all jobs to finish, the script will end and kill all still open threads
    parallelJobs.wait()
    print("finished at {0}".format(time.time()))


def sendData(url, dataObject, session, args):
    if args.auth is not None:
        authObj = {'auth': args.auth}
        session.patch(url, data=json.dumps(dataObject), params=authObj)
    else:
        session.patch(url, data=json.dumps(dataObject))


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Import a large json file into a Firebase via json Streaming.\
                                                     Uses HTTP PATCH requests.  Two-pass script, run once normally,\
                                                     then again in --priority_mode.")
    argParser.add_argument('firebase_url', help="Specify the Firebase URL (e.g. https://test.firebaseio.com/dest/path/).")
    argParser.add_argument('json_file', help="The JSON file to import.")
    argParser.add_argument('-a', '--auth', help="Optional Auth token if necessary to write to Firebase.")
    argParser.add_argument('-t', '--threads', type=int, default=8, help='Number of parallel threads to use, default 8.')
    argParser.add_argument('-s', '--silent', action='store_true',
                           help="Silences the server response, speeding up the connection.")
    argParser.add_argument('-p', '--priority_mode', action='store_true',
                           help='Run this script in priority mode after running it in normal mode to write all priority values.')

    main(argParser.parse_args())
