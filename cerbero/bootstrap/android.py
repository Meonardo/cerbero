# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import shutil

from cerbero.bootstrap import BootstrapperBase
from cerbero.bootstrap.bootstrapper import register_toolchain_bootstrapper
from cerbero.config import Distro, FatalError
from cerbero.utils import _, shell

# NDK_VERSION = 'r21'
# NDK_BASE_URL = 'https://dl.google.com/android/repository/android-ndk-%s-%s-%s.zip'
NDK_VERSION = 'r25c'
NDK_BASE_URL = 'https://dl.google.com/android/repository/android-ndk-%s-%s.zip'
NDK_CHECKSUMS = {
    # 'android-ndk-r21-linux-x86_64.zip': 'b65ea2d5c5b68fb603626adcbcea6e4d12c68eb8a73e373bbb9d23c252fc647b',
    # 'android-ndk-r21-darwin-x86_64.zip': 'b82a49ec591d6f283acc7a241a8c56a14788320bf85a3375b5f2309b3b0c9b45',
    # 'android-ndk-r21-windows-x86_64.zip': 'faf5a09f78dc7b350b2b77e71031d039191f2af66ac7c99494cd7d5a65e8d147',
    'android-ndk-r25c-linux.zip': '769ee342ea75f80619d985c2da990c48b3d8eaf45f48783a2d48870d04b46108',
    # doesn't ship as a zip file anymore
    'android-ndk-r25c-darwin.dmg': '1856108efde22d502399216c65e2a0f7823bdfac1df69fe6a1f3b71ff7be6ced',
    'android-ndk-r25c-windows.zip': 'f70093964f6cbbe19268f9876a20f92d3a593db3ad2037baadd25fd8d71e84e2',

}

class AndroidBootstrapper (BootstrapperBase):

    def __init__(self, config, offline, assume_yes):
        super().__init__(config, offline)
        self.prefix = self.config.toolchain_prefix
        # url = NDK_BASE_URL % (NDK_VERSION, self.config.platform, self.config.arch)
        url = NDK_BASE_URL % (NDK_VERSION, self.config.platform)
        self.fetch_urls.append((url, None, NDK_CHECKSUMS[os.path.basename(url)]))
        self.extract_steps.append((url, True, self.prefix))

    async def start(self, jobs=0):
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)
        ndkdir = os.path.join(self.prefix, 'android-ndk-' + NDK_VERSION)
        if not os.path.isdir(ndkdir):
            return
        # Android NDK extracts to android-ndk-$NDK_VERSION, so move its
        # contents to self.prefix
        for d in os.listdir(ndkdir):
            dest = os.path.join(self.prefix, d)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(os.path.join(ndkdir, d), self.prefix)
        os.rmdir(ndkdir)


def register_all():
    register_toolchain_bootstrapper(Distro.ANDROID, AndroidBootstrapper)
