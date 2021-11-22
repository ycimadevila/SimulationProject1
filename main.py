from distributions import Distributions as dt
import random
import math

rush_hours = [(90, 210), (420, 540)]
total_min = 660
workers = [(0, 0, 0)]
clients = []

arrives = {}
on_kitchen = {}
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
                        clients, workers, Ca, on_kitchen, testing_with_worker):
    # if min([ta, ts1, ts2, ts3]) == ta:
    current_time = ta
    Ca += 1 
    r = random.randint(0, 1)
    arrives[i] = (ta, r)

    lt = current_time

    if r: 
        # sandwish
        ts = current_time + dt.uniform(3, 5, random.random())
    else: 
        #sushi
        ts = current_time + dt.uniform(5, 8, random.random())

    # print(f'-------------------> entre con {i}')#,{ts - current_time},  {current_time}, {ta}, {ts1}, {ts2}, {ts3}, {workers}, {cook_count}')
    
    if in_rush_hour(current_time) and cook_count < 3 and testing_with_worker:
        
        if clients:
            # print(f'entre con {clients[0]}')
            if workers[0] == 0:
                clients.append(i)
                item = clients.pop(0)
                workers[0] = item
                food = arrives[workers[0]][1]
                if food: 
                    # sandwish
                    ts = current_time + dt.uniform(3, 5, random.random())
                else: 
                    #sushi
                    ts = current_time + dt.uniform(5, 8, random.random())
                on_kitchen[workers[0]] = current_time
                ts1 = ts
            elif workers[1] == 0:
                clients.append(i)
                item = clients.pop(0)
                workers[1] = item
                food = arrives[workers[1]][1]
                if food: 
                    # sandwish
                    ts = current_time + dt.uniform(3, 5, random.random())
                else: 
                    #sushi
                    ts = current_time + dt.uniform(5, 8, random.random())
                on_kitchen[workers[1]] = current_time
                ts2 = ts
            elif workers[2] == 0:
                clients.append(i)
                item = clients.pop(0)
                workers[2] = item
                food = arrives[workers[2]][1]
                if food: 
                    # sandwish
                    ts = current_time + dt.uniform(3, 5, random.random())
                else: 
                    #sushi
                    ts = current_time + dt.uniform(5, 8, random.random())
                on_kitchen[workers[2]] = current_time
                ts3 = ts
            cook_count += 1

        else:
            # print(f'entre a 3 con {i}')
            if workers[0] == 0:
                workers[0] = i
                ts1 = ts
            elif workers[1] == 0:
                workers[1] = i
                ts2 = ts
            elif workers[2] == 0:
                workers[2] = i
                ts3 = ts
            on_kitchen[i] = ts
            cook_count += 1
        # print(f'entro {i}')
    
    elif not in_rush_hour(current_time) and cook_count < 2 and testing_with_worker:
        if workers[0] == 0:
            workers[0] = i
            ts1 = ts
        elif workers[1] == 0:
            workers[1] = i
            ts2 = ts
        cook_count += 1
        on_kitchen[i] = ts
        # print(f'entro {i}')
    
    elif cook_count < 2 and not testing_with_worker:
        if workers[0] == 0:
            workers[0] = i
            ts1 = ts
        elif workers[1] == 0:
            workers[1] = i
            ts2 = ts
        cook_count += 1
        on_kitchen[i] = ts
        # print(f'entro {i}')

    else:
        clients.append(i)
        # print(f'le hice append a {i}')

    # print(workers)

    return True, Ca, ts1, ts2, ts3, cook_count, current_time, clients, workers, on_kitchen

def ts1_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients: list, leaves,  on_kitchen):
    # print(f'_______________________evento 1 sali con {workers[0]} {workers}{current_time} {ts1} {ts2} {ts3}')
    Cp += 1
    current_time = ts1
    leaves[workers[0]] = current_time
    
    if clients:
        workers[0] = clients[0]
        clients.pop(0)
        food = arrives[workers[0]][1]
        if food: 
            # sandwish
            ts1 = current_time + dt.uniform(3, 5, random.random())
        else: 
            #sushi
            ts1 = current_time + dt.uniform(5, 8, random.random())
        on_kitchen[workers[0]] = current_time
    else:  
        workers[0] = 0
        ts1 = math.inf
        cook_count -= 1

    return True, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves 

def ts2_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients: list, leaves, on_kitchen):
    
    # print(f'_______________________evento 2 sali con {workers[1]} {workers}  {current_time} {ts1} {ts2} {ts3}')
    Cp += 1
    current_time = ts2
    leaves[workers[1]] = current_time 
    
    if clients:
        workers[1] = clients[0]
        clients.pop(0)
        food = arrives[workers[1]][1]
        if food: 
            # sandwish
            ts2 = current_time + dt.uniform(3, 5, random.random())
        else: 
            #sushi
            ts2 = current_time + dt.uniform(5, 8, random.random())
        
        on_kitchen[workers[1]] = current_time
    else:  
        workers[1] = 0
        ts2 = math.inf
        cook_count -= 1

    return True, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves 
    return False, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves 

def ts3_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients: list, leaves, in_rush_hour, on_kitchen):
    
    # print(f'_______________________evento 3 sali con {workers[2]} {workers}  {current_time} {ts1} {ts2} {ts3}')
    Cp += 1
    current_time = ts3
    leaves[workers[2]] = current_time
    
    if clients:
        if in_rush_hour:
            workers[2] = clients[0]
            clients.pop(0)
            food = arrives[workers[2]][1]
            if food: 
                # sandwish
                ts3 = current_time + dt.uniform(3, 5, random.random())
            else: 
                #sushi
                ts3 = current_time + dt.uniform(5, 8, random.random())
        
            on_kitchen[workers[2]] = current_time
            return True, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves 
        
    workers[2] = 0
    ts3 = math.inf
    cook_count -= 1

    return True, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves 


if __name__ == "__main__":
    means = []
    verbose = 0
    for _ in range(1000):
        withcooker = 0
        withoutcooker = 0
        
        ### initializing the kitchen without an extra cooker
        arrives = {}
        leaves = {}
        on_kitchen = {}
        current_time = 0
        ts1 = math.inf
        ts2 = math.inf
        ts3 = math.inf
        Ca = 0
        Cp = 0
        i = 1

        workers = [0, 0, 0]
        cook_count = 0
        clients = []

        ta = current_time
        testing_with_worker = 0

        ##############################################
        current = 0
        _ta = [0]
        __ta = [-1]
        while True:
            if not in_rush_hour(current):
                current += dt.exponential(1, random.random())
                __ta.append(0)
            else:
                current += dt.exponential(4, random.random())
                __ta.append(1)

            if current > total_min:
                break

            _ta.append(current)

        ########################
        while i != len(_ta):
            m = min(_ta[i], ts1, ts2, ts3)

            if m == _ta[i]:
                status, Ca, ts1, ts2, ts3, cook_count, current_time, clients, workers, on_kitchen = \
                    arrive_event(i, _ta[i], ts1, ts2, ts3, \
                            total_min, cook_count, current_time, \
                                clients, workers, Ca, on_kitchen, testing_with_worker)
                i += 1
            elif m == ts1:
                s1, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts1_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            elif m == ts2:
                s2, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts2_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            else:
                s3, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts3_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves, \
                        in_rush_hour(current_time), on_kitchen)

        while clients or workers != [0, 0, 0]:
            m = min(ts1, ts2, ts3)

            if m == ts1:
                s1, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts1_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            elif m == ts2:
                s2, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts2_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            else:
                s3, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts3_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves, \
                        in_rush_hour(current_time), on_kitchen)
            
        
        for a in range(len(_ta) - 1):
            on_kitchen[a + 1]
            arrives[a + 1][0]
            if on_kitchen[a + 1] - arrives[a + 1][0] >= 5:
                withoutcooker += 1
        
        ### initializing the kitchen with an extra cooker
        arrives = {}
        leaves = {}
        on_kitchen = {}
        current_time = 0
        ts1 = math.inf
        ts2 = math.inf
        ts3 = math.inf
        Ca = 0
        Cp = 0
        i = 1

        workers = [0, 0, 0]
        cook_count = 0
        clients = []

        ta = current_time
        lambda_ = random.randint(2, 5)
        testing_with_worker = 1
    
        while i != len(_ta):
            m = min(_ta[i], ts1, ts2, ts3)

            if m == _ta[i]:
                # print(f'entre a arrive, {(_ta[i], ts1, ts2, ts3)} {workers}')
                status, Ca, ts1, ts2, ts3, cook_count, current_time, clients, workers, on_kitchen = \
                    arrive_event(i, _ta[i], ts1, ts2, ts3, \
                            total_min, cook_count, current_time, \
                                clients, workers, Ca, on_kitchen, testing_with_worker)
                i += 1
            elif m == ts1:
                # print(f'entre a ts1 {(_ta[i], ts1, ts2, ts3)} {workers}')
                s1, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts1_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            elif m == ts2:
                # print(f'entre a ts2 {(_ta[i], ts1, ts2, ts3)} {workers}')
                s2, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts2_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            else:
                # print(f'entre a ts3 {(_ta[i], ts1, ts2, ts3)} {workers}')
                s3, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts3_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves, \
                        in_rush_hour(current_time), on_kitchen)

        while clients or workers != [0, 0, 0]: #ts1 != math.inf and ts2 != math.inf and ts3 != math.inf:
            m = min(ts1, ts2, ts3)

            if m == ts1:
                # print(f'entre a ts1 {(ts1, ts2, ts3)} {workers}')
                s1, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts1_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            elif m == ts2:
                # print(f'entre a ts2 {(ts1, ts2, ts3)} {workers}')
                s2, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts2_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, \
                        leaves, on_kitchen)
            
            else:
                # print(f'entre a ts3 {(ts1, ts2, ts3)} {workers}')
                s3, ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves = \
                    ts3_leaving_event(ts1, ts2, ts3, Cp, current_time, cook_count, workers, clients, leaves, \
                        in_rush_hour(current_time), on_kitchen)
    
        for a in range(len(_ta) - 1):
            try:
                on_kitchen[a + 1]
            except KeyError as e:
                print(str(e), type(str(e)))
                print('was it in rudh hour?', __ta[int(str(e))])
                print(len(_ta))
                print(on_kitchen.keys())
                print(arrives.keys())
                print(leaves.keys())
            if on_kitchen[a + 1] - arrives[a + 1][0] >= 5:
                withcooker += 1
        
        if verbose:
            print('number of customers who waited more than 5 minutes with one more cook during rush hour:', withcooker * 100 / (len(_ta)- 1), '%')
            print('number of customers who waited more than 5 minutes without one more cook during rush hour:', withoutcooker * 100 / (len(_ta)- 1), '%')
            print('total number of customers:', len(arrives))
                
            rh = 0
            nrh = 0
            for i in __ta:
                if i: rh +=1
                else: nrh +=1
            
            print('number of customers in rush hour:', rh)
            print('number of customers in normal time:', nrh)
        if len(arrives) != 0:
            means.append((withoutcooker - withcooker) * 100 / len(arrives))
    print('After finding the mean of all the percentages obtained from the simulations, the conclusion is that the mean is:', sum(means) / len(means))