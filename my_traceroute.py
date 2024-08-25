from scapy.all import IP, ICMP, sr1
import time
import sys

i = 1
dst_site = sys.argv[1]
while True:
    start_time = time.time()  # Record the start time
    packet_send = IP(dst=dst_site, ttl=i) / ICMP()
    try:
        packet_replay = sr1(packet_send,timeout=2)
    except Exception as e:
        print("request failed",e)
    if packet_replay is None:
        print("none")
    else:
        print("the", i, "router is: " + packet_replay.src, "\r\n")
    i += 1
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
