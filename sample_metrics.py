#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, Histogram, Counter, push_to_gateway, Summary
import random
import time

dev_gw = '54.190.53.191:9091'
vpc_gw = '54.200.98.241:9091'
count = 0
reg = CollectorRegistry()
fx_time = Histogram("fx_exection_time_seconds","How long does this run", registry=reg)
exp_cnt = Counter("Total_Exceptions","Count of Exceptions Thrown",registry=reg)
g1 = Gauge("noise_seconds","Noise output in seconds", registry=reg)


def noise():
    return random.random()

def noise10():
    return noise() * 10

def rnd10():
    return random.randint(1,10)

def counter():
    count += rnd10()
    return count


def sometimes_except():
    m = random.random()
    try:
        if m > .50:
            raise Exception("Too Big")
    except Exception:
        exp_cnt.inc()
        pass
 
@fx_time.time()
def wait():
    m = random.random()
    delay = m
    print(delay)
    time.sleep(delay)

def do_work():
    for x in range(20):
        do_waiting()
        g1.set(noise())
        push_to_gateway(vpc_gw,job="Sample_Noise",registry=reg)

    
def do_waiting():
    for x in range(10):
        wait()
        sometimes_except()

def main():
    do_work()

if __name__ == '__main__':
    main()
 
