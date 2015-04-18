# -*- encoding: UTF-8 -*- 

''' Whole Body Motion: Left or Right Arm position control '''

import sys
import motion
import time
from naoqi import ALProxy
import almath

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(robotIP, effectorName):
    ''' Example of a whole body Left or Right Arm position control
        Warning: Needs a PoseInit before executing
                 Whole body balancer must be inactivated at the end of the script
    '''

    # Init proxies.

    motionProxy = ALProxy("ALMotion", robotIP, 9559)
    postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)  

    effectorList = ["RArm"]

    # Enable Whole Body Balancer
    isEnabled  = True
    proxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    proxy.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    proxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    space = motion.FRAME_ROBOT

    targetCoordinateList = [
        [0.10, 0.05, 0.00, 0.00, 0.00, 0.00], # target 4 for "RArm"
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00], # target 4 for "RArm"
    ]

    axisMaskList = [almath.AXIS_MASK_VEL] # for "RArm"

    coef = 1.5  # Seconds
    timesList  = [[coef*(i+1) for i in range(1)] ] # for "RArm" in seconds
    isAbsolute   = False

     # called cartesian interpolation
    motionProxy.positionInterpolations(effectorList, space, targetCoordinateList,
                                 axisMaskList, timesList, isAbsolute)

    # Deactivate whole body
    isEnabled    = False
    proxy.wbEnable(isEnabled)


if __name__ == "__main__":
    robotIp      = "169.254.95.24"
    effectorName = "RArm"

    main(robotIp, effectorName)