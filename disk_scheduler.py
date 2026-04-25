def fcfs(requests, head):
    seeks = []
    current = head
    for req in requests:
        seeks.append(abs(req - current))
        current = req
    return seeks, sum(seeks)

def sstf(requests, head):
    seeks = []
    current = head
    remaining = requests.copy()
    while remaining:
        closest = min(remaining, key=lambda x: abs(x - current))
        seeks.append(abs(closest - current))
        current = closest
        remaining.remove(closest)
    return seeks, sum(seeks)

def scan(requests, head, max_track=200):
    seeks = []
    current = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort(reverse=True)
    right.sort()
    
    for req in right:
        seeks.append(abs(req - current))
        current = req
    
    if left:
        seeks.append(abs(max_track - current))
        current = max_track
        for req in left:
            seeks.append(abs(req - current))
            current = req
    
    return seeks, sum(seeks)

def cscan(requests, head, max_track=200):
    seeks = []
    current = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort()
    right.sort()
    
    for req in right:
        seeks.append(abs(req - current))
        current = req
    
    if left:
        seeks.append(abs(max_track - current))
        seeks.append(max_track)
        current = 0
        for req in left:
            seeks.append(abs(req - current))
            current = req
    
    return seeks, sum(seeks)

def compare_algorithms(requests, head=100, max_track=200):
    results = {}
    
    fcfs_seeks, fcfs_total = fcfs(requests, head)
    results['FCFS'] = {'seeks': fcfs_seeks, 'total': fcfs_total}
    
    sstf_seeks, sstf_total = sstf(requests, head)
    results['SSTF'] = {'seeks': sstf_seeks, 'total': sstf_total}
    
    scan_seeks, scan_total = scan(requests, head, max_track)
    results['SCAN'] = {'seeks': scan_seeks, 'total': scan_total}
    
    cscan_seeks, cscan_total = cscan(requests, head, max_track)
    results['C-SCAN'] = {'seeks': cscan_seeks, 'total': cscan_total}
    
    best = min(results.items(), key=lambda x: x[1]['total'])[0]
    
    return results, best