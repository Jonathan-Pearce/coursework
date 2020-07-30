'''
This is the main file for implementing your cartpole control logic. 
There is only one TODO, but it includes writing some setup code at
the global scope to compute the LQR control gains, K and then 
applying those gains within the policyfn() method.
There are many other things going on in the code lower in this file
and in the accompanying files, which you can
mostly ignore. 
'''
import numpy as np
import scipy.linalg
from plant import gTrig_np
from cartpole import default_params
from cartpole import CartpoleDraw
import matplotlib.pyplot as plt
import sys
#np.random.seed(31337)
np.set_printoptions(linewidth=500)
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

data = []

# An lqr helper function that you can use in call in your solution
# Note: We expect this code to return with error for invalid
# A, B, Q, and R values such as the defaults we entered in the starter code.
# You must derive the proper matrices before this will start working.
def lqr( A, B, Q, R ):  
    x = scipy.linalg.solve_continuous_are( A, B, Q, R )
    k = np.linalg.inv(R) * np.dot( B.T, x )
    return k

# Constants for our cartpole that you can use in your solution
g = 9.82
m = 0.5
M = 0.5
l = 0.5
b = 0.1

# FOR YOU TODO: Fill in the values for a, b, q and r here.
# Note that they should be matrices not scalars. 
# Then, figure out how to apply the resulting k
# to solve for a control, u, within the policyfn that balances the cartpole.
A = np.array(
    [[ 0, 1, 0, 0 ],
    [ 0, -4*b/(4*M +m), 0, 3 * g * m / (4*M +m) ],
    [ 0, 6*b/(l * (4*M +m)), 0, -6* (m + M) * g / (l * (4*M +m)) ],
    [ 0,0, 1, 0 ]])

B = np.array( [[0,
    4 / (4*M +m),
    -6 / (l * (4*M +m)),
    0]] )

B.shape = (4,1)

Q =  np.array([
    [ 100, 0, 0, 0 ],
    [ 0, 1, 0, 0 ],
    [ 0, 0, 100, 0 ],
    [ 0, 0, 0, 1]] )

R = np.array([[1]])
print( "A holds:",A)
print( "B holds:",B)
print( "Q holds:",Q)
print( "R holds:",R)

# Uncomment this to get the LQR gains k once you have
# filled in the correct matrices.
k = lqr( A, B, Q, R )
print( "k holds:",k)
#print( "k holds:",k)

def policyfn( x ):

    #print(x)
    if x[0]>1 or x[0]<-1:
        print("TOO MUCH DRIFT!")
        sys.exit(0)


    x = np.matrix(  [
                    [np.squeeze(np.asarray(x[0]))],
                    [np.squeeze(np.asarray(x[1]))],
                    [np.squeeze(np.asarray(x[2]))],
                    [np.squeeze(np.asarray(x[3]-np.pi))]
                    ])

    goal = np.matrix(    [
                    [0],
                    [0],
                    [0],
                    [0]
                    ])

    #print(x)
    #sys.exit(0)
    u = k*(x-goal)

    #print(u)
    #sys.exit(0)

    #u = 0    
    return np.array([u])        

def apply_controller(plant,params,H,policy=None):
    '''
    Starts the plant and applies the current policy to the plant for a duration specified by H (in seconds).
    @param plant is a class that controls our robot (simulation)
    @param params is a dictionary with some useful values 
    @param H Horizon for applying controller (in seconds)
    @param policy is a function pointer to the code that implements your 
            control solution. It will be called as u = policy( state )
    '''

    # start robot
    x_t, t = plant.get_plant_state()
    if plant.noise is not None:
        # randomize state
        Sx_t = np.zeros((x_t.shape[0],x_t.shape[0]))
        L_noise = np.linalg.cholesky(plant.noise)
        x_t = x_t + np.random.randn(x_t.shape[0]).dot(L_noise);
    
    sum_of_error = 0
    H_steps = int(np.ceil(H/plant.dt))
    for i in xrange(H_steps):
        # convert input angle dimensions to complex representation
        x_t_ = gTrig_np(x_t[None,:], params['angle_dims']).flatten()
        #  get command from policy (this should be fast, or at least account for delays in processing):
        u_t = policy(x_t_)
        #For plotting
        data.append(x_t_)
       
        #  send command to robot:
        plant.apply_control(u_t)
        plant.step()
        x_t, t = plant.get_plant_state()
        l = plant.params['l']
        st = np.sin(x_t_[3])
        ct = np.cos(x_t_[3])
        goal = np.array([0,l])
        end =  np.array( [ x_t[0] + l*st, -l*ct ] )  
        dist = np.sqrt( (goal[0]-end[0])*(goal[0]-end[0]) +  (goal[1]-end[1])*(goal[1]-end[1]) ) 
        sum_of_error = sum_of_error + dist

        if plant.noise is not None:
            # randomize state
            x_t = x_t + np.random.randn(x_t.shape[0]).dot(L_noise);
        
        if plant.done:
            break

    print("Error this episode was: ",sum_of_error)
        
    # stop robot
    plant.stop()

def main():
    
    # learning iterations
    N = 1 
    H = 10
    
    learner_params = default_params()
    plant_params = learner_params['params']['plant'] 
    plant = learner_params['plant_class'](**plant_params)
   
    #draw_cp = CartpoleDraw(plant)
    #draw_cp.start()
    
    # loop to run controller repeatedly
    for i in xrange(N):
        
        # execute it on the robot
        plant.reset_state()
        apply_controller(plant,learner_params['params'], H, policyfn)

    print(len(data))
    print(len(data[0]))
    print(data[0])

    new_data = np.asarray(data)
    print(new_data.shape)
    print(len(new_data))
    print(new_data[0])

    x = np.arange(len(new_data))

    plt.figure()

    # linear
    plt.subplot(221)
    plt.plot(x, new_data[:,0])
    #plt.ylabel('x')
    plt.title('position')
    plt.grid(True)


    # log
    plt.subplot(222)
    plt.plot(x, new_data[:,1])
    #plt.ylabel(u'x\u0307')
    plt.title(u'velocity')
    plt.grid(True)


    # symmetric log
    plt.subplot(224)
    plt.plot(x, new_data[:,2])
    #plt.ylabel(u'\u03B8\u0307')
    plt.title(u'angular velocity')
    plt.grid(True)

    # logit
    plt.subplot(223)
    plt.plot(x, new_data[:,3])
    #plt.ylabel(u'\u03B8')
    plt.title(u'angle (radians)')
    plt.grid(True)

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.35,
                    wspace=0.35)

    plt.show()

    
if __name__ == '__main__':
    main()
    
