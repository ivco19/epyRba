library(minpack.lm)
library (deSolve) 
library('rjson')

 seir_model = function (t, state_values, parameters)
 {
 
   # create state variables (local variables)
 
   S        = state_values[1]   # susceptibles
   E        = state_values[2]   # exposed
   I        = state_values[3]   # infectious
   Mild     = state_values[4]   # Recovering (Mild)     
   Severe   = state_values[5]   # Recovering (Severe at home)
   Severe_H = state_values[6]   # Recovering (Severe in hospital)
   Fatal    = state_values[7]   # Recovering (Fatal)
   R_Mild   = state_values[8]   # Recovered                       
   R_Severe = state_values[9]   # Recovered
   R_Fatal  = state_values[10]  # Dead
 
   with ( 
     as.list (parameters),     # variable names within parameters can be used 
 
          {
      
            gamma=1.0/D_infectious
            a    =1.0/D_incbation
	    if ((t > InterventionTime+retardo) && t < (InterventionTime+retardo + duration))
	    {
                 beta = (InterventionAmt)*R0*gamma
            } 
	    else if(t > InterventionTime+retardo + duration)
	    {
	         beta = R0p*gamma
	    } 
	    else 
	    {
	         beta = R0*gamma
            }
      	    # compute derivatives
 
            p_mild   = 1.0 - p_severe -p_fatal

            dS        = -beta*I*S
            dE        =  beta*I*S - a*E
            dI        =  a*E - gamma*I
            dMild     =  p_mild*gamma*I   - (1.0/D_recovery_mild)*Mild
            dSevere   =  p_severe*gamma*I - (1.0/D_hospital_lag)*Severe
            dSevere_H =  (1.0/D_hospital_lag)*Severe - (1.0/D_recovery_severe)*Severe_H
            dFatal    =  p_fatal*gamma*I  - (1.0/D_death)*Fatal
            dR_Mild   =  (1.0/D_recovery_mild)*Mild
            dR_Severe =  (1.0/D_recovery_severe)*Severe_H
            dR_Fatal  =  (1.0/D_death)*Fatal

  
 
            # combine results
 
            results = c (dS,dE,dI,dMild,dSevere,dSevere_H,
                         dFatal,dR_Mild,dR_Severe,dR_Fatal)
 
            list(results)
          }
     )
 }

 ## devuelve un data.frame con los parámetros por defaul json tiene que tener estos tags con valores
 ## numéricos, salvo timepoints que es un array
 get_def_params <- function()
 {
    D_incbation       = 5.2
    D_infectious0      = 2.9
    Time_to_death     = 17

    list(
        Time_to_death     = Time_to_death,
        fact_futuro =0.5,
        D_incbation       = D_incbation,
        D_infectious      =D_infectious0,
        R0                   = 3.422,
        R0p                  = 3.422,
        D_recovery_mild      = (8 - D_infectious0),  
        D_recovery_severe    = (13 - D_infectious0),
        D_hospital_lag       = 5,
        retardo              = 4, 
        D_death              = Time_to_death - D_infectious0,
        p_fatal              = 0.021, 
        InterventionTime     = 18,  
        InterventionAmt      = 1.0/3.0,
        p_severe             = 0.2,
        duration             = 30,
        N = 44.0e4,
        I0                = 1,   
        timepoints = seq (0, 50, by=1)
    )
 }

 #json es el data frame de parametros, salida de fromJSON() o de get_def_params()
 get_ic <-function(json)
 {
            I0 = json$I0   # infectious hosts
            initial_values = c(
                 S= 1.0, #S0/(N-E0-I0),
                 E=E0/(N-E0-I0),
                 I=I0/(N-E0-I0),
                 Mild=0,
                 Severe=0,
                 Severe_H=0,
                 Fatal=0,
                 R_Mild=0,
                 R_Severe=0,
                 R_Fatal=0
            ) 
    return(initial_values)
 }

 integrador <-function(args)
 {

         json <- fromJSON(args)
	 #json is list

            parameter_list = c (
                      D_incbation       = json$D_incbation,
                      D_infectious      = json$D_infectious,
                      R0                = json$R0,
                      R0p               = json$R0*fact_futuro, 
                      D_recovery_mild   = json$D_recovery_mild,
                      D_recovery_severe = json$D_recovery_severe,
                      D_hospital_lag    = json$D_hospital_lag,
                      D_death           = json$D_death,
                      p_fatal           = json$p_fatal,
                      InterventionTime  = json$InterventionTime,
                      retardo           = json$retardo,
                      InterventionAmt   = json$InterventionAmt, #cuarentena sin efecto
                      p_severe          = json$p_severe,
                      duration          = json$duration
            )
          
            initial_values=get_ic(json)
            output = lsoda (initial_values, json$timepoints, seir_model, parameter_list)
	    res <- textConnection("foo1", "w") 
            write.csv(output, res) 
            textConnectionValue(res)
	    #devuelbe plain text csv
 }

 #args es json
 args <- commandArgs(trailingOnly = TRUE)
 integrador(args)
