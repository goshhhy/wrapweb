#!/usr/bin/env python3

# Copyright 2015 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, os, shutil
import tempfile, subprocess
from glob import glob
import zipfile


class UpstreamDefinition:
    def __init__(self, fname):
        self.values = {}
        ifile = open(fname)
        first = ifile.readline().strip()

        if first != '[wrap-file]':
            raise RuntimeError('Invalid format of package file')
        for line in ifile:
            line = line.split("#")[0]
            line = line.strip()
            if line == '':
                continue
            (k, v) = line.split('=', 1)
            k = k.strip()
            v = v.strip()
            self.values[k] = v
        for i in ['directory', 'source_url', 'source_filename', 'source_hash']:
            if i not in self.values:
                raise RuntimeError('Missing key %s from upstream wrap file.' % i)

    def __getattr__(self, attr):
        return self.values[attr]
    
class WrapCreator:
    def __init__(self, name, repo_url, branch):
        self.name = name
        self.repo_url = repo_url
        self.branch = branch
        self.out_dir = '.'

    def create(self):
        with tempfile.TemporaryDirectory() as workdir:
            subprocess.check_call(['git', 'clone', self.repo_url, workdir])
            subprocess.check_call(['git', 'checkout', self.branch], cwd=workdir)
            upstream_file = os.path.join(workdir, 'upstream.wrap')
            upstream_content = open(upstream_file).read()
            revision_str = subprocess.check_output(['git', 'describe'], cwd=workdir).decode('utf-8')
            revision_id = int(revision_str.split('-')[1])
            self.upstream_file = os.path.join(workdir, 'upstream.wrap')
            self.definition = UpstreamDefinition(self.upstream_file)
            shutil.rmtree(os.path.join(workdir, '.git'))
            os.unlink(os.path.join(workdir, 'readme.txt'))
            os.unlink(upstream_file)
            try:
                os.unlink(os.path.join(workdir, '.gitignore'))
            except FileNotFoundError:
                pass
            zip_name = self.name + '-' + self.branch + '-' + str(revision_id) + '.zip'
            zip = zipfile.ZipFile(os.path.join(self.out_dir, zip_name), 'w')
            for root, dirs, files in os.walk(workdir):
                for f in files:
                    abspath = os.path.join(root, f)
                    relpath = abspath[len(workdir)+1:]
                    zip.write(abspath, os.path.join(self.definition.directory, relpath))
            zip.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(sys.argv[0], '<project name> <data repo url> <branch>')
        sys.exit(1)
    x = WrapCreator(sys.argv[1], sys.argv[2], sys.argv[3])
    x.create()
