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
	# Assumes fully connected endpointCacheLatency
	for cid in range(0, cacheServerCount):
		if endpointCacheLatency[eid][cid] < ret: 
			for assignedVid in cacheVideoAssignments[cid]:
				if (assignedVid == vid):
					ret = endpointCacheLatency[eid][cid]

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

# do the thing


# videoCount
# endpointCount
# requestCount
# cacheServerCount
# cacheServerCapacity
# videoSize
# endpointDataCenterLatency[<endpoint id>] = <latency to that endpoint>
# endpointCacheLatency[endpoint id][cache id] = <latency from that endpoint to that cache>
# videoRequestsFromEndpoint[video id][endpoint id] = <number of requests for that video from that endpoint>

roundContestants = -1
while True:
    roundAssignments = {}

    # get all caches that aren't filled
    for cid in range(0, cacheServerCount):
        if len(cacheVideoAssignments[cid]) == 0:
            roundAssignments[cid] = []

    # the number of assignments this time is the same as
    #   the number of contestants from last time
    # it is expected to go down with each iteration
    # if it doesn't go down in one iteration, it will not go down
    #   in the next iteration
    currentRoundContestants = len(roundAssignments)
    if (currentRoundContestants == roundContestants):
        break
    elif currentRoundContestants == 0:
        # also break if there's nothing left to assign
        break
    else:
        roundContestants = currentRoundContestants

    valueTable = {}

    # for each participating cache in this round of assignments
    for cid in roundAssignments:
        valueTable[cid] = 0
        cvideos = roundAssignments[cid]

        # contains tuples of the following:
        #   vid
        #   size
        #   worth on this cache
        videoTable = []

        # get all videos onto the list on videoTable
        for vid in range(0, videoCount):
            videoTable.append((vid, videoSize[vid], realisticValueOfVideoInCache(vid, cid)))

        videoTable = sorted(videoTable, key=lambda V : (V[2] / V[1], V[1], V[0]))

        # start coalescing results into the cache server
        remainingCapacity = cacheServerCapacity
        for V in videoTable:
            vid = V[0]
            size = V[1]
            worth = V[2]

            # unworthy videos get no spot
            if (worth == 0):
                continue

            # only add a video of it will fit
            if (size <= remainingCapacity):
                remainingCapacity -= size
                cvideos.append(vid)
                valueTable[cid] += worth

                # no capacity left, done packing
                if (remainingCapacity == 0):
                    break
            else:
                continue

    # sort the results 
    roundAssignments = sorted(roundAssignments.items(), key=lambda A : (valueTable[A[0]], A[0]), reverse=True)

    bestAssignment = roundAssignments[0]

    # add the best result to the
    cacheVideoAssignments[bestAssignment[0]] = bestAssignment[1]

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