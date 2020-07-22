"""
bipedal robot walking simulation

by Einsbon (Sunbin Kim)
- GitHub: https://github.com/Einsbon
- Youtube:  https://www.youtube.com/channel/UCt7FZ-8uzV_jHJiKp3NlHvg
- Blog: https://blog.naver.com/einsbon
"""

import pybullet as p
import time
from time import sleep
import pybullet_data
import numpy as np
import math
import os

import motorController
import walkGenerator

# motor parameters
motor_kp = 0.5
motor_kd = 0.5
motor_torque = 20
motor_max_velocity = 5.0

# physics parameters
fixedTimeStep = 1. / 2000
numSolverIterations = 200

physicsClient = p.connect(p.GUI)
p.setTimeStep(fixedTimeStep)
p.setPhysicsEngineParameter(numSolverIterations=numSolverIterations)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # to load plane.urdf

p.setGravity(0, 0, 0)

p.resetDebugVisualizerCamera(cameraDistance=1, cameraYaw=10, cameraPitch=-0, cameraTargetPosition=[0.4, 0, 0.1])

planeID = p.loadURDF("plane.urdf")
robotID = p.loadURDF(os.path.abspath(os.path.dirname(__file__)) + '/humanoid_leg_12dof.8.urdf', [0, 0, 0.31],
                     p.getQuaternionFromEuler([0, 0, 0]),
                     useFixedBase=False)

motorsController = motorController.MotorController(robotID, physicsClient, fixedTimeStep, motor_kp, motor_kd, motor_torque, motor_max_velocity)
print(motorsController.getRevoluteJoint_nameToId())

# %%
motorController.MotorController()


walk = walkGenerator.WalkGenerator()
walk.setWalkParameter(bodyMovePoint=8,
                      legMovePoint=8,
                      height=50,
                      stride=90,
                      sit=50,
                      swayBody=30,
                      swayFoot=0,
                      bodyPositionForwardPlus=5,
                      swayShift=3,
                      liftPush=0.5,
                      landPull=0.7,
                      timeStep=0.06,
                      damping=0.0,
                      incline=0.0)
walk.generate()
walk.inverseKinematicsAll()
walk.showGaitPoint3D()

actionTime = walk._timeStep
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(0)
motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesStartRight[0], 2, 0)

# rest 1 second in engine
waitTime = 1
repeatTime = int(waitTime / fixedTimeStep)
for _ in range(repeatTime):
    p.stepSimulation()
    # time.sleep(fixedTimeStep)

p.setGravity(0, 0, -9.8)
rightStep = True
walkPointNum = walk._bodyMovePoint + walk._legMovePoint

for i in range(walkPointNum):
    motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesStartLeft[i], actionTime, 0)
for _ in range(4):
    for i in range(np.size(walk.walkAnglesWalkingRight, 0)):
        motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesWalkingRight[i], actionTime, 0)
    for i in range(np.size(walk.walkAnglesWalkingLeft, 0)):
        motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesWalkingLeft[i], actionTime, 0)
for i in range(walkPointNum):
    motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesEndRight[i], actionTime, 0)
'''
Implemented in a more complex way.

if rightStep == True:
    for i in range(walkPointNum):
        motorsController.setMotorsAngleInFixedTimestep(
            walk.inverseKinematicsPoint(walk.walkPointStartRightstepRightLeg[:, i], walk.walkPointStartRightstepLeftLeg[:, i]), actionTime, 0)
    rightStep = False
else:
    for i in range(walkPointNum):
        motorsController.setMotorsAngleInFixedTimestep(
            walk.inverseKinematicsPoint(walk.walkPointStartLeftstepRightLeg[:, i], walk.walkPointStartLeftstepLeftLeg[:, i]), actionTime, 0)
    rightStep = True
for i in range(4):
    if(rightStep):
        # right foot step
        for i in range(walkPointNum):
            motorsController.setMotorsAngleInFixedTimestep(
                walk.inverseKinematicsPoint(walk.walkPointRightStepRightLeg[:, i], walk.walkPointRightStepLeftLeg[:, i]), actionTime, 0)
        rightStep = False
    else:
        # left foot step
        for i in range(walkPointNum):
            motorsController.setMotorsAngleInFixedTimestep(
                walk.inverseKinematicsPoint(walk.walkPointLeftStepRightLeg[:, i], walk.walkPointLeftStepLeftLeg[:, i]), actionTime, 0)
        rightStep = True
if rightStep == True:
    # end walking. left
    for i in range(walkPointNum):
        motorsController.setMotorsAngleInFixedTimestep(
            walk.inverseKinematicsPoint(walk.walkPointEndRightstepRightLeg[:, i], walk.walkPointEndRightstepLeftLeg[:, i]), actionTime, 0)
    rightStep = False
else:
    # end walking. left
    for i in range(walkPointNum):
        motorsController.setMotorsAngleInFixedTimestep(
            walk.inverseKinematicsPoint(walk.walkPointEndLeftstepRightLeg[:, i], walk.walkPointEndLeftstepLeftLeg[:, i]), actionTime, 0)
    rightStep = True
'''

# rest 2 seconds in engine
waitTime = 1
repeatTime = int(waitTime / fixedTimeStep)
for _ in range(repeatTime):
    p.stepSimulation()

# robot control using (x,y,z) point.
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 0, 0], [0, 0, 0]), 0.5, 0.5)
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 0, 40], [0, 0, 40]), 0.5, 0.5)
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 0, 0], [0, 0, 0]), 0.5, 0.5)
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 0, 40], [0, 0, 40]), 0.5, 0.5)
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 30, 40], [0, 30, 40]), 0.5, 0.5)
motorsController.setMotorsAngleInFixedTimestep(walk.inverseKinematicsPoint([0, 0, 40], [0, 0, 40]), 0.5, 0.5)

# More applied version. Press Enter to start or stop walking.
walking = False
rightStep = True
while (1):
    keys = p.getKeyboardEvents()
    for k, v in keys.items():
        if (k == 65309) and (v == 3 or v == 6):  # if enter key is pressed
            walking = True
            keys = {}

    if walking == True:
        if rightStep == True:
            for i in range(walkPointNum):
                motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesStartRight[i], actionTime, 0)
            rightStep = False
        else:
            for i in range(walkPointNum):
                motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesStartLeft[i], actionTime, 0)
            rightStep = True

        keys = p.getKeyboardEvents()
        for k, v in keys.items():
            if (k == 65309) and (v == 3 or v == 6):  # if enter key is pressed
                walking = False
                keys = {}

        while (walking):
            if (rightStep):
                for i in range(walkPointNum):
                    motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesWalkingRight[i], actionTime, 0)
                rightStep = False
            else:
                for i in range(walkPointNum):
                    motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesWalkingLeft[i], actionTime, 0)
                rightStep = True

            keys = p.getKeyboardEvents()
            for k, v in keys.items():
                if (k == 65309) and (v == 3 or v == 6):  # if enter key is pressed
                    walking = False
                    keys = {}

        if rightStep == True:
            for i in range(walkPointNum):
                motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesEndRight[i], actionTime, 0)
            rightStep = False
        else:
            for i in range(walkPointNum):
                motorsController.setMotorsAngleInFixedTimestep(walk.walkAnglesEndLeft[i], actionTime, 0)
            rightStep = True
    else:
        p.stepSimulation()


# %%
