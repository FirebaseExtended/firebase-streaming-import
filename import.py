import ijson
import requests
import argparse
import json
import sys
import re


def main(args):

    CHUNK_THRESHHOLD = args.chunk_size * 1024 * 1024

    parser = ijson.parse(open(args.json_file))
    session = requests.Session()

    # for beginning/ending braces
    currentObjSize = 2
    rootObj = {}

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
            keys = prefix.split(' ')

            currObj = rootObj
            for key in keys[:-1]:
                if key in currObj:
                    currObj = currObj[key]
                    # Don't count the key size twice, but add a comma
                    currentObjSize += 1
                else:
                    newObj = {}
                    currObj[key] = newObj
                    currObj = newObj
                    # For size of key, quotes around key, colon, braces
                    currentObjSize += len(key) + 2 + 1 + 2

            if event == 'number':
                leafValue = float(value)
            else:
                leafValue = value
                # For quotes around string based leaf
                currentObjSize += 2
            currObj[keys[-1]] = leafValue
            # For size of final key, quotes, colon
            currentObjSize += len(keys[-1]) + 2 + 1
            # For size of leaf value
            currentObjSize += len(str(value))

            if currentObjSize > CHUNK_THRESHHOLD:
                patchToFirebase(rootObj, args, session)
                rootObj = {}
                currentObjSize = 2

    if bool(rootObj):
        patchToFirebase(rootObj, args, session)


def patchToFirebase(dataObj, args, session):
    restURL = args.firebase_url + '/.json'
    if args.silent:
        restURL += '?print=silent'
    if args.auth is not None:
        authObj = {'auth': args.auth}
        r = session.patch(restURL, data=json.dumps(dataObj), params=authObj)
    else:
        r = session.patch(restURL, data=json.dumps(dataObj))
    if not args.silent:
        print r.text
    else:
        sys.stdout.write('.')
        sys.stdout.flush()


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Import a large json file into a Firebase via json Streaming.  Uses HTTP PATCH requests.")
    argParser.add_argument('firebase_url', help="Specify the Firebase URL (e.g. https://test.firebaseio.com/dest/path/).")
    argParser.add_argument('json_file', help="The JSON file to import.")
    argParser.add_argument('-a', '--auth', help="Optional Auth token if necessary to write to Firebase.")
    argParser.add_argument('-s', '--silent', action='store_true', help="Silences the server response, speeding up the connection.")
    argParser.add_argument('-c', '--chunk_size', default=1, type=int, help="Chunk size in Megabytes, defaults to 1MB.")
    args = argParser.parse_args()
    main(args)
