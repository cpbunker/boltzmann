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
        
        return "Item: "+str(self.content);
    
    
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
        String representation of the DLL
        '''
        
        # simply use string of conversion of DLL to simple list using In()
        return str(self.In() );
    
    
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
        :param it: object of any type to be added to this list as an item
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
        :param it: object of any type to be added to the end of this list as an item
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
        Removes and returns the first item of the list.
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
        :param it: object of any type to be added to list as an item
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
            inlist.append(n.content);
            
            # update n using link to next item
            n = n.next;
            
        return inlist; #### end In
    
#### end DLL

    
################################################################################
# ladder inherits from DLL
# rungs of ladder are just Items with content = occupancy
################################################################################

class ladder(DoubleLinkedList):

    def __init__():
        return;
