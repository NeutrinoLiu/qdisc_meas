inFile = "../raw/tcpdump.txt"
outFile = "../stat/tcpdump_rtt.txt"

with open(inFile, "r") as f:
    raw = f.readlines()


def getSeq(r):
    span = r.split(" seq ")[1].split(", ack 1,")[0]
    return int(span.split(":")[1])

def getAck(r):
    span = r.split(", ack ")[1].split(", win ")[0]
    return int(span)

def getTs(r):
    span_sec = r.split(" ")[0].split(":")[-1]
    span_min = r.split(" ")[0].split(":")[-2]
    return int(span_min) * 60 + float(span_sec)


snd_t = {}
rev_t = {}
for r in raw:
    # if is a sender ip packet
    try:
        if "seq" in r and "Flags [R" not in r and "Flags [S" not in r and "Flags [F" not in r :
            snd_t[getSeq(r)] = getTs(r)
        if "197.227.12.11.5201 > neutrino-XPS.5001" in r and "ack" in r:
            rev_t[getAck(r)] = getTs(r)
    except:
        print(r)

rtts = []
for k in rev_t.keys():
    if k in snd_t:
        rtts.append(int((rev_t[k] - snd_t[k])*1e6))

rtts_string = [str(r) + "\n" for r in rtts]

with open(outFile, "w") as f:
    f.writelines(rtts_string)

print("ip rtts agv: {}, len: {}".format(sum(rtts)/len(rtts), len(rtts)))