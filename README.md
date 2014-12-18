Firebase Streaming Import
===========================

CONTAINS BUG DO NOT USE
=======================

This repo was intended as a streaming method of importing large Firebases.  It was not fast enough(took days for an 800MB Firebase), so it was modified to send 1MB patch requests containing a swiss-cheese part of the root object.  However, doing a PATCH and sending the entire object overwrites other parts of the object, so this script is broken.  Its slower form which was present a few commits back was too slow to be of any use.  The suggested restore method for large Firebases is https://docs.google.com/document/d/1n1EBFqLku8895qj-dl-PdOHK1QkGBUpmCvPef3nnddY/edit

Utilizes ijson python json streaming library along with requests to import a large json piecemeal into Firebase.

Repeats efforts already done in [firebase-import](https://github.com/firebase/firebase-import), however firebase-import doesn't handle large json files well.  Node runs out of memory.  This script streams in data so there are no limits, however it might not be as fast or efficient as the other one.

Requirements: 
- root of tree should be empty, since we make REST PATCH calls
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
