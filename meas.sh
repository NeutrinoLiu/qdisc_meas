# check sudo 
label=$(date +%T)
echo "sudo okay, current time: $label"

# run tcpdump
tcpdump "port 5001"  > raw/tcpdump.txt &

# run tcpprob
#   clean up trace
echo > /sys/kernel/debug/tracing/trace
#   enable trace
echo 1 > /sys/kernel/debug/tracing/events/tcp/tcp_probe/enable

# run iperf3
iperf3 -c speedtestrh.telecom.mu -p 5201 --cport 5001

# wait for end of iperf3

# disable trace
echo 0 > /sys/kernel/debug/tracing/events/tcp/tcp_probe/enable
cat /sys/kernel/debug/tracing/trace > raw/tcpprobe.txt
echo > /sys/kernel/debug/tracing/trace

# kill tcpdump
tcpdump_pid=$(ps -e | pgrep tcpdump)
kill -2 $tcpdump_pid

# data processing 
cd py
python3 proc_ip.py
python3 proc_tcp.py
