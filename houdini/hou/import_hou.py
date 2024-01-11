#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to import the Houdini `hou` module in a Python session, outside of Houdini."""

# Built-in
import os
import sys
from typing import Optional, Any


###### CODE ####################################################################


def import_hou(houdini_version: str = "20.0.547", python_version: str = "3.10") -> Optional[Any]:
    """Set up the environment so that `import hou` works in the current session.

    Args:
        houdini_version (str): The version of Houdini. Defaults to `20.0.547`.
        python_version (str): The version of Python. Defaults to `3.10`.

    Returns:
        ModuleType: The Houdini module (`hou`) if successfully imported.

    Raises:
        EnvironmentError: If the expected Python version doesn't match the
            running version.

    Example:
        >>> hou = enable_hou_module()
        >>> print(hou.applicationVersionString())
        Houdini version: 20.0.547

        >>> enable_hou_module()
        >>> import hou
        >>> print(hou.applicationVersionString())
        Houdini version: 20.0.547
    """

    # Check if the Python version matches the expected version. Do NOT take in
    # account the `patch` version (e.g. `3.10.0` is the same as `3.10.1`)
    major_version = sys.version_info[0]
    minor_version = sys.version_info[1]
    current_python_version = f"{major_version}.{minor_version}"

    if current_python_version != python_version:
        raise EnvironmentError(f"Expected Python version {python_version}, but got {current_python_version}")

    # Create `$HFS`
    hfs_path = os.path.join(
        os.getenv("PROGRAMFILES"),
        "Side Effects Software",
        f"Houdini {houdini_version}",
    ).replace(os.sep, "/")

    # Set up environment for `RTLD_GLOBAL`
    if hasattr(sys, "setdlopenflags"):
        old_dlopen_flags = sys.getdlopenflags()
        sys.setdlopenflags(old_dlopen_flags | os.RTLD_GLOBAL)

    # Add `%HFS%/bin` to the DLL search path (Windows only)
    sys.path.append(hfs_path)
    if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
        with os.add_dll_directory(os.path.join(hfs_path, "bin")):
            try:
                import hou  # type: ignore
            except ImportError:
                # If the `hou` module could not be imported, add Houdini-specific
                # path to `sys.path`
                hhp_path = os.path.join(hfs_path, "houdini", f"python{python_version}libs")
                os.environ["HHP"] = hhp_path
                sys.path.append(hhp_path)
                import hou  # type: ignore
            finally:
                # Reset `dlopen` flags if the attribute is available
                if hasattr(sys, "setdlopenflags"):
                    sys.setdlopenflags(old_dlopen_flags)

    return hou
