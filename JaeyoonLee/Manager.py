#!/user/bin/env python3

# Created by: Jaeyoon (Jay) Lee
# Created on: Jun 2021
# This class managing simulator.


import math
import random

import constants
from Person import Infectious, Person


class Manager:
    def __init__(self):
        self.healthPeople = self.generatePeople(
            constants.N_PEOPLE - 1, [100, 1300], [100, 700], constants.WHITE
        )
        self.infectedPeople = self.generatePeople(
            1, [650, 750], [350, 450], constants.RED, infected=True
        )
        self.deadPeople = []

    def movePerson(self, screen):
        for personIndex in range(constants.N_PEOPLE):
            person = self.separatePeople(personIndex, death=True)
            person.draw(screen)
            if person.getVelocity() != 0:
                person.move()
                if random.randint(1, constants.FPS) == constants.FPS:
                    person.setDirection(random.uniform(0, 2 * math.pi))
                if self.hitWall(
                    person.getX(),
                    person.getY(),
                    person.getDirection(),
                    constants.RADIUS,
                ):
                    person.setDirection(person.getDirection() + math.pi)

    def checkInfected(self):
        for infectious in self.infectedPeople:
            for healthCount, health in enumerate(self.healthPeople):
                healthPos = [health.getX(), health.getY()]
                infectiousPos = [infectious.getX(), infectious.getY()]
                distance = self.getDistance(healthPos, infectiousPos)
                if distance < constants.RADIUS * 2:
                    # Collide
                    newInfectious = Infectious(
                        health.getX(),
                        health.getY(),
                        health.getVelocity(),
                        health.getDirection(),
                        constants.RED,
                        infectious.getInfectionRate(),
                        infectious.getDeathRate(),
                    )
                    self.infectedPeople.append(newInfectious)
                    del self.healthPeople[healthCount]

    def checkDeath(self):
        for infectionCount, infectious in enumerate(self.infectedPeople):
            infectionRate = (
                infectious.getInfectionRate()
                * constants.FPS
                // infectious.getVelocity()
            )
            if random.randint(0, infectionRate) == 0:
                newDeath = Person(
                    infectious.getX(), infectious.getY(), 0, 0, constants.BLACK
                )
                self.deadPeople.append(newDeath)
                del self.infectedPeople[infectionCount]

    def mutateVirus(self):
        for infectious in self.infectedPeople:
            if random.randint(0, constants.MUTATE) == 0:
                infectious.mutate()

    def setSpeed(self, speed):
        for personIndex in range(self.getNumberOfLivingPeople()):
            person = self.separatePeople(personIndex)
            person.setVelocity(abs(int(speed)))

    def generatePeople(
        self, N_People, creationDomain, creationRange, colour, infected=False
    ):
        people = []
        for _ in range(N_People):
            x = random.randint(creationDomain[0], creationDomain[1])
            y = random.randint(creationRange[0], creationRange[1])
            velocity = 1
            if not infected:
                person = Person(
                    x, y, velocity, random.uniform(-math.pi, math.pi), colour
                )
            else:
                person = Infectious(
                    x, y, velocity, random.uniform(-math.pi, math.pi), colour, 20, 20
                )
            people.append(person)
        return people

    def separatePeople(self, personIndex, death=False):
        if personIndex < len(self.healthPeople):
            return self.healthPeople[personIndex]
        elif death and (personIndex >= self.getNumberOfLivingPeople()):
            return self.deadPeople[personIndex - self.getNumberOfLivingPeople()]
        return self.infectedPeople[personIndex - len(self.healthPeople)]

    def getDistance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def hitWall(self, pos_x, pos_y, direction, radius):
        if (
            pos_x - radius < 0
            and math.cos(direction) < 0
            or pos_x - radius >= 0
            and pos_x + radius > constants.WIDTH
            and math.cos(direction) > 0
        ):
            return True
        return (
            pos_y - radius < 0
            and math.sin(direction) < 0
            or pos_y - radius >= 0
            and pos_y + radius > constants.HEIGHT
            and math.sin(direction) > 0
        )

    def getHealthPeople(self):
        return self.healthPeople

    def getInfectedPeople(self):
        return self.infectedPeople

    def getDeadPeople(self):
        return self.deadPeople

    def getNumberOfHealthPeople(self):
        return len(self.healthPeople)

    def getNumberOfInfectedPeople(self):
        return len(self.infectedPeople)

    def getNumberOfDeadPeople(self):
        return len(self.deadPeople)

    def getNumberOfLivingPeople(self):
        return constants.N_PEOPLE - len(self.deadPeople)
