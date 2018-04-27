import numpy as np

POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 15     # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
DELTA_T = 1/5      # years (length of time step, how frequently you look at the patient)


# Part 1: Non-stroke annual mortality rate(asprin)
a = .042
#Non-stroke annual mortality rate(Warfrin)
b = .040
#Non-stroke annual mortality rate(dabigitran)
c = .039

# Part 2: Rate of stroke (asprin)
d = .027
# Part 2: Rate of stroke (Warfrin)
e = .012

# Part 3: Rate of transition from Well state to Major Stroke state (Aspirin)
f = d*.30
#         Rate of transition from Well state to  Minor Stroke state (Aspirin)
g=
#         Rate of transition from Well state to  TIA Stroke state (Aspirin)
#         Rate of transition from Well state to  Stroke Death state (Aspirin)
h = stroke_rate*0.1

# Part 3: Rate of transition from Well state to Major Stroke state (Warfrin & Dab)
i = stroke_rate*0.9
#         Rate of transition from Well state to  Minor Stroke state (Warfrin & Dab)
j=
#         Rate of transition from Well state to  TIA Stroke state (Warfrin & Dab)
#         Rate of transition from Well state to  Stroke Death state (Warfrin & Dab)
k = stroke_rate*0.1


# Part 4: Rate of recurrent stroke (annual)
recur_stroke_rate = 2.6

# Part 5: Rate of transition from Post-stroke state to Stroke state (annual)
d = recur_stroke_rate*0.8
#         Rate of transition from Post-stroke state to Stroke Death state (annual)
e = recur_stroke_rate*0.2

# Part 6: Rate of transition from Stroke state to Post-stroke state (annual)
f = 1/(1/52)

# transition rate matrix(asprin)
TRANS_MATRIX = [
    [None,  .01107,    .0081,    .00297, .004833,       0,    .042],     # Well
    [0.0,   None,       0.0,     0.0,    0.0,           52,    0.0] ,     # Minor Stroke
    [0.0,    0.0,       None,    0.0,    0.0,           52,   0.0],    #Major Stroke
    [0.0,    0.0,       0.0,    None,    0.0,           52,   0.0] ,   #TIA
    [0.0,    0.0,       0.0,    0.0,     None,          0,    0.0],     # Stroke-Death
    [0.0,   0.028782,   0.02106,0.007722,0.0125658,   None,  0.042],   # Post-Stroke
    [0.0,   0.0,         0.0,    0.0,    0.0,           0.0,  None],  # Death
    ]


# RR of treatment in reducing incidence of stroke and stroke death while in Post-Stroke state
STROKE_RR_Warf = 0.44
STROKE_RR_110 = 1.11
STROKE_RR_150 = 0.76
# RR of treatment in increasing mortality due to bleeding
BLEEDING_RR = 1.05

# transition rate matrix (warfrin)
TRANS_MATRIX_Warfrin= [
    [None, .0051, .004824, .001092, .000984, 0, .040],  # Well
    [0.0,   None,   0.0,   0.0,    0.0,    52, 0.0],  # Minor Stroke
    [0.0,   0.0,    None,  0.0,    0.0,    52, 0.0],  # Major Stroke
    [0.0,   0.0,    0.0,   None,   0.0,    52, 0.0],  # TIA
    [0.0,   0.0,    0.0,   0.0,    None,    0, 0.0],  # Stroke-Death
    [0.0,  0.01326, 0.0125424, 0.0028392, 0.0025584, None, 0.040],  # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
]
# transition rate matrix (Dab110)
TRANS_MATRIX_DAB110 = [
    [None, .0051*STROKE_RR_110, .004824*STROKE_RR_110, .001092*STROKE_RR_110, .000984*STROKE_RR_110, 0, .040],  # Well
    [0.0,   None,   0.0,   0.0,    0.0,    52, 0.0],  # Minor Stroke
    [0.0,   0.0,    None,  0.0,    0.0,    52, 0.0],  # Major Stroke
    [0.0,   0.0,    0.0,   None,   0.0,    52, 0.0],  # TIA
    [0.0,   0.0,    0.0,   0.0,    None,    0, 0.0],  # Stroke-Death
    [0.0,  0.01326*STROKE_RR_110, 0.0125424*STROKE_RR_110, 0.0028392*STROKE_RR_110, 0.0025584*STROKE_RR_110, None, 0.040],  # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
]

# transition rate matrix (Dab150)
TRANS_MATRIX_DAB300 = [
    [None, .0051*STROKE_RR_150, .004824*STROKE_RR_150, .001092*STROKE_RR_150, .000984*STROKE_RR_150, 0, .040],  # Well
    [0.0,   None,   0.0,   0.0,    0.0,    52, 0.0],  # Minor Stroke
    [0.0,   0.0,    None,  0.0,    0.0,    52, 0.0],  # Major Stroke
    [0.0,   0.0,    0.0,   None,   0.0,    52, 0.0],  # TIA
    [0.0,   0.0,    0.0,   0.0,    None,    0, 0.0],  # Stroke-Death
    [0.0,  0.01326*STROKE_RR_150, 0.0125424*STROKE_RR_150, 0.0028392*STROKE_RR_150, 0.0025584*STROKE_RR_150, None, 0.040],  # Post-Stroke
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None],  # Death
]


#annual cost of each health state
ANNUAL_STATE_COST = [
0, #well
2470.0, #minor long term
5400.0, #major long term
625.0, #tia, short term event divided by 12
10000.0, #stroke death copied from non-stroke, nonhemmorage death below
200.0, #poststroke copied from homework
10000.0 #death
]

# annual health utility of each health state

ANNUAL_STATE_UTILITY = [
1.0, #well
0.75, #minor
0.39, #major
0.9, #tia, short term
0.0, #stroke death
0.12, #poststroke
0.0 #death
]

# annual drug costs
Anticoagulant_COST = 2000.0

# annual probability of background mortality (number per 100,000 PY)
ANNUAL_PROB_BACKGROUND_MORT = (18*100-36.2)/100000
