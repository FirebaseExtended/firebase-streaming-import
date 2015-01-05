Firebase Streaming Import
===========================

Utilizes ijson python json streaming library along with requests to import a large json piecemeal into Firebase.

This is a **two-pass** script.  Run it once in normal mode to write all the data, then run it again in --priority-mode to write priority data.

Repeats efforts already done in [firebase-import](https://github.com/firebase/firebase-import), however firebase-import doesn't handle large json files well.  Node runs out of memory.  This script streams in data so there are no limits, however it might not be as fast or efficient as the other one.

Requirements: 
- root of tree should be empty, since we make REST PATCH calls
- run `pip install -r requirements.txt`

```
usage: import.py [-h] [-a AUTH] [-s] [-p] firebase_url json_file

Import a large json file into a Firebase via json Streaming. Uses HTTP PATCH
requests. Two-pass script, run once normally, then again in --priority-mode.

positional arguments:
  firebase_url          Specify the Firebase URL (e.g.
                        https://test.firebaseio.com/dest/path/).
  json_file             The JSON file to import.

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  Optional Auth token if necessary to write to Firebase.
  -s, --silent          Silences the server response, speeding up the
                        connection.
  -p, --priority_mode   Run this script in priority mode after running it in
                        normal mode to write all priority values.
```
