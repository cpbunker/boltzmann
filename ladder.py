"""
Created Sept 8, 2020
@author: Christian Bunker

Boltzmann ladder project:
In this project, I create a simple agent based model of particles moving up and
down a ladder. My aim is to connect this model to statistical mechanics by drawing
parallels between particle speed and temperature, and between rungs and energy
levels. Successful recreation of the Boltzmann distribution in this model could
offer insights into the interpretation of the distribution.

ladder.py:
This module creates the ladder object which is physical system that the agents see.
The ladder tracks the particles as they move between its rungs.
"""

import agent

import numpy as np

################################################################################
# base class of ladder is doubly linked list
################################################################################

class Item(object):
    '''
    Defines an item in the doubly linked list. The attributes of this object are actual data content and references
    to the previous and next items (the double links).
    '''
    
    #### #### overloaded methods
    
    def __init__(self, content):
        '''
        Create the item object in the double linked list.
        
        Args:
        :param content: can be any type, the content of the item
        '''
        
        self.content = content;
        
        # init links
        self.next = None;
        self.prev = None;
        
        return; #### end init
    
    
    def __str__(self):
        '''
        string representation of item
        '''
        
        return str(self.content);
    
    
    def __repr__(self):
        return str(self);
    
    #### end Item
    
    
    
class DoubleLinkedList(object):
    
    #### #### overloaded methods
    
    def __init__(self):
        '''
        Create the empty DLL. The starting node, set to None, is the only definitive atrribute.
        Start node and all other items are Item objects (see above).
        '''
        
        self.start = None;
        
        return; #### end init
    
    
    def __str__(self):
        '''
        String representation of the DLL is just list of its items
        '''
        
        return str(self.In())
    
    
    def __len__(self):
        '''
        Length of DLL
        '''
        
        # simply use length of simple list version of DLL
        return len(self.In() );
    
    
    def __getitem__(self, i):
        '''
        overload list indexing ([]) for the DLL
        
        Args:
        :param i: int, the index of the item we want to get
        
        Returns:
        item object that is the ith in the DLL
        '''
        
        # make sure index arg is an integer
        if( type(i) != type(1) ):
            raise TypeError("Double Linked List slicing must take integer arguments.")
        
        # make sure index is in range
        if( i >= len(self) ):
            raise IndexError;
        
        # step thru the list using links i times
        n = self.start; # start with starting item
        for j in range(i): # each time update to next item
            n = n.next; # gets next item
            
        # n is now the ith item
        return n; #### end getitem
            
            
        
    
    
    #### #### adding items to list
    
    def insertEmpty(self, it):
        '''
        Insert an item into an empty DLL.
        
        Args:
        :param it: object of any type to be added to this list as an item
        '''
        
        # make sure list is empty
        if( self.start == None):
            
            # add as starting Item object
            self.start = Item(it);
            
        else: # list is not empty
            raise Exception("Called insertEmpty() but "+str(self)+" is not empty.");
        
        return; #### end insertEmpty
    
    
    def insertStart(self, it):
        '''
        Insert an item into the beginning of any DLL.
        
        Args:
        :param it: object of any type to be added to this list as item content
        '''
        
        # if empty just insert it at start
        if( self.start == None):
            self.start = Item(it);
            return;
        
        # otherwise have to push back the start node and link it
        # create new item and link it to old start
        new = Item(it);
        new.next = self.start;
        
        # link old start to new
        self.start.prev = new;
        
        # add new item as start of DLL
        self.start = new;
        
        return; #### end insertStart
    
    
    def append(self, it):
        '''
        Inserts an item at the end of the DLL.
        
        Args:
        :param it: object of any type to be added to the end of this list as item content
        '''
        
        # if list is empty we just put it in at start
        if( self.start == None):
            self.start = Item(it);
            return;
        
        # otherwise have to stick on at end
        # get last item
        last = self[len(self)-1 ];
        
        # create new item
        new = Item(it);
        
        # link both ways
        last.next = new;
        new.prev = last;
        
        return; #### end append
    
    
    def pop(self):
        '''
        Removes and returns the content of the first item of the list.
        '''
        
        # check that the list is not empty
        if(self.start == None):
            raise Exception("Cannot pop() empty list.")
        
        # get the starting item
        start_item = self.start;
        
        # set the start to the second item
        self.start = self.start.next;
        
        # remove the previous link of the old second (new start) item
        # this only needs to be done if the new start is an Item and not none
        # ie we have not emptied the list
        if( self.start != None):
            self.start.prev = None;
        
        # return the content of the now unlinked start node
        return start_item.content; #### end pop
    
    
    def insert(self, it, i):
        '''
        Inserts an item to the DLL as the ith item.
        
        Args:
        :param it: object of any type to be added to list as item content
        :param i: int, index to put the item at
        '''
        
        # check that i is not out of range
        if( i > len(self) ):
            raise IndexError("Index out of range")
        
        # if i = 0, we put it at start
        if( i == 0):
            
            # replace start reference
            old_start = self.start; # grabs old start Item
            self.start = Item(it);
            
            # link old and new starts
            self.start.next = old_start;
            old_start.prev = self.start;
            
            return;
        
        # if i is length of DLL, we put it at end
        elif( i == len(self) ):
            
            # get the old last item
            last = self[len(self) - 1];
            
            # link to new last item
            new = Item(it);
            last.next = new;
            new.prev = last;
            
            return;
        
        # otherwise, iter thru the first i - 1 elements
        n = self.start;
        for j in range(i - 1):
            n = n.next; # update n
            
        # now n refers to the i-1th Item
        # we add the new item right after this
        old_next = n.next; # grabs old next link
        n.next = Item(it); # inserts new item in its place
        n.next.prev = n; # link new item back to i-1th item, its predecessor
        
        # link to i + 1th item, its successor
        n.next.next = old_next;
        old_next.prev = n.next;
        
        return;
        
        
        
    #### #### traversing, accessing list items
    
    def In(self):
        '''
        Returns list of items in the DLL so that it can be traversed by in operator.
        
        Returns:
        Python list object, whose elements are Item objects
        '''
        
        # define return object
        inlist = [];
        
        # if DLL is empty, preserve empty list
        if( self.start == None):
            return inlist;
        
        # traverse items, beginning at start
        # stop when we encounter a link to None
        n = self.start; # start with starting node of DLL
        while (n != None):
            
            # add item to the list
            inlist.append(n);
            
            # update n using link to next item
            n = n.next;
            
        return inlist; #### end In
    
#### end DLL

    
################################################################################
# ladder inherits from DLL
# rungs of ladder are simple objects with def'd energy, occupants list
################################################################################

class rung(object):
    """
    Each rung is def'd by its energy w/r/t the bottom rung (always zero energy)
    The rung also keeps track of particles on it with a np array
    """
    
    #### overloaded methods

    def __init__(self, E, occupants):
        """
        Args:
        E, double, the energy level of the rung
        occupants, 1d np array, holds agent objects that are on this rung
        """
        
        # check attribute types
        if( type(E) != type(1.0) and type(E) != type(1) ):
            raise TypeError("Energy level must be a number.");
            
        elif( type(occupants) != type([]) ):
            raise TypeError("Occupants list must be a list");
        
        # set attributes
        self.E = E; # energy of the rung
        self.occupants = occupants; # particles on the rung
        
        return; #### end init
        
    def __repr__(self):
        """
        String rep of ladder rung, should be what comes out when we print ladder
        """
        
        # show occupancy of rung and if it has any verbose agents
        retstring = "[ "+str(len(self.occupants))+" ]";
        for a in self.occupants: # look for verbose agents
            if(a.name == "verbose"):
                retstring += " X";
                
        return retstring; #### end repr


#### end rung class


class ladder(DoubleLinkedList):

    #### overloaded methods

    def __init__(self):
        """
        begin the ladder DLL with only a starting rung. All higher rungs will be
        created when needed.
        """
        
        # place rung in DLL item, place item at start of ladder
        self.start = Item(rung(0, []) );
        
        # how rungs correspond to energy
        self.deltaE = 1; # each rung 1 energy unit higher
        
        return; #### end init
        
    def __str__(self):
        '''
        String representation of the DLL
        '''
        
        # print each item of the DLL In() list on separate line
        retlist = ""
        for i in range(len(self.In())):
            retlist += "E = "+str(i*self.deltaE);
            retlist += " "*(7-len("E = "+str(i*self.deltaE)) ) + str(self[i]) + "\n";
            
        return retlist; #### end str
        
    #### basic access methods
    
    def N(self):
        """
        Quickly get how many total particles are in the ladder
        """
        
        # return var
        counter = 0;
        
        # iter over rungs
        for r in self.In():
            counter += len(r.content.occupants);
            
        return counter;
        
    def maxE(self):
        """
        Return the energy of the max occupied rung ( ie Fermi energy)
        """
        
        # iter backwards over rungs
        r = self.In()[-1]; # start with topmost rung
        
        while True: # keep going till we find EF and return
            if(len(r.content.occupants) != 0): # this rung is occupied so is fermi E
                return r.content.E;
            
            else: # try the one lower
                r = r.prev;
        
    #### placement of particles on rung
    
    def Start(self, parts):
        """
        start the particle on the lowest rung
        
        Args:
        parts: single agent or any iterable of agents (can be higher dimension also)
        """
        
        # try treating parts as an iterable
        try:
            # if parts is an iterable run over each part
            for p in parts:
                self.Start(p); # call recursively to allow nested inputs
            
        except: # should have reached input which is just an agent
        
            if(type(parts) == type (agent.TestAgent() ) ): # single agent
                self.start.content.occupants.append(parts);
                
            else: #problem
                raise ValueError("Start must take single agent or list of agent objects");
                
        #### end start
    
    def Place(self, part, r, delta):
        """
        Place the given particle, formerly on the given rung, onto new rung as
        spec'd by delta (-1, 0, 1)
        """

        # place based on value of delta
        if(delta == -1): # lower rung
            
            # check that lower rung exists
            if(r.prev != None): # it is there
                r.prev.content.occupants.append(part);
            else: # particle has to stay on this (lowest) rung
                r.content.occupants.append(part);
                
        elif(delta == 0): # stay on this rung
            r.content.occupants.append(part);
            
        elif(delta == 1): # upper rung
        
            # check that upper rung exists
            if(r.next != None): # it exists
                r.next.content.occupants.append(part);
                
            else: # we have to make it
            
                # determine its properties
                energy = r.content.E + self.deltaE; # energy goes up unit
                occ = [];
                
                # add it to ladder
                self.append(rung(energy, occ)); # DLL append takes content, places it in item
                
                # place the particle
                r.next.content.occupants.append(part);
                
        else: # wrong delta value given
            raise ValueError("Place() can only place particles for delta = -1, 0, 1.\n");
            
        #### end place
        
    #### time evolution of the system
    
    def TimeStep(self):
        """
        This method enacts the change in the state of the system with one time step.
        This amounts to letting each particle experience one time step by having it
        go up, down, or stay put (using its Act method).
        """
        
        # iter over all rungs
        for r in self.In(): # remember each r actually an item, w/ r.content a rung
        
            # pull out old occupants of rung
            occs = r.content.occupants
            
            # overwrite occupants list as empty
            r.content.occupants = [];
        
            # iter over old occupants
            for a in occs:
                    
            
                # let this particle decide on action, if it hasn't yet
                if(not a.flag):
                
                    # Act returns 1 for go up, 0 for stay, -1 for go down
                    delta = a.Act();
                    
                    if( a.name == "verbose"): # we want debug print statements for this a
                        print("verbose acted with result: "+str(delta));
                    
                    # move the agent to rung accordingly
                    self.Place(a, r, delta);
                        
                    # flag that this particle already acted this time step
                    a.flag = True;
                    
                    if( a.name == "verbose"): #debug
                        print("verbose placed and flagged");
                        
                # else if particle already acted, just put it back in occupants
                else:
                    r.content.occupants.append(a);
                    
                    if(a.name == "verbose"):
                        print("verbose already acted, placed back on rung");
                    
        # after the entire step, reset all flags
        for r in self.In():
            for a in r.content.occupants:
                a.flag = False;
                
                if( a.name == "verbose"): # debug
                    print("end of time step, verbose flag reset");
                
                    
        #### end time step
        
    #### calculating properties of the system
    
    
                    
                    

################################################################################
# test code / wrapper functions
################################################################################

def TimeStepTestCode():

    # make a ladder
    lad = ladder();
    
    # place an interesting particle on the ladder
    a1 = agent.agent(0,0.5, name = "verbose");
    a2 = agent.TestAgents(3); # add some other uninteresting agents
    lad.Start((a1, a2));
    
    # go over some time steps
    for t in range(50):
    
        lad.TimeStep();
        print("t = "+str(t)+"\n"+str(lad));
        
    print(lad.N());
    print(lad.maxE() );

    return; ### end place test code
    
    
################################################################################
# execute code
################################################################################

if(__name__ == "__main__"):

    TimeStepTestCode();
