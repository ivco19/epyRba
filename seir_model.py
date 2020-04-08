# This file is part of the
#   Arcovid19 (https://ivco19.github.io/).
# Copyright (c) 2020, Arcovid Team
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/epyRba/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"Backend and mini-frontend for Epicalc in Python an R"

# =============================================================================
# IMPORTS
# =============================================================================
from collections import namedtuple

import numpy as np 
import pandas as pd

from scipy.integrate import solve_ivp

# =============================================================================
# LOGIC
# =============================================================================

Vars = namedtuple('Variables', ['S', 'E', 'I', 'Mild', 'Severe', 'Severe_H',
                                'Fatal', 'R_Mild', 'R_Severe', 'R_Fatal'])

Pars = namedtuple('Parameters',
                  ['Time_to_death', 'D_incbation', 'D_infectious', 'R0',
                   'R0p', 'D_recovery_mild', 'D_recovery_severe',
                   'D_hospital_lag', 'retardo', 'D_death', 'p_fatal',
                   'InterventionTime', 'InterventionAmt', 'p_severe',
                   'duration', 'N', 'I0', 'E0'])

Derivs = namedtuple('Derivatives',
                    ['dS', 'dE', 'dI', 'dMild', 'dSevere', 'dSevere_H',
                     'dFatal', 'dR_Mild', 'dR_Severe', 'dR_Fatal'])


def seir_model(t, state_values, pars):
    # init parameters, named tuple with the following order
    S        = state_values[0]   # susceptibles
    E        = state_values[1]   # exposed
    I        = state_values[2]   # infectious
    Mild     = state_values[3]   # Recovering (Mild)
    Severe   = state_values[4]   # Recovering (Severe at home)
    Severe_H = state_values[5]   # Recovering (Severe in hospital)
    Fatal    = state_values[6]   # Recovering (Fatal)
    R_Mild   = state_values[7]   # Recovered
    R_Severe = state_values[8]   # Recovered
    R_Fatal  = state_values[9]  # Dead

    # pars is also a named tuple
    gamma = 1.0 / pars.D_infectious
    a     = 1.0 / pars.D_incbation

    totalTime = pars.InterventionTime + pars.retardo

    if 0 < (t - totalTime) < pars.duration:
        beta = pars.InterventionAmt * pars.R0 * gamma

    elif t - totalTime >  pars.duration:
        beta = pars.R0p * gamma
    else: 
        beta = pars.R0 * gamma

    # compute derivatives
    p_mild   = 1.0 - pars.p_severe - pars.p_fatal
    return np.array(Derivs(
        dS        = -beta * I * S,
        dE        =  beta * I * S - a * E,
        dI        =  a * E - gamma * I,
        dMild     =  p_mild * gamma * I - \
                        (1.0 / pars.D_recovery_mild) * Mild,
        dSevere   =  pars.p_severe * gamma * I - \
                        (1.0 / pars.D_hospital_lag) * Severe,
        dSevere_H =  (1.0 / pars.D_hospital_lag) * Severe - \
                        (1.0 / pars.D_recovery_severe) * Severe_H,
        dFatal    =  pars.p_fatal * gamma * I - \
                        (1.0 / pars.D_death) * Fatal,
        dR_Mild   =  (1.0 / pars.D_recovery_mild) * Mild,
        dR_Severe =  (1.0 / pars.D_recovery_severe) * Severe_H,
        dR_Fatal  =  (1.0 / pars.D_death) * Fatal
    ))


#for debuggin in a R console, not used in the backend
def get_def_params():
    D_incbation   = 5.2
    D_infectious0 = 2.9
    Time_to_death = 17
    return np.array(Pars(
        Time_to_death     = Time_to_death,
        D_incbation       = D_incbation,
        D_infectious      = D_infectious0,
        R0                = 3.422,
        R0p               = 3.422,
        D_recovery_mild   = (8 - D_infectious0),
        D_recovery_severe = (13 - D_infectious0),
        D_hospital_lag    = 5,
        retardo           = 4,
        D_death           = Time_to_death - D_infectious0,
        p_fatal           = 0.021,
        InterventionTime  = 18,
        InterventionAmt   = 1.0 / 3.0,
        p_severe          = 0.2,
        duration          = 30,
        N                 = 44.0e4,
        I0                = 1,
        E0                = 17
    ))

#json es el data frame de parametros, salida de fromJSON() o de get_def_params()
def get_ic(df):
    I0 = df['I0'][0]   # infectious hosts
    E0 = df['E0'][0]
    N  = df['N'][0]
    
    initial_values = Vars(
        S        = 1.0, #S0/(N-E0-I0),
        E        = E0 / (N - E0 - I0),
        I        = I0 / (N - E0 - I0),
        Mild     = 0,
        Severe   = 0,
        Severe_H = 0,
        Fatal    = 0,
        R_Mild   = 0,
        R_Severe = 0,
        R_Fatal  = 0
        )
    return(np.array(initial_values))

def get_pars(df):
    parsed = df[list(Pars._fields)].drop_duplicates()

    pars = Pars(
        Time_to_death=parsed.Time_to_death[0],
        D_incbation=parsed.D_incbation[0],
        D_infectious=parsed.D_infectious[0],
        R0=parsed.R0[0],
        R0p=parsed.R0p[0],
        D_recovery_mild=parsed.D_recovery_mild[0],
        D_recovery_severe=parsed.D_recovery_severe[0],
        D_hospital_lag=parsed.D_hospital_lag[0],
        retardo=parsed.retardo[0],
        D_death=parsed.D_death[0],
        p_fatal=parsed.p_fatal[0],
        InterventionTime=parsed.InterventionTime[0],
        InterventionAmt=parsed.InterventionAmt[0],
        p_severe=parsed.p_severe[0],
        duration=parsed.duration[0],
        N=parsed.N[0],
        I0=parsed.I0[0],
        E0=parsed.E0[0]
    )
    return(pars)

fields = ['Día', 'Susceptible','Expuesto','Infeccioso',
          'Recuperándose (caso leve)','Recuperándose (caso severo en el hogar)',
          'Recuperándose (caso severo en el hospital)','Recuperándose (caso fatal)',
          'Recuperado (caso leve)','Recuperado (caso severo)','Fatalidades']

def integrator(json_post, outfile=None):
    """
    Integrator of the SEIR model.

    Takes a JSON file, coming from a web post.
    Dumps a solution into the output csv file, 
    if not specified this is located into ./exports/results.csv
    """
    df = pd.read_json(json_post)
    initial_values = get_ic(df)
    parameters = get_pars(df)
    t0 = np.min(df.timepoints)
    tf = np.max(df.timepoints)
    
    model = lambda t, y: seir_model(t, y, parameters)

    output = solve_ivp(model, (t0, tf), initial_values, 
                       method='LSODA',
                       t_eval=df.timepoints.values,
                       rtol=1e-6)
    t_out = output['t']
    y_out = output['y'] * df.N[0]
    messg = output['message']
    stat  = output['status']
    success = stat >= 0
    
    results = pd.DataFrame({'Día': t_out})
    for i_field, afield in enumerate(fields[1:]):
        results[afield] = y_out[i_field]
    
    if outfile is None:
        outfile = 'exports/results.csv'
    results.to_csv(outfile, index=False)


if __name__=='__main__':
    from clize import run
    run(integrator)
    