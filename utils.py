import psutil


def get_network_usage() -> tuple[int, int]:
    net_io = psutil.net_io_counters()

    return net_io.bytes_sent, net_io.bytes_recv
