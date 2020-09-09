"""
Created Sept 8, 2020
@author: Christian Bunker

Boltzmann ladder project:
In this project, I create a simple agent based model of particles moving up and
down a ladder. My aim is to connect this model to statistical mechanics by drawing
parallels between particle speed and temperature, and between rungs and energy
levels. Successful recreation of the Boltzmann distribution in this model could
offer insights into the interpretation of the distribution.

agent.py:
This module codes the random-decision-making agents which traverse the ladder.
"""

import numpy as np
import time

################################################################################
# define the agent class
################################################################################

class agent(object):

    #### overloaded operators

    def __init__(self, prob_stay, prob_up, name="0"):
        """
        The agent is defined by its choices in two scenarios:
        - it is on a rung, and can stay on the rung with probability prob_stay or
            move with probability 1-prob_stay
        - it is on the ladder, and can move up with probability prob_up or down
            with probability 1-prob_up
        These define the prob attributes init'd here
        
        Args:
        prob_stay, prob_up, doubles, choice probs that define the agents action,
            each is 0<p<1
        name, optional, string, way to identify the agents, defaults to "0"
        """
        
        # check reasonability of probabilites
        if( prob_stay > 1 or prob_stay < 0 ):
            raise ValueError("Cannot init agent "+name+" : prob stay must be 0 < prob_up < 1");
            
        elif( prob_up > 1 or prob_up < 0 ):
            raise ValueError("Cannot init agent "+name+" : prob up must be 0 < prob_up < 1");
        
        # def probability attributes
        self.stay = prob_stay;
        self.up = prob_up;
        
        # other attributes
        self.name = name; # simple id for agent
        self.flag = False; # bool for keeping track of actions performed on agent
        
        #### end init
        
    def __str__(self):
        """
        String rep of the agent
        """
        pstring = "";
        
        # name of agent
        pstring += "Agent: "+self.name+"\n";
        
        # attributes
        pstring += "- stay probability = "+str(self.stay)+"\n";
        pstring += "- up probability = "+str(self.up)+"\n";
        
        return pstring;
        
    #### choice scenarios of the agent
    
    def OnRung(self):
        """
        1st choice scenario: agent reaches rung, it decides whether to stay, leave
        
        Returns bool, True if stay, False if leave
        """
        
        # generate random val
        alpha = np.random.uniform();
        
        # choose based on prob
        if(alpha < self.stay):
            return True; # agent will stay on rung
        else:
            return False; # will continue to move on ladder
            
        #### end OnRung
    
    def OnLadder(self):
        """
        2nd choice scenario: when the agent has left a rung, it will
        decide whether to go up or down the ladder.
        
        Returns bool, True if up, False if down
        """
        
        # generate random val
        alpha = np.random.uniform();
        
        # choose based on prob
        if(alpha < self.up):
            return True; # agent will move up ladder
        else:
            return False; # will move down
            
        #### end OnLadder
        
    #### overall action of the agent in one time step
    
    def Act(self):
        """
        In a single time step, the agent can either move one rung up, one down, or stay
        put. These options are expressed as return values 1, -1, 0. Each time step,
        the agent begins on a rung, so it must first choose to stay (return 0) or
        leave. If it leaves, it is on the ladder, and will choose to go up (return 1) or
        down (return -1).
        
        Returns: int 1, -1, 0 as explained above
        """
        
        # first choice
        if( self.OnRung() ): # true means it stays
            return 0;
            
        else: # false means it leaves
        
            # second choice
            if( self.OnLadder() ): # true means go up
                return 1;
                
            else: # false means go down
                return -1;
                
        #### end act
        
        
################################################################################
# test code / wrapper functions
################################################################################


def VisualizeAgent(N_ladder, ag):
    """
    Repeatedly print out simple ladder graphics as agent moves up and down
    """
    
    # create ladder as array of rung strings
    ladder=np.full(N_ladder,"|------|");
    
    # let agent act for a bit
    for i in range(N_ladder):
        time.sleep(1);
        print(str(ag.Act()) + "\n");
    
    
    
    

def AgentTestCode():

    # create agent
    a = agent(0.5,1);
    print(a);
    
    VisualizeAgent(10, a);

    return;
    
################################################################################
# execute code
################################################################################

if( __name__ == "__main__"):

    AgentTestCode();
        
