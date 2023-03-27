import ping3
import argparse
import sys
import time
import socket


def ping(host, count=4, timeout=2, verbose=False, interval=1):
    """Ping a remote host to test network connectivity.

    Args:
        host (str): The hostname or IP address to ping.
        count (int): The number of packets to send. Default is 4.
        timeout (float): The maximum time to wait for a response. Default is 2.
        verbose (bool): Whether to print verbose output. Default is False.
        interval (float): The interval between pings when running continuously. Default is 1.

    Returns:
        A tuple containing the minimum, maximum, and average round-trip times (in milliseconds).
    """
    
    # Test the network connectivity to the remote host
    family = socket.AF_INET  # Start with IPv4
    while True:
        try:
            # Attempt to ping the host using the current IP version
            results = ping3.ping(host, count=count, timeout=timeout, family=family)
        except (ping3.exceptions.ConnectionError, ping3.exceptions.TimeoutError):
            # If the ping fails, switch to the other IP version and try again
            family = socket.AF_INET6 if family == socket.AF_INET else socket.AF_INET
            continue
    
        # Print the ping results
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

        # If we're not running continuously, exit after the first ping
        if count == 1:
            break

        # Sleep for the specified interval before pinging again
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
    args = parser.parse_args()

    ping(args.host, count=args.count, timeout=args.timeout, verbose=args.verbose, interval=args.interval)


if __name__ == '__main__':
    main()
