#============================================#
#   read inputs                              #
#============================================#

# main parameters go here
videoCount = 1
endpointCount = 1
requestCount = 1
cacheServerCount = 1
cacheServerCapacity = 1

try:
    args = input().split(' ')
    videoCount = int(args[0])
    endpointCount = int(args[1])
    requestCount = int(args[2])
    cacheServerCount = int(args[3])
    cacheServerCapacity = int(args[4])
except:
    print('Error when reading first line of input')
    exit()

# get descriptions of each video
videoSize = []
try:
    args = input().split(' ')

    if len(args) != videoCount:
        print('Number of video sizes does not match number of videos')
        exit()

    for v in range(0, videoCount):
        videoSize.append(int(args[v]))
except:
    print('Error when reading video sizes')
    exit()

# get endpoint data

# hashtable for:

# hashtable for:
# endpointDataCenterLatency[<endpoint id>] = <latency to that endpoint>
endpointDataCenterLatency = {}

# hashtable of hashtables for:
# endpointCacheLatency[endpoint id][cache id] = <latency from that endpoint to that cache>
endpointCacheLatency = {}

try:
    for e in range(0, endpointCount):
        eargs = input().split(' ')

        # Determine datacenter latency for this endpoint.
        latency = int(eargs[0])
        endpointDataCenterLatency[e] = latency
        cachesConnected = int(eargs[1])

        # Initalize every cache latency as equal to datacenter latency
        # This makes the hashtable fully connected.  
        endpointCacheLatency[e] = {}
        for cid in range(0, cacheServerCount):
        	endpointCacheLatency[e][cid] = latency

    	# Determine latency of connected caches. 
        for c in range(0, cachesConnected):
            cargs = input().split(' ')

            cid = int(cargs[0])
            clatency = int(cargs[1])
            endpointCacheLatency[e][cid] = clatency
except:
    print('Error when reading endpoint details')
    exit()


# get request data

# hashtable of hastables for:
# videoRequestsFromEndpoint[video id][endpoint id] = <number of requests for that video from that endpoint>
videoRequestsFromEndpoint = {}
try:
    for r in range(0, requestCount):
        rarg = input().split(' ')
        vid = int(rarg[0])
        endpoint = int(rarg[1])
        requests = int(rarg[2])


        if vid not in videoRequestsFromEndpoint:
            videoRequestsFromEndpoint[vid] = {}

        # assuming requests for vid from endpoint are only singularly listed, i.e. not split across lines
        videoRequestsFromEndpoint[vid][endpoint] = requests
except:
    print('Error when reading video requests')
    exit()

#============================================#
#   helper functions                         #
#============================================#

# returns the value of a video vid if it were put in cache cid
# does not regard contents of any cache
def valueOfVideoInCache(vid : int, cid : int):
    if videoSize[vid] > cacheServerCapacity:
        return 0

    if vid not in videoRequestsFromEndpoint:
        return 0

    totalValue = 0
    for eid in videoRequestsFromEndpoint[vid]:
        totalValue += videoRequestsFromEndpoint[vid][eid] * (endpointDataCenterLatency[eid] - endpointCacheLatency[eid][cid])

    return totalValue

# returns the value of a video vid if it were put in cache cid
# DOES factor in the contents of other caches... but is slower
def realisticValueOfVideoInCache(vid : int, cid : int):
    if videoSize[vid] > cacheServerCapacity:
        return 0

    if vid not in videoRequestsFromEndpoint:
        return 0

    totalValue = 0
    for eid in videoRequestsFromEndpoint[vid]:
    	totalValue += max(0, videoRequestsFromEndpoint[vid][eid] * (currentBestVideoEndpointLatency(vid, eid, cacheVideoAssignments) - endpointCacheLatency[eid][cid]))

    return totalValue

# gives the best current latency for a video and endpoint. 
# If the video isn't in a connected cache, this will be the datacentre latency.
# Takes a video id, endpoint id, and a list of cache-video assignments 
def currentBestVideoEndpointLatency(vid, eid, cacheVideoAssignments):
	ret = endpointDataCenterLatency[eid]

	# search for the video in connected caches, find the fastest one it's connected to 
	for cid in range(0, cacheServerCount):
		latency = endpointCacheLatency[eid][cid]
		if (latency < ret) and (vid in cacheVideoAssignments[cid]): 
			ret = latency

	return ret

# gives the best possible latency for a video and endpoint (ie. if the video was cached ideally).
# If the endpoint has no connected caches OR the video is too large for a cache, returns the datacenter latency.
def bestPossibleVideoEndpointLatency(vid, eid):
	ret = endpointDataCenterLatency[eid]

	# if the video is too large to fit in a cache, we're done here
	if (videoSize[vid] > cacheServerCapacity):
		return ret

	# look at all connected caches, find the fastest one it's connected to 
	for cid in range(0, cacheServerCount):
		if endpointCacheLatency[eid][cid] < ret: 
			ret = endpointCacheLatency[eid][cid]

	return ret

#============================================#
#   do the thing                             #
#============================================#

# this stores our answers to the question. 
cacheVideoAssignments = {}
for cid in range(0, cacheServerCount):
	cacheVideoAssignments[cid] = []

# stores how much capacity each cache has 
cacheRemainingCapacity = []
for i in range(0, cacheServerCount):
	cacheRemainingCapacity.append(cacheServerCapacity)

# find the smallest video 
minVideoSize = min(videoSize)

# for each video/cache pairing, just do whatever one seems the best 
# (very greedy approach)
while True:
	bestVid = -1; 
	bestCid = -1; 
	bestScore = -1; 

	for cid in range(0, cacheServerCount): 
		capacity = cacheRemainingCapacity[cid]
		# If this cache can no longer hold ANY videos, continue
		if (capacity < minVideoSize):
			continue

		for vid in range(0, videoCount):
			size = videoSize[vid]

			# If this video cannot fit in this cache or is already in it, continue
			if (capacity < size) or (vid in cacheVideoAssignments[cid]):
				continue

			# Score the potential placement of this video in this cache
			# Video size is factored in, smaller videos are prioritized
			score = realisticValueOfVideoInCache(vid, cid) / size
			if (score > 0) and (score > bestScore):
				bestVid = vid
				bestCid = cid
				bestScore = score

	# Perform the chosen placement and update the new remaining capacity 
	# If no choices are possible, we're done here. 
	if (bestVid != -1):
		cacheVideoAssignments[bestCid].append(bestVid)
		cacheRemainingCapacity[bestCid] -= videoSize[bestVid]
	else:
		break

#########################

# sanity check - make sure no cache is overfilled 
for cid in range(0, cacheServerCount): 
	capacityUsed = 0
	for vid in cacheVideoAssignments[cid]: 
		capacityUsed += videoSize[vid]
	if (capacityUsed > cacheServerCapacity): 
		print('ERROR: cache {0} is overfilled (cheater!)'.format(cid))

# score the solution 
timeSaved = 0
totalRequests = 0 
# go through every request to see how much latency was saved on it 
for vid in videoRequestsFromEndpoint: 
	for eid in videoRequestsFromEndpoint[vid]:
		# find the time saved by caching the video (if any)
		requestCount = videoRequestsFromEndpoint[vid][eid]
		bestLatency = currentBestVideoEndpointLatency(vid, eid, cacheVideoAssignments)
		requestTimeSaved = requestCount * (endpointDataCenterLatency[eid] - bestLatency)
		timeSaved += requestTimeSaved
		totalRequests += requestCount

		#find the ideal time save if the video was cached in the fastest possible cache 
		idealLatency = bestPossibleVideoEndpointLatency(vid, eid)
		idealTimeSaved = requestCount * (endpointDataCenterLatency[eid] - idealLatency)

		print('vid {0} at eid {1} saved {2} ms (ideal = {3})'.format(vid, eid, requestTimeSaved, idealTimeSaved))

print('{0} ms saved on average'.format(timeSaved / totalRequests))

#============================================#
#   print the thing                          #
#============================================#

# print the solution
#cacheVideoAssignments = sorted(cacheVideoAssignments.items(), key=lambda A : A[0])
print(str(cacheServerCount))
for cid in range(0, cacheServerCount):
    print(str(cid), end='')
    #cacheVideoAssignments[cid] = sorted(cacheVideoAssignments)
    for vid in cacheVideoAssignments[cid]:
        print(' ' + str(vid), end='')
    print('')