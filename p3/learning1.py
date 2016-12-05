import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy

numRuns = 1
# n is total number of features
n = numTiles * 3 # numActions = 3
# gamma = 1

def learn(alpha=0.1 / numTilings, epsilon=0.0, numEpisodes=200):
    theta1 = -0.001 * rand(n)
    theta2 = -0.001 * rand(n)
    returnSum = 0.0
    for episodeNum in range(numEpisodes):
        G = 0.0
        #your code goes here (20-30 lines, depending on modularity)
        state = mountaincar.init()
        #q1 = [0] * 3 # state-action value q for each
        #q2 = [0] * 3
        #feature_vectors = np.zeros(n)

        while state != None:
            tileIndices = [-1]*numTilings
            tilecode(s[0], s[1], tileIndices) # s[0]:position s[1]:velocity
            q0 = Qs(theta1, tileIndices) + Qs(theta2, tileIndices) # if action is 0
            q1 = Qs(theta1, tileIndices+numTiles) + Qs(theta2, tileIndices+numTiles) #if action is 1
            q2 = Qs(theta1, tileIndices+numTiles*2) + Qs(theta2, tileIndices+numTiles*2) # if action is 2
            Q = np.array([q0, q1, q2])

            # apply epsilon greedy to choose actions
            greedy = np.random.random()
            if(greedy >= epsilon):
                action = Q.argmax()
            else:
                action = np.random.randint(0,3)

            reward, nextS = mountaincar.sample(state, action)
            G = G + reward

            while nextS == None: # if next state is terminal state




        print("Episode:", episodeNum, "Steps:", step, "Return: ", G)
        returnSum += G
    print("Average return:", returnSum / numEpisodes)
    return returnSum, theta1, theta2


#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data


def writeF(theta1, theta2):
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            F = [-1] * numTilings
            tilecode(-1.2 + (i * 1.7 / steps), -0.07 + (j * 0.14 / steps), F)
            height = -max(Qs(F, theta1 + theta2 / 2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()

def Qs(tileIndices, theta):
    #Write code to calculate the Q-values for all actions for the state represented by tileIndices
    Q = np.zeros(numActions)
    for a in range(numActions):
        for i in tileIndices:
            Q[i] = Q[i] + theta[i+a*4*81]
    return Q


if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    print("Overall performance: Average sum of return per run:", end="")
    print(runSum / numRuns)
