"""Provide platform specific settings for the nv_typewriter plugin.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_typewriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvtypewriter.platform.generic_keys import GenericKeys
from nvtypewriter.platform.mac_keys import MacKeys
from nvtypewriter.platform.windows_keys import WindowsKeys

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
else:
    PLATFORM = ''
    KEYS = GenericKeys()

