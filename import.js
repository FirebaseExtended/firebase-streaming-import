var oboe = require('oboe');
var fs = require('fs');
var Firebase = require("firebase");


var argv = require('optimist')
  .usage('Usage: $0')
  .demand('firebase_url')
  .describe('firebase_url', 'Firebase URL (e.g. https://test.firebaseio.com/dest/path).')
  .alias('f', 'firebase_url')
  .demand('json')
  .describe('json', 'The JSON file to import.')
  .alias('j', 'json')
  .argv;

var firebaseRootRef = new Firebase(argv.firebase_url)

oboe(fs.createReadStream(argv.json))
  .node('*', function(jsonLeaf, path) {
    var nodePath = firebaseRootRef;
    for (i = 0; i < path.length; i++) { 
        nodePath = nodePath.child(path[i]);
    }
    nodePath.update(jsonLeaf);
    return oboe.drop;
  })
  .done(function(things) {
    console.log("we're all done, should return an empty json object below:");
    console.log(things);
  });