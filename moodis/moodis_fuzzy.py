import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Set up fuzzy logic
def getFuzzyServerControlSimulation():

    #range input
    input_range_low = np.array([ 0,	1.067,	1.867])
    input_range_medium = np.array([1.215,	2.067,	2.800])
    input_range_high = np.array([2.933,	3.867,	4.1])

    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    G01 = ctrl.Antecedent(np.arange(0, 5, 1), 'G01')
    G03 = ctrl.Antecedent(np.arange(0, 5, 1), 'G03')
    G05 = ctrl.Antecedent(np.arange(0, 5, 1), 'G05')
    G07 = ctrl.Antecedent(np.arange(0, 5, 1), 'G07')
    G08 = ctrl.Antecedent(np.arange(0, 5, 1), 'G08')
    G09 = ctrl.Antecedent(np.arange(0, 5, 1), 'G09')
    G11 = ctrl.Antecedent(np.arange(0, 5, 1), 'G11')
    G12 = ctrl.Antecedent(np.arange(0, 5, 1), 'G12')
    G17 = ctrl.Antecedent(np.arange(0, 5, 1), 'G17')
    G18 = ctrl.Antecedent(np.arange(0, 5, 1), 'G18')

    G01['low'] = fuzz.trimf(G01.universe, input_range_low)
    G01['medium'] = fuzz.trimf(G01.universe, input_range_medium)
    G01['high'] = fuzz.trimf(G01.universe, input_range_high)

    G03['low'] = fuzz.trimf(G03.universe, input_range_low)
    G03['medium'] = fuzz.trimf(G03.universe, input_range_medium)
    G03['high'] = fuzz.trimf(G03.universe, input_range_high)
    
    G05['low'] = fuzz.trimf(G05.universe, input_range_low)
    G05['medium'] = fuzz.trimf(G05.universe, input_range_medium)
    G05['high'] = fuzz.trimf(G05.universe, input_range_high)

    G07['low'] = fuzz.trimf(G07.universe, input_range_low)
    G07['medium'] = fuzz.trimf(G07.universe, input_range_medium)
    G07['high'] = fuzz.trimf(G07.universe, input_range_high)

    G08['low'] = fuzz.trimf(G08.universe, input_range_low)
    G08['medium'] = fuzz.trimf(G08.universe, input_range_medium)
    G08['high'] = fuzz.trimf(G08.universe, input_range_high)

    G09['low'] = fuzz.trimf(G09.universe, input_range_low)
    G09['medium'] = fuzz.trimf(G09.universe, input_range_medium)
    G09['high'] = fuzz.trimf(G09.universe, input_range_high)

    G11['low'] = fuzz.trimf(G11.universe, input_range_low)
    G11['medium'] = fuzz.trimf(G11.universe, input_range_medium)
    G11['high'] = fuzz.trimf(G11.universe, input_range_high)

    G12['low'] = fuzz.trimf(G12.universe, input_range_low)
    G12['medium'] = fuzz.trimf(G12.universe, input_range_medium)
    G12['high'] = fuzz.trimf(G12.universe, input_range_high)

    G17['low'] = fuzz.trimf(G17.universe, input_range_low)
    G17['medium'] = fuzz.trimf(G17.universe, input_range_medium)
    G17['high'] = fuzz.trimf(G17.universe, input_range_high)

    G18['low'] = fuzz.trimf(G18.universe, input_range_low)
    G18['medium'] = fuzz.trimf(G18.universe, input_range_medium)
    G18['high'] = fuzz.trimf(G18.universe, input_range_high)

    episode = ctrl.Consequent(np.arange(-1, 2, 1), 'episode')

    #range output
    output_range_hipomania = np.array([-1, -1, 0])
    output_range_eutemik = np.array([-1, 0, 1])
    output_range_mania = np.array([0, 1, 1])

    episode['hipomania'] = fuzz.trimf(episode.universe, output_range_hipomania)
    episode['eutemik'] = fuzz.trimf(episode.universe, output_range_eutemik)
    episode['mania'] = fuzz.trimf(episode.universe, output_range_mania)
    
    rules = []

    rules.append(ctrl.Rule(G01['high'] & G03['high'] & G05['high'] & G07['high'] & G08['high'] & G09['high'] & G11['high'] & G12['high'] & G17['high'] & G18['high'], episode['mania']))
    rules.append(ctrl.Rule(G01['high'] & G03['high'] & G05['high'] & G07['high'] & G08['high'] & G09['high'] & G11['high'] & G12['high'] & G17['high'] & G18['medium'], episode['mania']))
    rules.append(ctrl.Rule(G01['high'] & G03['high'] & G05['high'] & G07['medium'] & G08['high'] & G09['high'] & G11['high'] & G12['high'] & G17['high'] & G18['medium'], episode['mania']))
    #rules.append(ctrl.Rule(G01['high'] & G03['high'] & G05['high'] & G07['medium'] & G08['high'] & G09['high'] & G11['high'] & G12['high'] & G17['high'] & G18['high'], episode['']))
    rules.append(ctrl.Rule(G01['medium'] & G03['high'] & G05['high'] & G07['medium'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['high'] & G08['medium'] & G09['low'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['high'] & G08['low'] & G09['low'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['high'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['high'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['medium'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['low'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['hipomania']))
    rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['medium'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['medium'], episode['hipomania']))
    #rules.append(ctrl.Rule(G01['medium'] & G03['medium'] & G05['medium'] & G07['high'] & G08['medium'] & G09['low'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['']))
    #rules.append(ctrl.Rule(G01['medium'] & G03['high'] & G05['high'] & G07['medium'] & G08['medium'] & G09['medium'] & G11['medium'] & G12['medium'] & G17['low'] & G18['low'], episode['']))
    
    server_ctrl = ctrl.ControlSystem(rules)
    server_ctrl_simulation = ctrl.ControlSystemSimulation(server_ctrl)
    
    return server_ctrl_simulation

#Calculate fuzzy logic
def calculateFuzzy(G01, G03, G05, G07, G08, G09, G11, G12, G17, G18):
    server = getFuzzyServerControlSimulation()
    server.input['G01'] = G01
    server.input['G03'] = G03
    server.input['G05'] = G05
    server.input['G07'] = G07
    server.input['G08'] = G08
    server.input['G09'] = G09
    server.input['G11'] = G11
    server.input['G12'] = G12
    server.input['G17'] = G17
    server.input['G18'] = G18

    server.compute()
    output=server.output['episode']
    
    return output


#TODO create get mood by answered question using fuzzy logic
def getMoodEpisode(patient_mood_responses):
    #set initial parameter
    G01=0
    G03=0
    G05=0
    G07=0
    G08=0
    G09=0
    G11=0 
    G12=0
    G17=0 
    G18=0
    episode_score=0
    episode_category=''
    for patient_mood_response in patient_mood_responses:
        if (patient_mood_response.question.question_code=="G01"):
            G01 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G03"):
            G03 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G05"):
            G05 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G07"):
            G07 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G08"):
            G08 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G09"):
            G09 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G11"):
            G11 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G12"):
            G12 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G17"):
            G17 = patient_mood_response.answer_score
        if (patient_mood_response.question.question_code=="G18"):
            G18 = patient_mood_response.answer_score
    
    try:
        episode_score = calculateFuzzy(G01, G03, G05, G07, G08, G09, G11, G12, G17, G18)
        
    except Exception as e:
        print("Something Error: "+ str(e))
        pass

    print("Episode Score: "+str(episode_score))
    if (episode_score<-0.5):
        episode_category='HIPOMANIA'
    elif(episode_score<0.5):
        episode_category='EUTEMIK'
    elif(episode_score<1):
        episode_category='MANIA'

    
    return episode_score, episode_category

