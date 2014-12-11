Firebase Streaming Importer
===========================

Utilizes Oboe JSON streaming library combined with the Firebase JS Client to import large JSON files to an online Firebase.  

Requirements: 
- root of tree should be empty, since we make firebaseRef.update() calls
- security rules should allow write access (you can turn this off after the import completes)
- run npm install

Usage: node ./import.js

Options:
  --firebase_url  Firebase URL (e.g. https://test.firebaseio.com/dest/path).  [required]
  --json          The JSON file to import.                                    [required]