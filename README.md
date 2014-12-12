Firebase Streaming Import
===========================

Utilizes ijson python json streaming library along with requests to import a large json piecemeal into Firebase.

Requirements: 
- root of tree should be empty, since we make firebaseRef.update() calls
- run `pip install -r requirements.txt`

```
usage: import.py [-h] [-a AUTH] firebase_url json_file

Import a large json file into a Firebase via json Streaming.

positional arguments:
  firebase_url          Specify the Firebase URL (e.g.
                        https://test.firebaseio.com/dest/path).
  json_file             The JSON file to import.

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  Optional Auth token if necessary to write to Firebase.
```