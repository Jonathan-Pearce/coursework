from pybullet_envs.bullet.kukaGymEnv import KukaGymEnv
from itertools import count
import matplotlib.pyplot as plt
import numpy as np 

env = KukaGymEnv(renders=True, isDiscrete=False)
env.reset()

unwrapped = env.unwrapped
unwrapped.reset()
p = unwrapped._p

#do not scale robot arm weight
mass_multiplier = 1
#collect z coordinate data of robot arm gripper
data_org = []

#Run simulation
for t in count():
    #action = env.action_space.sample()
    action = [0,0,0]
    next_obs, reward, done, _ = env.step(action)

    data_org.append(next_obs[2])


    if done == True:
        break

    obs = next_obs

#reset 
env.reset()
#we will scale the weight of the arm
mass_multiplier = 5
#z coordinate data of robot arm gripper
data_changed = [0.0981]*len(data_org)

#part = unwrapped.robot.parts['planeLink']
print("numBodies = ", p.getNumBodies())
for b in range (p.getNumBodies()):
    print("info for body[",b,"]=",p.getBodyInfo(b))
    for j in range(p.getNumJoints(b)):
        print("bodyInfo[",b,",",j,"]=",p.getJointInfo(b,j))
        info = p.getDynamicsInfo(b, j)
        mass_part = info[0]
        print('before mass', mass_part)
        #change weight of robot arm components!
        p.changeDynamics(b, j, mass=mass_part*mass_multiplier)
        info = p.getDynamicsInfo(b, j)
        mass_part_new = info[0]
        print('before mass', mass_part_new)


index = 0
for t in count():
    #action = env.action_space.sample()
    action = [0,0,0]
    next_obs, reward, done, _ = env.step(action)

    data_changed[index] = next_obs[2]
    index += 1

    if done == True:
        break

    obs = next_obs

del data_org[-1]
del data_changed[index-1]

#plot data
x = np.arange(0.0, len(data_org), 1)

plt.figure(figsize=(10,6))

plt.plot(x, data_org, label="original arm weight")
plt.plot(x, data_changed, label="5x arm weight")

plt.title('Tracking Kuka Arm Gripper Z Coordinate Under Passive Dynamics')
plt.xlabel('timestep')
plt.ylabel('z coordinate of gripper in global frame')
plt.legend(loc='lower left')

plt.show()
