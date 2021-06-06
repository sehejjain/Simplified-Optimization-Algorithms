
# PSO No inertia

import sys
import time
import copy
import numpy as np
from operator import attrgetter


class Particle:

    def __init__(self, bounds):
        # current solution
        self.solution = []
        for bound in bounds:
            print(bound)
            self.solution.append(np.random.uniform(bound[0], bound[1]))
        self.solution = np.array(self.solution)
        print(self.solution)
        self.pbest_value = float('inf')
        self.pbest_solution = self.solution

        self.velocity = np.zeros(len(bounds))

    def move(self):
        self.solution = self.solution + self.velocity


class PSO:

    def __init__(self, function,bounds, iterations, population, c1=2, c2=2, verbose=True, step=10):
        self.iterations = iterations  # max of iterations
        self.population = population  # size population
        self.verbose = verbose
        self.step = step
        self.progress = []
        self.score = function
        self.c1 = c1  
        self.c2 = c2

        # initialized with a group of random particles (solutions)
        particles = []

        for _ in range(population):
            particles.append(Particle(bounds))

        # checks if exists any solution
        if not particles:
            print('Initial population empty! Try run the algorithm again...')
            sys.exit(1)

        # creates the particles
        self.particles = particles

        # updates "population"
        self.population = len(self.particles)
        self.gbest_value = float('inf')

        # Set random solution as GBest
        self.gbest_solution = np.random.uniform(-10, 10, len(bounds))

    def print_particles(self):
        for particle in self.particles:
            print(particle)

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.score(particle.solution)
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.solution = particle.solution

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.score(particle.solution)
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_solution = particle.solution

    def move_particles(self):
        for particle in self.particles:
            a = particle.velocity  # No Inertia
            b = (self.c1*np.random.random()) * \
                (particle.pbest_solution - particle.solution)  # Cognitive
            c = (np.random.random()*self.c2) * \
                (self.gbest_solution - particle.solution)  # Social

            new_velocity = a+b+c
            particle.velocity = new_velocity
            particle.move()

    def run(self):

        # for each time step (iteration)
        for step in range(self.iterations):
            if self.verbose:
                if step % self.step == 0:
                    print("Iteration: ", step)
            self.set_pbest()
            self.set_gbest()
            self.progress.append(self.gbest_value)
            self.move_particles()


def func(sol):
    return sol[0]**2 + sol[1]**2

def sphere(sol):
    val = 0
    for i in range(len(sol)):
        val += sol[i] ** 2
    return val

pso = PSO(sphere, [(-5, 5), (-5, 5)], 100, 20, c1=2, c2=2)
pso.run()
print(str(pso.gbest_value)+ " at "+ str(pso.gbest_solution))