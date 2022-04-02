import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pickle
    
def step_f_plotting():
    infile=open("response_study_output/respone_analysis",'rb') 
    log =pickle.load(infile)   
    print(log[0])

    fig , ax =plt.subplots()
    ax.plot(log[:,1],log[:,0])
    #ax.set(xlable='time ms',,title='step function response')
    ax.set_title('step function response')
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('RPS')
    ax.grid()
    fig.savefig("response_study_output/step_response_at_6v_input.png")
    plt.show()

def DC_RPS_plotting():
    infile=open("response_study_output/respone_analysis_DC_RPS",'rb') 
    log =pickle.load(infile)   
    print(log)

    fig , ax =plt.subplots()
    ax.plot(log[:,1],log[:,0])
    #ax.set(xlable='time ms',,title='step function response')
    ax.set_title('Duty Cycle - RPS relation Graph')
    ax.set_xlabel('Duty Cycle')
    ax.set_ylabel('RPS')
    ax.grid()
    fig.savefig("response_study_output/DC_RPS_relationat_6v_input.png")
    plt.show()
DC_RPS_plotting()