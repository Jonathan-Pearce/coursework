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

#######################################################################
min_x = -0.3
number_x = 5
delta_x = (min_x*-2)/number_x

#2: velocity

#check reasonable value from freefall state
min_v = -0.25
number_v = 5
delta_v = (min_v*-2)/number_v

#3: angular velocity

#check reasonable value from freefall state
min_av = -0.25
number_av = 10
delta_av = (min_av*-2)/number_av


#4: angle
min_a = np.pi-0.1
max_a = np.pi+0.1
number_a = 5
#keep in radians
delta_a = (0.2)/number_a


#5: actions
min_u = -0.5
number_u = 10
delta_u = (min_u*-2)/number_u
print('delta_u: ',delta_u)
number_u += 1

min_bound = np.array([min_x,min_v,min_av,min_a])
delta = np.array([delta_x,delta_v,delta_av,delta_a])
number = np.array([number_x,number_v,number_av,number_a])
zeros = np.zeros(4)

#value function
V = np.zeros((number_x,number_v,number_av,number_a))


Q =  np.array([[ 100, 0, 0, 0 ],
       	       [ 0, 1, 0, 0 ],
	            [ 0, 0, 10, 0 ],
               [ 0, 0, 0, 100 ]] )

theta=1
discount_factor=0.9

policy = np.zeros((number_x,number_v,number_av,number_a))

n = np.array(np.meshgrid([0, delta_x], [0, delta_v],[0, delta_av],[0, delta_a])).T.reshape(-1,4)
#######################################################################

def state_action(x_t,u_t,plant):
    #apply dynamics       
    #  send command to robot:
    plant.set_state(x_t)
    plant.apply_control(np.array(([u_t])))
    plant.step()
    x_t, t = plant.get_plant_state()
    return x_t
    #return new_state

#input index, e.g. (0,1,2,3)
#output state e.g. (1.2,5.4,4.2,pi/4)
def index_to_state(i):
    x = np.zeros(4)
    #we count up from min by delta each time 
    x = np.add(min_bound,np.multiply(delta,i))
    return x

def state_to_index(x):
	#checks to make sure they are all inbounds!
	i = np.zeros(4)
	#subtract min bound and divide by deltas
	i = np.rint(np.divide(np.subtract(x,min_bound),delta))
	return tuple(i.astype(int))

def index_valid(i):
    #lowerbound = np.greater_equal(i, zeros)
    #upperbound = np.
    # try:
    #     Value = V[i]
    #     return True
    # except IndexError:
    #     return False
    #valid = True
    for j in range(4):
    	if i[j] < 0 or i[j] >= number[j]:
    		return False
    return True

def state_score(s):
    s[3] -= np.pi
    #print(Q)
    return -np.dot(np.dot(s, Q),s.T)


#given action index
def get_action(n):
    return (min_u + n*delta_u)

#round state down
def floor_index(x):
	i = np.zeros(4)
	#subtract min bound and divide by deltas
	i = np.floor(np.divide(np.subtract(x,min_bound),delta))
	return tuple(i.astype(int))

def get_neighbour_states(s):
	#convert to index and round down
	base_index = floor_index(s)
	#convert back to state
	base_state = index_to_state(base_index)
	#intialize
	neighbours = np.zeros([16,4])

	for j in range(16):
		neighbours[j,:] = base_state + n[j]  

	#print(s)
	#print(base_state)
	#print(delta)


	#for j in range(16):
		#print(neighbours[j])
		#print(state_to_index(neighbours[j]))
		#print(index_valid(state_to_index(neighbours[j])))
	#print(neighbours)

	#sys.exit(0)
	return neighbours

def neighbour_prob(s,n):
	p = np.zeros(16)

	for i in range(16):
		p[i] = 1/(np.linalg.norm(s-n[i])+0.000001)

	total = sum(p)
	p = np.divide(p,total)
	#print(sum(p))
	#print(p)

	return p
	#sys.exit(0)


def one_step_lookahead(index, V,plant):
    #print(index)
    state = index_to_state(index)
    #print(state)

    A = np.zeros(number_u)
    #go through every action
    for n in range(number_u):
        #get action
        u = get_action(n)
        #print(u)
        #run action

        new_state = state_action(state,u,plant)
        #print(new_state)

        #convert to index
        #new_index = state_to_index(new_state)

        neighbours = get_neighbour_states(new_state)
        p = neighbour_prob(new_state,neighbours)

        A[n] = 0

        for j in range(16):
		    #if validneighbour state
		    new_index = state_to_index(neighbours[j])
		    if index_valid(new_index):
		        #print('here')
		        A[n] += p[j]*(state_score(neighbours[j]) + discount_factor * V[new_index])
		    else:
		        A[n] += p[j]*-10000

    #print(A)
    #sys.exit(0)
    return A

def value_iteration(plant):

	# start robot
    x_t, t = plant.get_plant_state()
    if plant.noise is not None:
        # randomize state
        Sx_t = np.zeros((x_t.shape[0],x_t.shape[0]))
        L_noise = np.linalg.cholesky(plant.noise)
        x_t = x_t + np.random.randn(x_t.shape[0]).dot(L_noise);

    not_converged = True

    while not_converged:
        # Stopping condition
        delta = 0
        #print(V)
        # Update each state...
        # Need indexes of array
        it = np.nditer(V, flags=['multi_index'])
        while not it.finished:
            #get state indexes (e.g. (0,1,2,3))
            i = it.multi_index
            # Do a one-step lookahead to find the best action
            #A = np.ones(7)
            A = one_step_lookahead(i, V, plant)

            #get best action
            best_action_value = np.max(A)
            # Calculate delta across all states seen so far
            delta = max(delta, np.abs(best_action_value - V[i]))
            # Update the value function. Ref: Sutton book eq. 4.10. 
            V[i] = best_action_value

            #if i == (0,0,0,0):
             #   print('Action value of first state:',V[i])

            #print(A)


            #END OF LOOP
            #go to next state index
            it.iternext();

        #print np.max(V)
        #print np.min(V)

        print delta



        # Check if we can stop
        if delta < theta:
            not_converged = False

    #sys.exit(0)
    print('converged')

    # Create a deterministic policy using the optimal value function
    print('converged')

    it = np.nditer(policy, flags=['multi_index'])
    while not it.finished:
        i = it.multi_index
        # Do a one-step lookahead to find the best action
        #A = np.ones(7)
        A = one_step_lookahead(i, V, plant)
        # One step lookahead to find the best action for this state
        best_action = np.argmax(A)
        # Always take the best action
        policy[i] = best_action

        #print(A)
        #print(best_action)

        it.iternext();

    #sys.exit(0)
    print(policy)
    #print np.max(V)
    #print np.min(V)

    
    #return policy, V

def policyfn(x):
    #print(x)
    index = state_to_index(x)
    #print(index)
    #print(np.array(([get_action(int(policy[index]))])))
    return np.array(([get_action(int(policy[index]))]))

        

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
    N = 5   
    H = 10
    
    learner_params = default_params()
    plant_params = learner_params['params']['plant'] 
    plant = learner_params['plant_class'](**plant_params)

    plant.reset_state()
    value_iteration(plant)
   
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
        #plt.savefig('plots_vi/plot_'+str(i))

        del data[:]
    
if __name__ == '__main__':
    main()
    
