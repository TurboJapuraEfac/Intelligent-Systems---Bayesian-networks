from BayesNetwork import *

def defStrucAndProbability():
    structure = {
        "variables": {
            "Burglary": ["True", "False"],
            "Earthquake": ["True", "False"],
            "Alarm": ["True", "False"],
            "JohnCalls": ["True", "False"],
            "MaryCalls": ["True", "False"]
        },
        "dependencies": {
            "Alarm": ["Burglary", "Earthquake"],
            "JohnCalls": ["Alarm"],
            "MaryCalls": ["Alarm"]
        }
    }

    values = {
        "prior_probabilities": {
            "Burglary": {
                "True": 0.001,
                "False": 0.999
            },
            "Earthquake": {
                "True": 0.002,
                "False": 0.998
            }
        },
        "conditional_probabilities": {
            "Alarm": [
                {
                    "Burglary": "True",
                    "Earthquake": "True",
                    "own_value": "True",
                    "probability": 0.95
                },
                {
                    "Burglary": "True",
                    "Earthquake": "True",
                    "own_value": "False",
                    "probability": 0.05
                },
                {
                    "Burglary": "False",
                    "Earthquake": "True",
                    "own_value": "True",
                    "probability": 0.29
                },
                {
                    "Burglary": "False",
                    "Earthquake": "True",
                    "own_value": "False",
                    "probability": 0.71
                },
                {
                    "Burglary": "True",
                    "Earthquake": "False",
                    "own_value": "True",
                    "probability": 0.94
                },
                {
                    "Burglary": "True",
                    "Earthquake": "False",
                    "own_value": "False",
                    "probability": 0.06
                },
                {
                    "Burglary": "False",
                    "Earthquake": "False",
                    "own_value": "True",
                    "probability": 0.001
                },
                {
                    "Burglary": "False",
                    "Earthquake": "False",
                    "own_value": "False",
                    "probability": 0.999
                }
            ],
            "JohnCalls": [
                {
                    "Alarm": "True",
                    "own_value": "True",
                    "probability": 0.9
                },
                {
                    "Alarm": "True",
                    "own_value": "False",
                    "probability": 0.1
                },
                {
                    "Alarm": "False",
                    "own_value": "True",
                    "probability": 0.05
                },
                {
                    "Alarm": "False",
                    "own_value": "False",
                    "probability": 0.95
                }
            ],
            "MaryCalls": [
                {
                    "Alarm": "True",
                    "own_value": "True",
                    "probability": 0.7
                },
                {
                    "Alarm": "True",
                    "own_value": "False",
                    "probability": 0.3
                },
                {
                    "Alarm": "False",
                    "own_value": "True",
                    "probability": 0.01
                },
                {
                    "Alarm": "False",
                    "own_value": "False",
                    "probability": 0.99
                }
            ]
        }
    }

    return structure, values


if __name__ == "__main__":
    structure, values = defStrucAndProbability()
    noofParams = int(input('Input No of outcomes for the 2nd Term : '))

    print('1st Term values:\n\tAlarm\n\tJohnCalls\n\tMaryCalls')
    firstTerm = input('Enter the 1st Term: ')
    if firstTerm not in ['Alarm', 'JohnCalls', 'MaryCalls']:
        print('Invalid input please try again')
        exit(-1)
   
    secondTerm = None
    print('Possible 2nd Term values:\n\tAlarm\n\tBurglary\n\tEarthquake')
    queries = {
        "given": {},
        "tofind": {
            firstTerm: "True"
        }
    }
    for i in range(noofParams):
        secondTerm = input('Enter the 2nd Term or Terms: ')
        if secondTerm not in ['Alarm', 'Burglary', 'Earthquake']:
            print('Invalid 2nd Term')
            exit(-1)
        queries["given"][secondTerm] = "True"


    network_obj = BayesianNetwork(structure, values, queries)
    network_obj.makeGraph()
    
    network_obj.inference()
