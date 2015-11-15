import numpy as np
import random
import copy
import matplotlib.pyplot as plt

class User(object):
    def __init__(self, ability, contribution):
        self.status = 0
        self.value = 0

        self.ability = ability
        self.cost = 0

        self.contribution = contribution
        self.utility = 0

    def updateInfo(self, contributions):
        above = sum(i >= self.contribution for i in contributions)
        self.status = float(above) / len(contributions)
        # Status function is 1-self.status

        self.value = 1 - self.status
        self.cost = float(self.contribution) / self.ability
        self.utility = self.value - self.cost

    #def calculateInfo()

    def __str__(self):
        return "ability: %d, utility: %.2f\n"%(self.ability, self.utility*100)

    __repr__ = __str__


class Model(object):
    def __init__(self, threshold=0):
        self.users = []
        self.abilities = []
        self.badges = []
        self.contributions = []
        self.threshold = threshold

    def createUsers(self, N):
        mu, sigma = 50, 30 # mean and standard deviation
        self.abilities = np.random.normal(mu, sigma, N)
        for ability in self.abilities:
            contribution = random.randint(1, N)
            self.contributions.append(contribution)
            user = User(ability, contribution)
            self.users.append(user)

    def updateUserInfo(self):
        for user in self.users:
            # update status, value, cost, and utility
            user.updateInfo(self.contributions)

    def modifyUserContribution(self):
        step = 1
        for i in range(len(self.users)):
            user = self.users[i]
            b = user.contribution
            utility_old = user.utility

            if b < user.ability:
                user.contribution += step
            elif b > user.ability:
                user.contribution -= step

            self.contributions[i] = user.contribution
            user.updateInfo(self.contributions)

            if user.utility < utility_old:
                user.contribution = b
                self.contributions[i] = b
                user.updateInfo(self.contributions)


if __name__ == "__main__":
    m1 = Model()
    m1.createUsers(30)
    m1.updateUserInfo()
    old = copy.deepcopy(m1.contributions)
    print m1.users
    print "original contributions: %.2f"%sum(m1.contributions)
    print "original utilities: %.2f"%sum(user.utility for user in m1.users)
    for n in range(50):
        m1.modifyUserContribution()
        m1.updateUserInfo()
    print m1.users
    print "final contributions: %.2f"%sum(m1.contributions)
    print "final utilities: %.2f"%sum(user.utility for user in m1.users)
    n = 0
    for i in range(len(old)):
        if m1.contributions[i] > old[i]:
            n += 1
    print "number increased contribution: %d"% n
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.legend()
    plt.scatter(m1.abilities, m1.contributions, c='r', label='Final Contributions')
    plt.scatter(m1.abilities, old, c='b', label='Initial Contributions')
    plt.legend(loc='upper left')
    plt.show()