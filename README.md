# bump
Increment version numbers in source files

__WARNING__: This tool is experimental and does some file manipulation, use at your own risk.

## Install

You'll need Python 3, `pip`.

As superuser do:
```
pip install PyYAML semantic-version schema # install python dependencies
mkdir /opt/bump/ # or wherever you want
wget https://raw.githubusercontent.com/fredshonorio/bump/master/bump.py -O /opt/bump/bump.py
chmod +x /opt/bump/bump.py
ln -s /opt/bump/bump.py /usr/local/bin/bump # you can also call it something else
```

Run `bump` (or whatever else you called it) and you should get some output.

## Use

### Files

### Execute before/after

## TODO
- Handle semantic version/build labels
- More error handling
- Add some tests
- Add example projects
