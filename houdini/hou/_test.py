import os
from import_hou import import_hou


def main():
    """_summary_"""

    os.environ["HSITE"] = ""  # Empty `HSITE` environment variable

    houdini_version = "19.5.773"
    python_version = "3.9"

    import_hou(houdini_version, python_version)
    import hou

    print("Houdini version:", hou.applicationVersionString())


if __name__ == "__main__":
    main()
