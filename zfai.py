import math

# Note: argument 'parts' is a string of comma separated part IDs. e.g. '1,2,3'

def printAll(arr):
	for str in arr:
		print str
		
def secToFrames(sec):
	return math.floor(sec * 30)

def macro_setSize(parts, size, START_FRAME, REPEAT_AFTER_FRAMES):
	strs = []

	strs.append(makeTriggerRepeat(START_FRAME, REPEAT_AFTER_FRAMES, setWidth(parts, size)))
	strs.append(makeTriggerRepeat(START_FRAME, REPEAT_AFTER_FRAMES, setHeight(parts, size)))

	return strs
	
def randomRotate(speed):
	return 'randomRotate, %d' % speed

def makeInvincible(parts):
	return 'makeInvincible, %s' % parts
	
def makeTriggerRepeat(START_FRAME, REPEAT_AFTER_FRAMES, ANY_COMMAND):
	return 'makeTrigger, timeRepeat, %d, %d, %s' % (START_FRAME, REPEAT_AFTER_FRAMES, ANY_COMMAND)

def disableGun(parts):
	return 'disableGun, ' + parts
def enableGun(parts):
	return 'enableGun, ' + parts
	
def rotatePartToShip(parts):
	return 'rotatePartToShip, ' + parts
	
def setDistance(parts, dist):
	return 'setDistance, %d, %s' % (dist, parts)

def setGunTime(parts, time):
	return 'setGunTime, %d, %s' % (time, parts)

def setWidth(parts, widthPercentage):
	return 'setWidth, %d, %s' % (widthPercentage, parts)

def setHeight(parts, heightPercentage):
	return 'setHeight, %d, %s' % (heightPercentage, parts)

def setSize(parts, percentage):
	strs = []
	strs.append( setWidth(parts, percentage) )
	strs.append( setHeight(parts, percentage) )
	return strs

def rotatePartToShip(parts):
	return 'rotatePartToShip, %s' % (parts)
	
def stop(cmd):
	return 'stop, %s' % cmd
	
# parts: list of Single Shot guns
def macro_machineGun(parts):
	return makeTriggerRepeat(0,5, setGunTime(parts, 98))

# parts: list of Single Shot guns
def macro_stopMachineGun(parts):
	return stop(makeTriggerRepeat(0,5, setGunTime(parts, 98)))
	
# parts: list of Single Shot guns
def macro_machineGunOnOff(parts):
	strs = []
	
	phaseDuration = secToFrames(6)
	strs.append( makeTriggerRepeat(secToFrames(0), phaseDuration, disableGun(parts)) )
	strs.append( makeTriggerRepeat(secToFrames(0), phaseDuration, macro_stopMachineGun(parts)) )
	strs.append( makeTriggerRepeat(secToFrames(4), phaseDuration, enableGun(parts)) )
	strs.append( makeTriggerRepeat(secToFrames(4), phaseDuration, macro_machineGun(parts)) )
	
	return strs

def macro_linearMove(parts, waitTimeDuration, moveTimeDuration, startDist, endDist, waitDist):
	strs = []
	
	startMoveTime = int(waitTimeDuration)
	totalTime = int(waitTimeDuration) + int(moveTimeDuration)
	
	distToTravel = endDist - startDist
	distPerStep = math.floor(distToTravel / moveTimeDuration)
	
	# Wait: set distance to static location
	setDistCmd = setDistance(parts, waitDist)
	strs.append(
		makeTriggerRepeat(0, totalTime, setDistCmd)
	)
	
	# Move: distance chages over time
	for time in range(startMoveTime, totalTime):
		timeDelta = time - startMoveTime
		
		newDist = startDist + timeDelta*distPerStep
	
		setDistCmd = setDistance(parts, newDist)
		strs.append(
			makeTriggerRepeat(time, totalTime, setDistCmd)
		)
	
	return strs
	
GUNTIME_SINGULARITY_FIRST_SHOT = 109
def macro_singularityFire(parts, timeToFire):
	strs = []
	strs.append( makeTriggerRepeat(timeToFire, timeToFire, enableGun(parts)) )
	strs.append( makeTriggerRepeat(timeToFire, timeToFire, setGunTime(parts, GUNTIME_SINGULARITY_FIRST_SHOT)) )
	strs.append( makeTriggerRepeat(4, timeToFire, disableGun(parts)) )
	
	return strs
	
def macro_rotateToShipOnceRepeating(parts, rotateTime, cycleTime):
	strs = []
	strs.append( makeTriggerRepeat(rotateTime, cycleTime, rotatePartToShip(parts)) )
	strs.append( makeTriggerRepeat(rotateTime+1, cycleTime, stop(rotatePartToShip(parts))) )
	return strs
