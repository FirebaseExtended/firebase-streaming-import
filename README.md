Firebase Streaming Import
===========================

- Utilizes ijson python json streaming library along with requests to import a large json piecemeal into Firebase.

- This is a **two-pass** script.  Run it once in normal mode to write all the data, then run it again in --priority-mode to write priority data.

- Defaults to 8-thread parallelization.  Tweak this argument for your own best performance.  

- Repeats efforts already done in [firebase-import](https://github.com/firebase/firebase-import), however firebase-import doesn't handle large json files well.  Node runs out of memory.  This script streams in data so there are no limits, however it might not be as fast or efficient as the other one.

- Root of tree does not need to be empty, since we make REST PATCH calls

- Speed: about 30 seconds/mb, for datasets with many small leaf values.  Performance improves when leaves have larger values.

Requirements: 
- run `pip install -r requirements.txt`
- May need to do `pip install pp --allow-unverified pp` in order to install the pp module

```
usage: import.py [-h] [-a AUTH] [-t THREADS] [-s] [-p] firebase_url json_file

Import a large json file into a Firebase via json Streaming. Uses HTTP PATCH
requests. Two-pass script, run once normally, then again in --priority_mode.

positional arguments:
  firebase_url          Specify the Firebase URL (e.g.
                        https://test.firebaseio.com/dest/path/).
  json_file             The JSON file to import.

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  Optional Auth token if necessary to write to Firebase.
  -t THREADS, --threads THREADS
                        Number of parallel threads to use, default 8.
  -s, --silent          Silences the server response, speeding up the
                        connection.
  -p, --priority_mode   Run this script in priority mode after running it in
                        normal mode to write all priority values.
```
