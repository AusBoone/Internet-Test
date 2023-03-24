import speedtest

# Create a speedtest-cli object
st = speedtest.Speedtest()

# Perform a speed test and get the results
download_speed = st.download() / 1000000
upload_speed = st.upload() / 1000000

# Print the results
print(f"Download speed: {download_speed:.2f} Mbps")
print(f"Upload speed: {upload_speed:.2f} Mbps")
