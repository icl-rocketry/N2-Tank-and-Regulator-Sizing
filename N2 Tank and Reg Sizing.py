import numpy as np
import matplotlib.pyplot as plt

#Gas Properties
gamma = 1.4
R = 296.8

#Standard gas values
Tst = 273.15
Pst = 101325
rhost = Pst/(R*Tst)

#Nitrogen Tank Parameters (in convenient units)
V_litres = 2
P_0_bar = 300
T_0_degC = 20

#Engine/Mass Flow/Propellant Properties
OF = 4
mdot_prop = 1.3
rho_fuel = 786
rho_ox = 800 #approx. average nitrous density
m_prop = 8

#Calculate 
mdot_fuel = mdot_prop*(1/(1+OF))
mdot_ox = mdot_prop*(OF/(1+OF))
Vdot_fuel = mdot_fuel/rho_fuel
Vdot_ox = mdot_ox/rho_ox
tend = m_prop/mdot_prop

#Approximate values for nitrous vapour pressures at start and end (based on empirical results)
Pox0_bar = 40
Pox1_bar = 27

#Create a vector for the time period of the burn
dt = 0.01
t = np.arange(0,tend+dt,dt)
#Create vector for nitrous tank pressure (approx. linear interp based on experimental data)
Pox = Pox0_bar + t*((Pox1_bar - Pox0_bar)/tend)
Pox = Pox*10**5 #Convert to Pa

#Regulator Parameters
P_out_bar = 50

#convert to SI units
V = V_litres/1000
P0 = P_0_bar*10**5
T0 = T_0_degC + 273.15
rho0 = P0/(R*T0)
Pout = P_out_bar*10**5

#work out initial mass of N2
m_i = P0*V/(R*T0)
#work out volumetric outlet flow profile across the burn
Vdot = Vdot_fuel + Vdot_ox*(Pout - Pox)/Pout

#RK4 ODE Solver
def RK4(t0, y0, h, tend):
    t = np.arange(t0, tend+h, h)
    y = np.ndarray((len(t)))
    y[0] = y0
    for i in range(0,len(t)-1):
        k1 = h*func(t[i],y[i])
        k2 = h*func(t[i] + 0.5*h, y[i] + 0.5*k1)
        k3 = h*func(t[i] + 0.5*h, y[i] + 0.5*k2)
        k4 = h*func(t[i] + h, y[i] + k3)
        y[i+1] = y[i] + (k1+2*k2+2*k3+k4)/6
    return t,y

#ODE for rate of change of density of N2 in the pressurant tank
def func(t,rho):
    tau = Pout*Vdot[int(t/dt)]/(R*T0*V)
    P = P0*(rho/rho0)**gamma
    if P <= Pout: #If pressurant tank pressure is below regulator outlet pressure, set flow rate to zero (not what actually happens)
        F = 0
    else:        
        F = -tau*(rho/rho0)**(1-gamma)
    return F

def cv_calc(stdVdotL, rho, T, F_L, P_i, P_o): #Find the minimum CV required for required flow rate
    q = stdVdotL*2.11888 #Convert standard flow rate to Cu ft/hr
    SG = rho/1.225 #Convert density to specific gravity (relative to room temp. air)
    T_f = ((T - 273.15) * 9/5) + 32 #convert temp. to fahrenheit
    P_i = P_i*(14.7/10**5) #convert pressures to psia
    P_o = P_o*(14.7/10**5)
    dp = P_i - P_o #calculate pressure drop
    CV = np.ndarray(len(q))
    
    for i in range(0, len(q)):
        if dp[i] > 0.47*P_i[i]:
            #Critical (choked) flow through regulator
            CV[i] = q[i]*np.sqrt(SG*(T_f[i] + 460))/(834*F_L*P_i[i])
        else:
            #non-choked flow through regulator
            CV[i] = q[i]*np.sqrt(SG*(T_f[i] + 460))/(1360*np.sqrt(dp[i]*P_o[i]))

    return CV
    
#Calculate N2 tank states using numerical ODE solver
t,rho = RK4(0,rho0,dt,tend)
P = P0*(rho/rho0)**gamma
T = P/(rho*R)

mdot = (Pout/(R*T))*Vdot #Calculate 
mdot[P<=Pout] = 0 #Remove any negative mdot values

stdVdotL = (mdot*R*Tst/Pst)*1000*60 #Convert mass flow rate to standard litres/min

F_L = 1 #Define pressure recover factor for pressure regulator
CV = cv_calc(stdVdotL, rhost, T, F_L, P, Pout) #Calculate required CV at every point

mtank = np.ndarray(len(mdot))

#Calculate mass of N2 in pressurant tank throughout burn by integrating mdot
for i in range(0, len(mdot)):    
    mtank[i] = m_i - np.trapz(mdot[0:i])*dt

#Plot results
plt.plot(t,P/10**5, label='N2 Tank')
plt.plot(t,Pox/10**5, label='Nitrous Vapour')
plt.xlabel('Time [s]')
plt.ylabel('Tank Pressure [bar]')
plt.legend()
plt.show()

plt.plot(t,T-273.15)
plt.xlabel('Time [s]')
plt.ylabel('N2 Temperature [degC]')
plt.show()

plt.plot(t,mdot)
plt.xlabel('Time [s]')
plt.ylabel('N2 Mass Flow Rate [kg/s]')
plt.show()

plt.plot(t,mtank)
plt.xlabel('Time [s]')
plt.ylabel('Mass of N2 in Tank [kg]')
plt.show()

plt.plot(t,Vdot*1000)
plt.xlabel('Time [s]')
plt.ylabel('Volumetric N2 Flow Rate [L/s]')
plt.show()

plt.plot(t,stdVdotL)
plt.xlabel('Time [s]')
plt.ylabel('Standard N2 Flow Rate [L/min]')
plt.show()

plt.plot(t,CV)
plt.xlabel('Time [s]')
plt.ylabel('Minimum Required CV')
plt.show()