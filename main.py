from distributions import Distributions as dt
import random
import math

rush_hours = [(90, 210), (420, 540)]
total_min = 660
workers = [(0, 0, 0)]
clients = []

arrives = {}
times = {}
current_time = 0
cook_count = 0

def ppl_arrive(index, time):
    arrives[index] = time

def in_range(x, a):
    return a[0] <= x and x <= a[1]

def in_rush_hour(t):
    return in_range(t, rush_hours[0]) or in_range(t, rush_hours[1])

def arrive_event(i, ta, ts1, ts2, ts3, \
                    total_time, cook_count, current_time, \
                        clients, workers, Ca, testing_with_worker):
    
    if min([ta, ts1, ts2, ts3]) == ta and ta < total_time:
        current_time += ta
        Ca += 1 
        r = random.randint(0, 1)
        arrives[i] = (ta, r)

        if r: 
            # sandwish
            ts = dt.uniform(3, 5, random.random())
        else: 
            #sushi
            ts = dt.uniform(5, 8, random.random())


        if in_rush_hour(current_time) and cook_count < 3 and testing_with_worker:
            if workers[0] == 0:
                workers[0] = i
                ts1 = ts
            elif workers[1] == 0:
                workers[1] = i
                ts2 = ts
            elif workers[2] == 0:
                workers[2] = i
                ts3 = ts
            cook_count += 1
        
        elif not in_rush_hour(current_time) and cook_count < 2 and testing_with_worker:
            if workers[0] == 0:
                workers[0] = i
                ts1 = ts
            elif workers[1] == 0:
                workers[1] = i
                ts2 = ts
            cook_count += 1
        
        elif cook_count < 2 and not testing_with_worker:
            if workers[0] == 0:
                workers[0] = i
                ts1 = ts
            elif workers[1] == 0:
                workers[1] = i
                ts2 = ts
            cook_count += 1

        else:
            clients.append(i)

        return True, Ca, ts1, ts2, ts3, cook_count, current_time, clients, workers
    
    return False, Ca, ts1, ts2, ts3, cook_count, current_time, clients, workers

def ts1_leaving_event(ts1, ts2, ts3, Cp, cook_count, workers, clients: list, leaves, testing_with_extra_worker):
    if min([ts1, ts2, ts3]) == ts1:
        Cp += 1
        leaves[workers[0]] = ts1
        
        if clients:
            workers[0] = clients[0]
            clients.pop[0]
            food = arrives[workers[0]][1]
            if food: 
                # sandwish
                ts1 = dt.uniform(3, 5, random.random())
            else: 
                #sushi
                ts1 = dt.uniform(5, 8, random.random())
        else:  
            workers[0] = 0
            ts1 = math.inf
            cook_count -= 1

        return True, ts1, ts2, ts3, cook_count, workers, clients, leaves 
    return False, ts1, ts2, ts3, Cp, cook_count, workers, clients, leaves 

def ts2_leaving_event(ts1, ts2, ts3, Cp, cook_count, workers, clients: list, leaves, testing_with_extra_worker):
    if min([ts1, ts2, ts3]) == ts2:
        Cp += 1
        leaves[workers[1]] = ts2
        
        if clients:
            workers[1] = clients[0]
            clients.pop[0]
            food = arrives[workers[1]][1]
            if food: 
                # sandwish
                ts2 = dt.uniform(3, 5, random.random())
            else: 
                #sushi
                ts2 = dt.uniform(5, 8, random.random())
        else:  
            workers[1] = 0
            ts2 = math.inf
            cook_count -= 1

        return True, ts1, ts2, ts3, cook_count, workers, clients, leaves 
    return False, ts1, ts2, ts3, Cp, cook_count, workers, clients, leaves 

def ts3_leaving_event(ts1, ts2, ts3, Cp, cook_count, workers, clients: list, leaves, testing_with_extra_worker):
    if min([ts1, ts2, ts3]) == ts3:
        Cp += 1
        leaves[workers[2]] = ts3
        
        if clients:
            workers[2] = clients[0]
            clients.pop[0]
            food = arrives[workers[2]][1]
            if food: 
                # sandwish
                ts3 = dt.uniform(3, 5, random.random())
            else: 
                #sushi
                ts3 = dt.uniform(5, 8, random.random())
        else:  
            workers[0] = 0
            ts3 = math.inf
            cook_count -= 1

        return True, ts1, ts2, ts3, cook_count, workers, clients, leaves 
    return False, ts1, ts2, ts3, Cp, cook_count, workers, clients, leaves 


if __name__ == "__main__":
    ### initializing the restaurant
    arrives = {}
    cook = {}
    leaves = {}
    current_time = 0
    ts1 = math.inf
    ts2 = math.inf
    ts3 = math.inf
    Ca = 0
    Cp = 0

    workers = (0, 0, 0)
    cook_count = 0
    clients = []

    ta = current_time
    lambda_ = random.randint(2, 5)

    while True:
        ta += dt.exponential(lambda_, random.random())
        if ta < total_min:
            break
        



    while clients:
        # si cerro el restaurante pero aun hay clientes
        pass
