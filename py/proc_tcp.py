inFile = "../raw/tcpprobe.txt"
outFile = "../stat/tcpprobe_rtt.txt"
# srttFile = "../stat/tcpprobe_srtt.txt"
cwndFile = "../stat/cwnd.txt"

with open(inFile, "r") as f:
    raw = f.readlines()

def getSrtt(r):
    return int(r.split("srtt=")[1].split(" rcv_wnd=")[0])

def getCwnd(r):
    return int(r.split("snd_cwnd=")[1].split(" ssthresh=")[0])

srtts = []
cwnds = []
for r in raw:
    if "192.168.0.151:5001" in r:
        srtts.append(getSrtt(r))
        cwnds.append(getCwnd(r))

rtts = [ 8*srtts[i]-7*srtts[i-1] for i in range(1, len(srtts))]
# rtts = srtts

rtts_string = [str(s) + "\n" for s in rtts]
srtts_string = [str(s) + "\n" for s in srtts]
cwnd_string = [str(s) + "\n" for s in cwnds]

with open(outFile, "w") as f:
    f.writelines(rtts_string)

# with open(srttFile, "w") as f:
#     f.writelines(srtts_string)

with open(cwndFile, "w") as f:
    f.writelines(cwnd_string)

print("tcp rtts agv: {}, len: {}".format(sum(rtts)/len(rtts), len(rtts)))