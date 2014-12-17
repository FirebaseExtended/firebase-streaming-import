import ijson
import requests
import argparse
import json
import sys


def main(args):

    parser = ijson.parse(open(args.json_file))

    rootObj = {}
    for prefix, event, value in parser:
        if value is not None and event != 'map_key':

            if event == 'number':
                leafValue = float(value)
            else:
                leafValue = value

            prefixes = prefix.split('.')

            currObj = rootObj
            for prefix in prefixes[:-1]:
                if prefix in currObj:
                    currObj = currObj[prefix]
                else:
                    newObj = {}
                    currObj[prefix] = newObj
                    currObj = newObj
            currObj[prefixes[-1]] = leafValue

    patchToFirebase(rootObj, args)


def patchToFirebase(dataObj, args):
    restURL = args.firebase_url + '.json?print=silent'
    if args.auth is not None:
        authObj = {'auth': args.auth}
        requests.patch(restURL, data=json.dumps(dataObj), params=authObj)
    else:
        requests.patch(restURL, data=json.dumps(dataObj))
    sys.stdout.write('.')
    sys.stdout.flush()


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Import a large json file into a Firebase via json Streaming.")
    argParser.add_argument('firebase_url', help="Specify the Firebase URL (e.g. https://test.firebaseio.com/dest/path).")
    argParser.add_argument('json_file', help="The JSON file to import.")
    argParser.add_argument('-a', '--auth', help="Optional Auth token if necessary to write to Firebase.")
    args = argParser.parse_args()
    main(args)
