# coronaW
To simulate the coronavirus impact on society using user input parameters. Rather than a purely mathematical model of exponential or logistic growth, we will use "Person" objects, which can be given different behavioral parameters, to simulate social interaction (or lack of) and thus the spread of the virus. So far, the model resembles the simulations done by 3B1B (which inspired this project). We will also implement an economical model for how quarantine may affect the individual in negative ways as well. The economical impacts of a pandemic like COVID-19 is very real at the individual level. People start to lose jobs, housing, and ultimately, happiness. We want to be able to quantify this data, and its relationship with the spread of the virus. 

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
