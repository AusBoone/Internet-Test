import java.net.InetAddress;
import java.net.UnknownHostException;
import java.io.IOException;

/**
 * A simple Java program to ping a remote host to test network connectivity.
 */
public class Ping {

    public static void main(String[] args) {
        String host = args[0];
        int count = 4;
        float timeout = 2;
        boolean verbose = false;
        float interval = 1;
        
        // Parse command-line arguments
        for (int i = 1; i < args.length; i++) {
            if (args[i].equals("-c")) {
                // Set the number of packets to send
                count = Integer.parseInt(args[i+1]);
            } else if (args[i].equals("-t")) {
                // Set the maximum time to wait for a response
                timeout = Float.parseFloat(args[i+1]);
            } else if (args[i].equals("-v")) {
                // Set verbose output mode
                verbose = true;
            } else if (args[i].equals("-i")) {
                // Set the interval between pings
                interval = Float.parseFloat(args[i+1]);
            }
        }
        
        // Test the network connectivity to the remote host
        InetAddress address;
        try {
            // Get the IP address of the host
            address = InetAddress.getByName(host);
        } catch (UnknownHostException e) {
            // If the host is unknown, print an error message and exit
            System.err.println("Error: Unknown host " + host);
            return;
        }
        for (int i = 0; i < count; i++) {
            try {
                // Ping the host and measure the RTT
                long start = System.currentTimeMillis();
                boolean reachable = address.isReachable((int) (timeout * 1000));
                long end = System.currentTimeMillis();
                long rtt = end - start;
                if (reachable) {
                    if (verbose) {
                        // Print detailed ping results
                        System.out.println("Ping to " + host + " succeeded.");
                        System.out.println("RTT: " + rtt + " ms");
                    } else {
                        // Print only the average RTT
                        System.out.println("RTT to " + host + ": " + rtt + " ms");
                    }
                } else {
                    // If the ping fails, print an error message
                    System.out.println("Ping to " + host + " failed.");
                }
            } catch (IOException e) {
                // If an I/O error occurs, print an error message and exit
                System.err.println("Error: " + e.getMessage());
                return;
            }
            if (i < count - 1) {
                try {
                    // Wait for the specified interval before pinging again
                    Thread.sleep((int) (interval * 1000));
                } catch (InterruptedException e) {
                    // Ignore the exception and continue
                }
            }
        }
    }
}
