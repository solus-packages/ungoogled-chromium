#!/usr/bin/python3

import os
import sys
import shutil

sys.path.append("build/linux/unbundle")

import replace_gn_files

def strip(path):
    if os.path.exists(path):
        for filename in os.listdir(path):
            remove = True
            for extension in ('.py','.gn','.gni','google','chromium'):
                if filename.endswith(extension):
                    remove = False
            if remove:
                removal=os.path.join(path,filename)
                print('removing: %s'%removal)
                if os.path.isdir(removal):
                    shutil.rmtree(removal)
                else:
                    os.remove(removal)

keepers = ('openh264','libjpeg','flot','ffmpeg')

# Awkward buggers
strip('third_party/libjpeg_turbo')
#strip('base/third_party/libevent')

for lib,rule in replace_gn_files.REPLACEMENTS.items():
    if lib not in keepers:
        libdir = os.path.join('third_party',lib)
        if os.path.exists(libdir):
            # remove conflicting embedded third party source files
            strip(libdir)
            strip(os.path.dirname(rule))
            # remove the gn file that builds the embedded library
            if os.path.lexists(rule):
                print('removing: %s'%rule)
                os.remove(rule)
        else:
            # otherwise, create the missing directory
            os.mkdir(libdir)
        # create a symlink to the unbundle gn file
        symlink = "ln -s "
        path = os.path.split(rule)
        while path[0] != '':
            path = os.path.split(path[0])
            symlink += '../'
        symlink += "build/linux/unbundle/%s.gn %s"%(lib,rule)
        if os.system(symlink):
            raise RuntimeError("error creating symlink",symlink)
