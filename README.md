# chrome-to-firefox
A script to convert a WebExtension for Chrome to run on Firefox.

### Usage
Its default expected use is as a submodule in a chrome extension's repo.
Run without args to create a firefox-compatible ```.xpi``` archive of the parent directory's contents, named using keys
from the manifest.

You can also specify which directory to package, and the new values to add to the gecko part of the manifest.
Run with ```-h``` or ```--help``` for more information.

### Installation as submodule
The script ignores hidden directories; to avoid packing itself, best hide the submodule dir.
```git submodule add git@github.com:Steven-Eardley/chrome-to-firefox.git .build```
