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

        latency = int(eargs[0])
        endpointDataCenterLatency[e] = latency

        endpointCacheLatency[e] = {}
        cachesConnected = int(eargs[1])
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

# gives the best current latency for a video and endpoint. 
# If the video isn't in a connected cache, this will be the datacentre latency.
# Takes a video id, endpoint id, and a list of 
def currentBestVideoEndpointLatency(vid, eid, cacheVideoAssignments):
	ret = endpointDataCenterLatency[eid]
	return ret

#============================================#
#   do the thing                             #
#============================================#

# this stores our answers to the question. 
cacheVideoAssignments = {}
for cid in range(0, cacheServerCount):
	cacheVideoAssignments[cid] = []

# do the thing



# print the solution
print(str(cacheServerCount))
for cid in range(0, cacheServerCount):
	print(str(cid), end='')
	for vid in cacheVideoAssignments[cid]:
		print(' ' + str(vid), end='')
	print('')

# videoCount
# endpointCount
# requestCount
# cacheServerCount
# cacheServerCapacity
# endpointDataCenterLatency[<endpoint id>] = <latency to that endpoint>
# endpointCacheLatency[endpoint id][cache id] = <latency from that endpoint to that cache>
# videoRequestsFromEndpoint[video id][endpoint id] = <number of requests for that video from that endpoint>