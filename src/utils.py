import re


def try_float(x: str) -> float:
    try:
        return float(x)
    except:
        return 0


def extract_zoom_from_filename(filename: str) -> str | None:
    """
    Extracts the zoom level from a filename. The zoom level is assumed to be in the format 'Nx' where N is a number,
    and it can be located at the beginning or end of the filename.

    :param filename: The filename to extract the zoom level from.
    :return: The zoom level if found, otherwise None.
    """
    zoom_pattern = re.compile(r"\b(\d+x)\b")

    match = zoom_pattern.search(filename)
    zoom_level = match.group(1) if match else None

    return zoom_level
