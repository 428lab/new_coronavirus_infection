# -*- coding: utf-8 -*-
import sys
import csv
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
from datetime import datetime as dt
import datetime 
from decimal import Decimal, ROUND_HALF_UP

class EstimationInfectedPeople():
    def __init__(self, ax, name, population, timestamp, accumulation, daily, latent_period = 5.5):
        self.ax1 = ax
        self.ax2 = ax.twinx()
        self.name = name
        self.population = population
        self.timestamp = timestamp
        self.accumulation =  np.array(accumulation, dtype=float)
        self.daily = np.array(daily, dtype=float)
        self.max = len(timestamp)
        self.dt = 0.01
        self.time = np.arange(0, self.max, self.dt)
        self.initParams = [self.population,0,np.min(self.accumulation[np.nonzero(self.accumulation)]),0]
        self.latent_period = latent_period


    def SEIR(self,v,time,rate_of_infection,infection_period):
        #return [-rate_of_infection*v[0]*v[2], rate_of_infection*v[0]*v[2]-(1/self.latent_period)*v[1],(1/self.latent_period)*v[1]-(1/infection_period)*v[2],(1/infection_period)*v[2]]
        return [-rate_of_infection*v[0]*v[2], rate_of_infection*v[0]*v[2]-(1/self.latent_period)*v[1],(1/self.latent_period)*v[1]-(1/infection_period)*v[2],(1/infection_period)*v[2]]

    def estimate(self, initialParams,rate_of_infection,infection_period):
        v=odeint(self.SEIR,initialParams,self.time,args=(rate_of_infection,infection_period))
        est=v[0:int(self.max/self.dt):int(1/self.dt)]
        return est[:,2]

    def y(self, params):
        est_i=self.estimate(self.initParams,params[0],params[1])
        return np.sum(est_i-self.daily*np.log(est_i))

    def getRandLP(self):
        a = random.normalvariate(self.lp, 5)
        if a < 0:
            a *= -1
        return self.lp

    def getEstimatedParams(self):
        self.estimatedParams = minimize(self.y,[0.00001,4.0],method="nelder-mead")
        return self.estimatedParams

    def plot(self, estimatedParams):
        handler1, label1 = self.plot_total()
        handler2, label2 = self.plot_daily()
        handler3, label3 = self.plot_estimation(estimatedParams)
        self.ax1.set_xlabel('Date',fontsize=20)
        self.ax1.set_xticklabels(timestamp, fontsize=18, rotation=0)
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        self.ax1.set_title(self.name,fontsize=25)
        self.ax1.grid()
        self.ax1.legend(handler1 + handler3 , label1 + label3 , loc=2, borderaxespad=0. , fontsize=30)

    def plot_total(self):
        self.ax1.plot(self.timestamp, self.accumulation, color='b', label="Total")
        self.ax1.set_ylabel('Total # of infected people',fontsize=20)
        self.ax1.set_xlim(self.timestamp[0], self.timestamp[-1]) 
        self.ax1.set_ylim(0, ) 
        return ax.get_legend_handles_labels()

    def plot_daily(self):
        self.ax2.bar(self.timestamp, self.daily, color='y', label="Daily")
        self.ax2.set_ylabel('Daily infections',fontsize=20)
        self.ax2.set_xlim(self.timestamp[0], self.timestamp[-1]) 
        self.ax2.set_ylim(0, max(self.daily)*1.5) 
        #self.ax2.set_ylim(0, max(self.daily)) 
        return self.ax2.get_legend_handles_labels()

    def plot_estimation(self, estimatedParams):
        self.ax2.plot(self.timestamp, self.estimate(self.initParams,estimatedParams.x[0],estimatedParams.x[1]),color='r',label="Estimation(daily)",linewidth=6.0)
        return self.ax2.get_legend_handles_labels()

    def print_estimation(self, estimatedParams):
        print('<<' + self.name + '>>')
        print('rate of infection:', Decimal(estimatedParams.x[0]).quantize(Decimal('.00000000'),rounding=ROUND_HALF_UP))
        #print('latent period   :', self.latent_period)
        print('Infection period :', Decimal(estimatedParams.x[1]).quantize(Decimal('.00000000'),rounding=ROUND_HALF_UP))

    def save_plot(self):
        output = 'new_coronavirus_' + self.name + '.png'
        plt.savefig(output) 


def read_csv(filename):
    accumulation = {}
    daily = {}
    timestamp = []
    pre_value = {}
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            for cnt, name in enumerate(header):
                if name not in pre_value:
                    pre_value[name] = 0
                if name not in accumulation:
                    accumulation[name] = []
                if name not in daily:
                    daily[name] = []
                if name == 'timestamp':
                    timestamp.append(dt.strptime(row[cnt], '%Y-%m-%d'))
                else:
                    value = int(row[cnt])
                    accumulation[name].append(value)
                    daily[name].append(value - pre_value[name])
                    pre_value[name] = value
    return timestamp, accumulation, daily


if __name__ == '__main__':

    ############################################################
    # Read csv file 
    ############################################################
    args = sys.argv
    filename = args[1]
    timestamp, accumulation, daily = read_csv(filename)

    #fig = plt.figure()
    fig = plt.figure(figsize=(20,10),dpi=200)
    fig.suptitle('Infections of a new coronavirus', fontsize=30)

    ############################################################
    # Estimation for infected People in China and visualization
    ############################################################
    ax = fig.add_subplot(1, 1, 1)
    China = EstimationInfectedPeople(ax, 'China', 58500000, timestamp, accumulation['China'], daily['China'])
    estParams = China.getEstimatedParams()
    China.print_estimation(estParams)
    China.plot(estParams)
    China.save_plot()
    plt.close()

    #fig = plt.figure()
    fig = plt.figure(figsize=(20,10),dpi=200)
    fig.suptitle('Infections of a new coronavirus', fontsize=30)
    ############################################################
    # Estimation for infected People in Japan and visualization
    ############################################################
    ax = fig.add_subplot(1, 1, 1)
    Japan = EstimationInfectedPeople(ax, 'Japan', 12000000, timestamp, accumulation['Japan'], daily['Japan'])
    estParams = Japan.getEstimatedParams()
    Japan.print_estimation(estParams)
    Japan.plot(estParams)
    Japan.save_plot()
    plt.close()

