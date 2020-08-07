#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""file test functions.
"""
from .contents import get_content, contain, load  # noqa: F401
from .files import (  # noqa: F401
    is_file, exist, exists, is_directory, is_block_device, is_character_deivce,
    is_pipe, is_socket, is_symlink, is_owned_by, is_grouped_into, is_linked_to
)
from .mount import is_mounted  # noqa: F401
from .permission import (  # noqa: F401
    has_mode, is_readable, is_writable, is_executable, is_immutable
)
from .selinux_ import has_selinux_label  # noqa: F401
from .stat import (  # noqa: F401
    get_checksum, has_checksum, get_size, has_size
)

# vim:sw=4:ts=4:et:
