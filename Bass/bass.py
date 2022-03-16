"""
Python model 'bass.py'
Translated using PySD
"""

from os import TMP_MAX
from pathlib import Path
from dask.utils import tmp_cwd

from pysd.py_backend.statefuls import Integ

__pysd_version__ = "2.2.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",

    "clients concentration" : "m1",
    "competitor clients concentration" : "m2",
    "total population" : "tp",
    "potential clients" : "pc",
    "clients" : "cl",
    "competitor clients" : "comp",
    "new clients flow": "new_cl",
    "flow from potential clients to clients" : "pc_cl",
    "flow from competitor clients to clients" : "comp_cl",
    "new potential clients flow" : "new_pc",
    "flow from clients to potential clients" : "cl_pc",
    "flow from competitor clients to potential clients" : "comp_pc",
    "new competitor clients flow" : "new_comp",
    "flow from clients to competitor clients" : "cl_comp",
    "flow from potential clients to competitor clients" : "pc_comp",
    "proportion of satisfied clients of 1st comp": "p11",
    "proportion of disappointed clients of 1st comp": "p13",
    "proportion of satisfied clients of 2st comp": "p21",
    "proportion of disappointed clients of 2st comp": "p23",
    
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

_dependencies = {
    "m1" : {"cl": 1, "tp": 1},
    "m2" : {"comp": 1, "tp": 1},
    "tp" : {"cl": 1, "comp": 1, "pc": 1},
    "pc" : {"_integ_pc": 1},
    "cl" : {"_integ_cl": 1},
    "comp" : {"_integ_comp": 1},
    "new_cl" : {"pc_cl": 1, "comp_cl": 1},
    "pc_cl" : {"eff_m": 1, "pc": 1, "eff_w": 1, "rate": 1, "cl": 1, "p11": 1, "tp": 1},
    "comp_cl" : {"tr": 1, "eff_w": 1, "rate": 1, "cl": 1, "p11": 1, "comp": 1, "p21": 1, "k": 1, "p23": 1, "tp": 1},
    "new_pc" : {"cl_pc": 1, "comp_pc": 1},
    "cl_pc" : {"cl": 1, "p13": 1, "k": 1},
    "comp_pc" : {"comp": 1, "p23": 1, "k": 1},
    "new_comp" : {"pc_comp": 1, "cl_comp": 1},
    "pc_comp" : {"eff_m": 1, "pc": 1, "eff_w": 1, "rate": 1, "comp": 1, "p21": 1, "tp": 1},
    "cl_comp" : {"tr": 1, "eff_w": 1, "rate": 1, "comp": 1, "p21": 1, "cl": 1, "p11": 1, "k": 1, "p13": 1, "tp": 1},
    "rate": {},
    "eff_w": {},
    "eff_m": {},
    "k": {"eff_m": 1, "eff_w": 1},
    "tr": {"eff_m": 1, "eff_w": 1},
    "p11": {},
    "p13": {},
    "p21": {},
    "p23": {},
    "final_time": {},
    "initial_time": {},
    "saveper": {"time_step": 1},
    "time_step": {},
    "_integ_cl": {"initial": {}, "step": {"new_cl": 1}},
    "_integ_pc": {"initial": {}, "step": {"new_pc": 1}},
    "_integ_comp": {"initial": {}, "step": {"new_comp": 1}}
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 100
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return __data["time"].final_time()


def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return __data["time"].initial_time()


def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Month
    Limits: (None, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 1
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return __data["time"].time_step()


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################

def m1():
    """
    Real Name: Clients Concentration
    Original Eqn: number_of_clients / total_population
    Units: Percentage
    Limits: [0, 1]
    Type: Real

    Ratio of clients of the company to the total number of people.
    """
    return cl() / tp()

def m2():
    """
    Real Name: Competitor Clients Concentration
    Original Eqn: competittor_clients / total_population
    Units: Percentage
    Limits: [0, 1]
    Type: Real

    Ratio of clients of the competitor company to the total number of people in the system.
    """
    return comp() / tp()

def tp():
    """
    Real Name: Total Population
    Original Eqn: potential_clients + clients + competitor_clients
    Units: People
    Limits: [1e05, 1e05]
    Type: Integer

    Total number of people in the system.
    """
    return pc() + cl() + comp()

def pc():
    """
    Real Name: Potential Clients
    Original Eqn: Integ(lambda: new_pc(), lambda: 0)
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Number of potential clients for both of the companies.
    """
    return _integ_pc()

def cl():
    """
    Real Name: Clients
    Original Eqn: Integ(lambda: new_cl(), lambda: 0)
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Number of the clients of the company.
    """
    return _integ_cl()

def comp():
    """
    Real Name: Competitor Clients
    Original Eqn: Integ(lambda: new_comp(), lambda: 0)
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Number of the clients of the competitor company.
    """
    return _integ_comp()

_integ_cl = Integ(lambda: new_cl(), lambda: 0, "_integ_cl")

def new_cl():
    """
    Real Name: New Clients Flow
    Original Eqn: potential_clients_clients_flow + competitor_clients_clients_flow
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that become the clients of the company.
    """
    return pc_cl() + comp_cl()

def pc_cl():
    """
    Real Name: Potential Clients - Clients Flow
    Original Eqn: marketing_efficiency * potential_clients + wom_efficiency * talking_rate * potential_clients * clients * statisfied_clients_ratio / total_population
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that go from being potential clients to be the clients of the company.
    """
    return eff_m()*pc() + eff_w()*rate()*pc()*cl()*p11() / tp()

def comp_cl():
    """
    Real Name: Competitor Clients - Clients Flow
    Original Eqn: poaching_success * wom_efficiency * talking_rate * clients * satisfied_clients_ratio * competitor_clients * (1 - satisfied_competitor_clients_ratio - moving_people_ratio * disappointed_competitor_clients_ratio) / total_population
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that go from being competitor clients to be the clients of the company.
    """
    return tr() * eff_w() * rate() * cl() * p11() * comp() * (1-p21()-k()*p23()) / tp()


_integ_pc = Integ(lambda: new_pc(), lambda: 1e005, "_integ_pc")

def new_pc():
    """
    Real Name: New Potential Clients Flow
    Original Eqn: clients_potential_clients_flow + competitor_clients_potential_clients_flow
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that become potential clients.
    """
    return cl_pc() + comp_pc()

def cl_pc():
    """
    Real Name: Clients - Potential Clients Flow
    Original Eqn: clients * disappointed_clients_ratio * moving_people_ratio
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that go from being clients to be potential clients.
    """
    return cl() * p13() * k()

def comp_pc():
    """
    Real Name: Competitor Clients - Potential Clients Flow
    Original Eqn: competitor_clients * disappointed_competitor_clients_ratio * moving_people_ratio
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that go from being competitor clients to be potential clients.
    """
    return comp() * p23() * k()


_integ_comp = Integ(lambda: new_comp(), lambda: 0, "_integ_comp")

def new_comp():
    """
    Real Name: New Competitor Clients Flow
    Original Eqn: potential_clients_competitor_clients_flow + clients_competitor_clients_flow
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that become new competitor clients.
    """
    return pc_comp() + cl_comp()

def pc_comp():
    """
    Real Name: Potential Clients - Competitor Clients Flow
    Original Eqn: marketing_efficiency * potential_clients + wom_efficiency * talking_rate * potential_clients * competitor_clients * satisfied_competitor_clients_ratio / total_population
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that go from being potential clients for be competitor clients.
    """
    return eff_m()*pc() + eff_w()*rate()*pc()*comp()*p21() / tp()

def cl_comp():
    """
    Real Name: Clients - Competitor Clients Flow
    Original Eqn: poaching_success * wom_efficiency * talking_rate * competitor_clients * satisfied_competitor_clients_ratio * clients * (1 - satisfied_clients_ratio - moving_people_ratio * disappointed_clients_ratio) / total_population
    Units: People
    Limits: [0, 1e05]
    Type: Real

    Amount of people that become new competitor clients.
    """
    return tr()*eff_w()*rate()*comp()*p21()*cl()*(1-p11()-k()*p13())/tp()

def rate():
    """
    Real Name: Talking Rate
    Original Eqn: 100
    Units: Number
    Limits: (0, None)
    Type: constant

    Describes how often the people meet each other and talk.
    """
    return 100

def eff_w():
    """
    Real Name: Word Of Mouth Efficiency
    Original Eqn: 0.015
    Units: Percentage
    Limits: (0, None)
    Type: constant

    Percentage of cases when word of mouth brings positive results.
    """
    return 0.015

def eff_m():
    """
    Real Name: Marketing Efficiency
    Original Eqn: 0.011
    Units: Percentage
    Limits: (0, None)
    Type: constant

    Percentage of cases when marketing brings positive results.
    """
    return 0.011

def k():
    """
    Real Name: Moving People Ratio
    Original Eqn: 2 * marketing_efficiency / ( 2 * wom_efficiency + 2 * marketing_efficiency ) 
    Units: Percentage
    Limits: (0, None)
    Type: constant

    Share of dissatisfied in the market who are going to move.
    """
    return (eff_m() + eff_m()) / (eff_w() + eff_w() + eff_m() + eff_m())

def tr():
    """
    Real Name: Poaching Success
    Original Eqn: 2 * wom_efficiency / ( 2 * wom_efficiency + 2 * marketing_efficiency ) 
    Units: Percentage
    Limits: (0, None)
    Type: constant

    Describes how often the poaching brings positive results.
    """
    return (eff_w() + eff_w()) / (eff_w() + eff_w() + eff_m() + eff_m())

def p11():
    """
    Real Name: Satisfied Clients Ratio
    Original Eqn: 0.5 
    Units: Percentage
    Limits: (0, None)
    Type: constant
    """
    return 0.5

def p13():
    """
    Real Name: Disappointed Clients Ratio
    Original Eqn: 0.5 
    Units: Percentage
    Limits: (0, None)
    Type: constant
    """
    return 0.5

def p21():
    """
    Real Name: Satisfied Competitor Clients Ratio
    Original Eqn: 0.5 
    Units: Percentage
    Limits: (0, None)
    Type: constant
    """
    return 0.5

def p23():
    """
    Real Name: Disappointed Competitor Clients Ratio
    Original Eqn: 0.5 
    Units: Percentage
    Limits: (0, None)
    Type: constant
    """
    return 0.5
