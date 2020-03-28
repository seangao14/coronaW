# coronaW
corona

all may be subject to change

Each person object will have simulated variables:
  - position xy,  
  - velocity xy,  
  - accel xy,  
  - state (healthy (susceptible), infected, immune, asympomatic carrier, dead, etc..)
  
Each object will also have user input variables:
  - radius of infection,  
  - rate of infection - (inputted as probability per second, will be calculated as probability per tick using Poisson(?) distribution),  
  - distance of social distancing (at what distance will each person start accelerating the other way),
  - "rate" of social distancing (how fast the acceleration will change)
