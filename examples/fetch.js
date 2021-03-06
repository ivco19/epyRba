var data = {
    'Time_to_death': 17,
    'fact_futuro': 0.5,
    'D_incbation': 5.2,
    'D_infectious': 2.9,
    'R0': 3.422,
    'R0p': 3.422,
    'D_recovery_mild': 5.1,
    'D_recovery_severe': 10.1,
    'D_hospital_lag': 5,
    'retardo': 4,
    'D_death': 14.1,
    'p_fatal': 0.021,
    'InterventionTime': 18,
    'InterventionAmt': 1,
    'p_severe': 0.2,
    'E0': 17,
    'duration': 30,
    'N': 440000,
    'I0': 1,
    'timepoints': [0, 1, 2, 3, 4]
}


// or wathever you deployed epyrba
var URL = "https://epyrba.herokuapp.com/seir";

fetch(URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: "query=" + JSON.stringify(data)
}).then(res => {
    if(!res.ok)
        throw new Error('Error en backend!');
    return res;
}).then(data => {
    data.text().then(text => {
        alert(text);
    });
}).catch(err => {
    throw new Error('Error!!');
});
