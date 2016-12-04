import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy

numRuns = 1
n = numTiles * 3


def learn(alpha=.1 / numTilings, epsilon=0, numEpisodes=200):
    theta1 = -0.001 * rand(n)
    theta2 = -0.001 * rand(n)
    returnSum = 0.0
    for episodeNum in range(numEpisodes):
        G = 0
        S = mountaincar.init()
        while (S):
            indexList = [-1] * numTilings
            tilecode(S[0], S[1], indexList)
            indexList = np.array(indexList)
            q0 = qVal(theta1, indexList) + qVal(theta2, indexList)
            q1 = qVal(theta1, indexList + numTiles) + qVal(theta2, indexList + numTiles)
            q2 = qVal(theta1, indexList + 2 * numTiles) + qVal(theta2, indexList + 2 * numTiles)
            Q = np.array([q0, q1, q2])

            prob1 = np.random.random()
            if prob1 < epsilon:
                # explore
                A = np.random.choice([0, 1, 2])
                print("hfkjashdkjahkfjhsakhkkfshajhdkjashfkhask")
            else:
                # greedy
                A = Q.argmax()


            R, S_prime = mountaincar.sample(S, A)
            G += R

            prob2 = np.random.choice([1, 2])
            if prob2 == 1:
                theta_n = theta1
                theta_prime = theta2
            else:
                theta_n = theta2
                theta_prime = theta1
            indexList = [x + A * numTiles for x in indexList]
            qval_theta_n = qVal(theta_n, indexList)

            if not S_prime:
                for index in indexList:
                    theta_n[index] = theta_n[index] + alpha * (R - qval_theta_n)
                break

            indexList_prime = [-1] * 4
            tilecode(S_prime[0], S_prime[1], indexList_prime)
            indexList_prime = np.array(indexList_prime)

            q0_n = qVal(theta_n, indexList_prime)
            q1_n = qVal(theta_n, indexList_prime + numTiles)
            q2_n = qVal(theta_n, indexList_prime + 2 * numTiles)
            A_prime = np.array([q0_n, q1_n, q2_n]).argmax()
            q_prime_max = qVal(theta_prime, A_prime * numTiles + indexList_prime)

            for index in indexList:
                theta_n[index] = theta_n[index] + alpha * (R + q_prime_max - qval_theta_n)

            S = S_prime

        print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    return returnSum, theta1, theta2


# Additional code here to write average performance data to files for plotting...
def qVal(theta, tileIndices):
    # write your linear function approximator here (5 lines or so)
    sum1 = 0
    for index in tileIndices:
        sum1 += theta[index]
    return sum1


# You will first need to add an array in which to collect the data

def writeF(theta1, theta2):
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            height = -max(Qs(F, theta1, theta2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    print("Overall performance: Average sum of return per run:", runSum / numRuns)
