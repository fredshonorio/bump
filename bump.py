#!/usr/bin/env python3

_VERSION = "0.0.1"

import sys, os, re, time
from collections import namedtuple
from operator import attrgetter as get, eq
from functools import partial
from shutil import copyfile
from subprocess import call

import yaml
from semantic_version import Version as semver
from schema import Schema, And, Use, Optional

CFG = ".bump.yml"
SCHEMA = Schema({"files": [{"path": str, "pattern": str}], "exec_after":[str], "exec_before":[str]})

class BumpError(Exception): pass
class BumpExit(Exception): pass

File = namedtuple("File", ["path", "pattern"])

def epoch_now(): return int(time.time())
def flatten(l): return [i for sub in l for i in sub]

def die(msg, *args): print(msg, *args, file=sys.stderr); raise BumpError()
def exit(msg, *args): print(msg, *args, file=sys.stderr); raise BumpExit()

def read_conf():
    with open(CFG, "r") as f:
        r = yaml.load(f)
    SCHEMA.validate(r)
    assert r["files"]
    return [File(f["path"], f["pattern"]) for f in r["files"]], r["exec_before"], r["exec_after"]

def get_versions(file_lines, pattern): # returns a list of versions using the patterns for a single file
    return list(
        map(lambda r: r.group(1), # get the version from the line
        filter(bool, # ignore lines that don't match
        map(lambda l: re.search(pattern, l), # find version with pattern
        file_lines)))) # read file as line iterator

def check_versions(vs): # checks if all the versions are the same
    x = set(vs)
    assert len(x) == 1, "Multiple or no versions detected"
    return x.pop()

def write_lines(f, lines):
    with open(f, "wt") as ff:
        ff.writelines(lines)

def read_lines(f):
    with open(f, "rt") as ff:
        return ff.readlines()

def update_matching(pred, update): # replaces an item if it matches a predicate
    return lambda i: update(i) if pred(i) else i

def replace_first_with(pattern, sub): # replaces the first regex group with the given substitute
    def f(line):
        m = re.search(pattern, line)
        return line[:m.start(1)] + sub + line[m.end(1):]
    return f

def get_increment(args):
    first_is = lambda ss: any(map(partial(eq, args[0]), ss)) if len(args) >= 1 else False

    if not args or first_is(["p", "pat", "patch"]):
         return lambda s: s.next_patch()
    if first_is(["mi", "min", "minor"]):
        return lambda s: s.next_minor()
    if first_is(["ma", "maj", "major"]):
        return lambda s: s.next_major()
    if first_is(["n", "noop", "none"]):
        return lambda s: s

    raise ValueError("Unknown update %s" % args)

def exec_many(cmds, t_vars): # execute commands passing template vars
    for raw_cmd in cmds:
        cmd = raw_cmd.format(**t_vars)

        ans = input("Execute '{}'? [Y/n]".format(cmd))
        if not ans or ans.lower() == "y":
            # TODO: print output when return code is no 0
            if call(cmd, shell=True) != 0:
                die("Failed command '%s'" % cmd)
        else:
            quit("Aborting.")

def main(args):
    incr = get_increment(args)

    if (not os.path.isfile(CFG)):
        exit("No config file found, nothing to do.")

    files, pre_cmds, post_cmds = read_conf()

    files_paths = list(map(get("path"), files))
    files_patterns = list(map(get("pattern"), files))
    files_lines = list(map(read_lines, files_paths))

    # check if versions are unique
    versions = flatten(map(get_versions, files_lines, files_patterns))
    current = check_versions(versions)

    newver = str(incr(semver(current)))

    if current == newver:
        exit("Nothing to do.")

    print("Bumping to version %s" % newver)

    t_vars = {"oldv": current, "newv": newver, "files": " ".join(files_paths)}

    exec_many(pre_cmds, t_vars)

    for pattern, lines, path in zip(files_patterns, files_lines, files_paths):
        splice_new_version = replace_first_with(pattern, newver)
        is_version_line = partial(re.search, pattern)
        new_lines = map(update_matching(is_version_line, splice_new_version), lines)

        copyfile(path, "%s.%d.bkp" % (path, epoch_now()))
        write_lines(path, new_lines)

    exec_many(post_cmds, t_vars)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except BumpError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborting.")
        sys.exit(1)
    except BumpExit:
        pass
