"""Provide platform specific settings for the nv_writer plugin.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvwriter.platform.generic_keys import GenericKeys
from nvwriter.platform.linux_keys import LinuxKeys
from nvwriter.platform.mac_keys import MacKeys
from nvwriter.platform.windows_keys import WindowsKeys

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = LinuxKeys()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
else:
    PLATFORM = ''
    KEYS = GenericKeys()

