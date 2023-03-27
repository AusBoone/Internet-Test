import ping3
import argparse
import sys
import time
import socket
import csv
import json
import statistics


def validate_host(host):
    """Validate the host argument."""
    try:
        addrinfo = socket.getaddrinfo(host, None)
        family = addrinfo[0][0]
    except socket.gaierror:
        print(f"Error: {host} is not a valid hostname or IP address.")
        sys.exit(1)

    return family


def ping(host, count=4, timeout=2, verbose=False, interval=1, family=socket.AF_INET, mode="icmp", data_size=56):
    """Ping a remote host to test network connectivity.

    Args:
        host (str): The hostname or IP address to ping.
        count (int): The number of packets to send. Default is 4.
        timeout (float): The maximum time to wait for a response. Default is 2.
        verbose (bool): Whether to print verbose output. Default is False.
        interval (float): The interval between pings when running continuously. Default is 1.
        family (int): The IP family to use. Default is AF_INET (IPv4).
        mode (str): The type of ping to use. Default is "icmp".
        data_size (int): The number of data bytes to be sent.

    Returns:
        A tuple containing the minimum, maximum, and average round-trip times (in milliseconds).
    """
    if mode == "icmp":
        ping_fn = ping3.ping
    elif mode == "tcp":
        ping_fn = ping3.tcp_ping
    elif mode == "udp":
        ping_fn = ping3.udp_ping
    else:
        print(f"Error: {mode} is not a valid ping mode.")
        sys.exit(1)

    while True:
        try:
            results = ping_fn(host, count=count, timeout=timeout, family=family, size=data_size)
        except (ping3.exceptions.ConnectionError, ping3.exceptions.TimeoutError):
            family = socket.AF_INET6 if family == socket.AF_INET else socket.AF_INET
            continue

        if results is not None:
            if verbose:
                print(f"Ping to {host} succeeded.")
                print(f"Minimum RTT: {results.min_rtt:.2f} ms")
                print(f"Maximum RTT: {results.max_rtt:.2f} ms")
                print(f"Average RTT: {results.avg_rtt:.2f} ms")
            else:
                print(f"Average RTT to {host}: {results.avg_rtt:.2f} ms")
            return (results.min_rtt, results.max_rtt, results.avg_rtt)
        else:
            print(f"Ping to {host} failed.")

        if count == 1:
            break

        time.sleep(interval)


def main():
    """Main function that parses command-line arguments and runs the ping function."""

    # Set up the command-line arguments
    parser = argparse.ArgumentParser(description="Ping a remote host to test network connectivity.")
    parser.add_argument("host", help="The hostname or IP address to ping.")
    parser.add_argument("-c", "--count", type=int, default=4, help="The number of packets to send.")
    parser.add_argument("-t", "--timeout", type=float, default=2, help="The maximum time to wait for a response.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output.")
    parser.add_argument("-i", "--interval", type=float, default=1, help="The interval between pings when running continuously.")
    parser.add_argument("--ipv6", action="store_true", help="Use IPv6 instead of IPv4.")
    parser.add_argument("-s", "--size", type=int, default=56, help="The number of data bytes to be sent.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet output. Nothing is displayed except the summary lines.")
    args = parser.parse_args()

    # Set the IP family based on the --ipv6 argument
    family = socket.AF_INET6 if args.ipv6 else socket.AF_INET

    # Ping the host and get the results
    try:
        min_rtt, max_rtt, avg_rtt = ping(args.host, count=args.count, timeout=args.timeout, verbose=args.verbose,
                                          interval=args.interval, family=family, data_size=args.size)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Print the summary
    packet_loss = ((args.count - len(avg_rtt)) / args.count) * 100
    print(f"\n--- {args.host} ping statistics ---")
    print(f"{args.count} packets transmitted, {len(avg_rtt)} packets received, {packet_loss:.1f}% packet loss")
    if len(avg_rtt) > 0:
        print(f"round-trip min/avg/max/stddev = {min(avg_rtt):.2f}/{sum(avg_rtt) / len(avg_rtt):.2f}/{max(avg_rtt):.2f}/{statistics.stdev(avg_rtt):.2f} ms")
    else:
        print("No response from host.")
        
    if args.quiet:
        # If quiet mode is enabled, only display the summary
        pass
    else:
        # Otherwise, display the detailed results
        for i, rtt in enumerate(avg_rtt):
            print(f"Reply from {args.host}: bytes={args.size} time={rtt:.2f} ms TTL=?")
        
        # Print the total time taken
        print(f"\nPing complete in {sum(avg_rtt):.2f} ms.")


if __name__ == '__main__':
    main()
