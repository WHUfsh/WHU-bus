import copy

def extract_time(lines, max_stop):    
    expanded_list = []
    cur_expanded = [ [] for i in range(0, max_stop+1)]
    prev_time = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        _, arrived, nums, direction, stop, cur_time = line.split(',')
        if prev_time is None:
            prev_time = cur_time
        if prev_time != cur_time:
            expanded_list.append(cur_expanded)
            cur_expanded = [[] for i in range(0, max_stop+1)]
        prev_time = cur_time
        for i in range(0, int(nums)):
            cur_expanded[int(stop)].append(int(arrived))
            cur_expanded[0] = cur_time

    if prev_time:
        expanded_list.append(cur_expanded)

    arrives = [[] for i in range(0, max_stop+1)]
    departs = [[] for i in range(0, max_stop+1)]
    # TODO: should adjust prev based on expanded_list[0]
    prev = [None for i in range(0, max_stop+1)]
    for expanded in expanded_list:
        expanded_copy = copy.deepcopy(expanded)
        for i in range(1, max_stop+1):
            if prev[i]:
                prev[i].sort()
                for arrive_status in prev[i]:
                    # check if we've changed status or no
                    if arrive_status in expanded_copy[i]:
                        expanded_copy[i].remove(arrive_status)
                    # bus hasn't arrived yet 
                    if arrive_status == 0:
                        # if it arrived
                        if 1 in expanded_copy[i]:
                            arrives[i].append(expanded[0])
                            expanded_copy[i].remove(1) 
                        # jumped a stop
                        # TODO: fix bus reaching final stop
                        elif i+1<=max_stop and 0 in expanded_copy[i+1]:
                            arrives[i].append(expanded[0])
                            departs[i].append(expanded[0])
                            expanded_copy[i+1].remove(0)
                    # bus arrived
                    if arrive_status == 1:
                        # check if it departed
                        # TODO: fix bus reaching final stop
                        if i+1<=max_stop and 0 in expanded_copy[i+1]:
                            departs[i].append(expanded[0])
                            expanded_copy[i+1].remove(0)
        prev = expanded

    return arrives, departs

if __name__ == '__main__':
    lines = []
    with open('buslian2.txt') as f:
        lines = f.readlines()
    max_stop = 7
    arrives, departs = extract_time(lines, max_stop)
    print "arrive times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print arrives[i]

    print "depart times"
    for i in range(1, max_stop + 1):
        print "terminal %d" % i
        print departs[i]
