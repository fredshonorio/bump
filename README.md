# bump
Increment version numbers in source files

_TODO_: better description

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

## Configure

`bump` expects a file with the name `.bump.yml` in a project's directory. This file must
be a valid YAML file.
An example follows:
```
files:
  - path: README.md
    pattern: "VERSION (.*)"
  - path: somefile
    pattern: "v: (.*)"
exec_before: []
exec_after:
  - "echo Now at version {newv}!"
```

`files` is a list of files that contain a version number which you want to
increment. `pattern` must be a regexp with a single group, the contents of that
group will me modified.
`exec_before` and `exec_after` are lists of shell commands to be executed before
and after writing the new versions to the files. You can use this to automate
your release workflow, e.g. doing a `git flow release start` before and
`git flow release finish` after, appending to a changelog).

The strings are python 3 [templates](https://docs.python.org/3.1/library/string.html#formatspec) and can have the following arguments:
- `oldv` - the previous version
- `newv` - the new version after the bump
- `files` - a space separated list of the paths listed in `files`, for the example above it's the string `README.md somefile`

## Use

First, ensure all versions are a valid [semantic version](http://semver.org/), and that they are all the same across files.

Then simply run `bump <version part>` where `version part` is one of:
- `ma`, `maj`, `major` - to increment the major version: `1.0.0` to `2.0.0`
- `mi`, `min`, `minor` - to increment the minor version: `1.0.0` to `1.1.0`
- `p`, `pat`, `patch` - to increment the patch version: `1.0.0` to `1.0.1`
- `n`, `noop`, `none` - to do nothing.

You should see your files updated and a copy of the previous version.

## Examples

--

## TODO
- Add usage, `--help`
- Handle semantic version/build labels
- More error handling, edge cases
- Add some tests
- Add example projects, use cases

## License

Licensed under [the Unlicense](http://unlicense.org/)
