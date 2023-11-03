import psutil


def get_network_usage() -> tuple[int, int]:
    """Return current number of bytes sent & recived

    Returns
    -------
    Tuple of two inteagers
        (number of bytes sent, number of bytes recived)"""

    net_io = psutil.net_io_counters()

    return net_io.bytes_sent, net_io.bytes_recv


def convert_bytes(size_in_bytes: int) -> str:
    """Convert bytes to a human-readable format."""

    for x in ["bytes", "Kb", "Mb", "Gb", "Tb"]:
        if size_in_bytes < 1024.0:
            return "%3.1f %s" % (size_in_bytes, x)
        size_in_bytes /= 1024.0

    return "%3.1f %s" % (size_in_bytes, "Tb")
