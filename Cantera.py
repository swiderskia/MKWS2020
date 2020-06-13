"""
Constant volume, heater included, kinetic simulation of self-ignition.
"""
import matplotlib.pyplot as plt
import cantera as ct

# gas implementation
gas = ct.Solution('gri30.xml')
gas.TPX = 1000, 1*ct.one_atm, 'CH4:1, O2:2, N2:7.52'

# reactor to represent the cylinder filled with gas
r = ct.IdealGasReactor(gas)
r.volume = 1.0

sim = ct.ReactorNet([r])

time = 0.0  # initial time
states = ct.SolutionArray(gas, extra=['t'])

# implementation of heater that gives constant heat
heater_gas = ct.Solution('gri30.xml')
heater_gas.TPX = 1000, ct.one_atm, 'H2:2,O2:1'
heater = ct.Reservoir(heater_gas)
w = ct.Wall(heater, r, A=1.0, K=0, U=0, Q=1000000000, velocity=0)

time_step = 1.e-6

print('%10s %10s %10s %14s' % ('t [s]','T [K]','P [Pa]','u [J/kg]'))
for n in range(100):
    time += time_step
    sim.advance(time)
    states.append(r.thermo.state, t=time*1e3)
    plt.clf()

    plt.subplot(2, 2, 1)
    plt.plot(states.t, states.T)
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (K)')

    plt.subplot(2, 2, 2)
    plt.plot(states.t, states.P)
    plt.xlabel('Time (ms)')
    plt.ylabel('Pressure (Pa)')
    plt.tight_layout()

    plt.subplot(2, 2, 3)
    plt.plot(states.t, states.u)
    plt.xlabel('Time (ms)')
    plt.ylabel('Specific Internal Energy (J/kg)')

    plt.tight_layout()
    print('%10.3e %10.3f %10.3f %14.6e' % (sim.time, r.T,
                                           r.thermo.P, r.thermo.u))

plt.show()