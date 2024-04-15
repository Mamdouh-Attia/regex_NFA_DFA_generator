from graphviz import Digraph

############################################################################################
class edge:

      def __init__(self, label=None, destination=None):
        self.label = label
        self.destination = destination

      def __str__(self):
        return f"edge {self.label} going to {self.destination}"
      
############################################################################################
class NFA_state:
  
  def __init__(self):
    self.label: str = None
    self.out_edges: list[edge] = []

  '''
    gets the direct neighbours from taking the Character input edge, just the direct neighbours.
  '''
#   def get_char_closure(self, char) -> set:  # set[SuperState]
#     closure = set()
#     for edge in self.out_edges:
#       if edge.label == char:
#         closure.add(edge.destination)
#     return closure
  
  '''
    Returns a set of States reachable from taking Char edges recursively
  '''
  def get_char_closure(self, char) -> set:  # set[SuperState]
    reachable_states = set()
    for edge in self.out_edges:
      if edge.label == char:
        reachable_states.add(edge.destination)
        reachable_states = reachable_states.union(edge.destination.get_char_closure(char))
    return reachable_states
  
  '''
    Returns a set of States reachable from taking Epsilon edges recursively
  '''
  def get_epsilon_closure(self) -> set:  # set[SuperState]
    epsilon_closure = set()
    epsilon_closure.add(self)
    for edge in self.out_edges:
      if edge.label == "ε":
        epsilon_closure.add(edge.destination)
        epsilon_closure = epsilon_closure.union(edge.destination.get_epsilon_closure())
    return epsilon_closure

  def __str__(self) -> str:
    return self.label
  
  def __repr__(self) -> str:
     return self.label
  
  def __eq__(self, other) -> bool:
    return other.label == self.label
  
  def __ne__(self, other) -> bool:
    return other.label != self.label
  
  def __hash__(self) -> int:
     return hash(self.label)
  
############################################################################################
class NFA:

    def __init__(self, initial, acc, inner):
        self.start: NFA_state = initial
        self.accept: NFA_state = acc
        self.inner_states: list[NFA_state] = inner

    
    def print_graph(self):
        '''
        print the graph in a visual way
        '''
        print("NFA graph:")
        for state in self.inner_states:
            print(f"State {state.label} :")
            for edge in state.out_edges:
                print(f"  {edge}")
        print(f"Start state : {self.start.label}")
        print(f"Accept state : {self.accept.label}")

    def visualize(self):
        '''
        Visualize the graph
        '''
        dot = Digraph()
        #distinguish accept states
        for state in self.inner_states:
            if state == self.accept:
                dot.node(state.label, shape="doublecircle")
            else:
                dot.node(state.label)

        #add edges
        for state in self.inner_states:
            for edge in state.out_edges:
                dot.edge(state.label, edge.destination.label, label=edge.label)
        #Top to bottom
        dot.graph_attr["rankdir"] = "BT"
        dot.graph_attr["rankdir"] = "TB"
        #Left to right
        dot.graph_attr["rankdir"] = "LR"
        #format
        dot.format = "png"
        #show
        dot.view()
        #save
        dot.save("NFA.png")
        return dot

    def __str__(self) -> str:
      return self.start.label

    def __repr__(self) ->str:
      return self.start.label
    
############################################################################################

class SuperState:
  '''A superState is defined by a bunch of SubStates, a bunch of outgoing edges, and its label/ID,
    and 2 flags indicating whether or not this SuperState is starting or accepting
  '''
  def __init__(self):
      self.is_start: bool = False          
      self.is_end: bool = False            
      self.out_edges: list[edge] = []        
      self.sub_states: set[NFA_state] = set()        
      self.label: str = None

  def get_labels(self) -> list[str]:
    labels = []
    for s in self.sub_states:
      labels.append(s.label)
    return labels
  
  def get_destination(self, char):
     for edge in self.out_edges:
        if edge.label == char:
           return edge.destination
     return None
    

  def generate_new_superstate(self, char):
      reachable_states = set()
      for state in self.sub_states:
          reachable_states = reachable_states.union(state.get_char_closure(char))

      new_superstate = set()
      for state in reachable_states:
          new_superstate = new_superstate.union(state.get_epsilon_closure())


      # create a new superstate with the new states
      new_super = SuperState()
      new_super.sub_states = new_superstate
      return new_super

  def __eq__(self, other):
    set_of_src_labels = set()
    set_of_dst_labels = set()
    for s in self.sub_states:
      set_of_src_labels.add(s.label)
    for s in other.sub_states:
      set_of_dst_labels.add(s.label)
    return set_of_src_labels == set_of_dst_labels
  
  def __ne__(self, other):
    set_of_src_labels = set()
    set_of_dst_labels = set()
    for s in self.sub_states:
      set_of_src_labels.add(s.label)
    for s in other.sub_states:
      set_of_dst_labels.add(s.label)
    return set_of_src_labels != set_of_dst_labels

  def __str__(self):
    if(self.sub_states):
      stringy = ""
      for sub in self.sub_states:
        stringy = stringy + str(sub) + ","
      return "SuperState " +stringy
    else:
      return "Empty SuperState"

  def __repr__(self):
    if(self.sub_states):
      stringy = ""
      for sub in self.sub_states:
        stringy = stringy + str(sub) + ","
      return stringy
    else:
      return "Empty SuperState"

  def __hash__(self):
    if(self.sub_states):
      stringy = " "
      for sub in self.sub_states:
        stringy = stringy + str(sub) + ","
      return hash("SuperState" +stringy)
    else:
      return hash(None)
    
############################################################################################

class DFA:
    
    ''' A DFA object contains a set of SuperStates, also a pointer to the starting SuperState and a set of the accept SuperState'''
    def __init__(self, nfa: NFA = None):
        if nfa is None:
            self.start_super_state: SuperState = SuperState()          
            self.super_states: set[SuperState] = set() 
            self.accept_super_states: set[SuperState] = set()
        else:
            self.start_super_state = SuperState()
            self.start_super_state.is_start = True
            self.start_super_state.label = "S0"
            self.start_super_state.sub_states = nfa.start.get_epsilon_closure()
            self.start_super_state.out_edges = []
            self.super_states = {self.start_super_state}
            self.accept_super_states = set()

      
    '''takes a list of states, returns the matching SuperState if the list already'''
    def get_super_state(self, super_state: SuperState):
      for ss in self.super_states:
        if ss == super_state:
          return ss
      return None
    
    def get_accept_states(self):
       return self.accept_super_states
    
    def get_non_accept_states(self):
       return self.super_states.difference(self.accept_super_states)
    
    def get_super_state_from_label(self, label):
      for ss in self.super_states:
          if ss.label == label:
             return ss
          
      return None

    def __eq__(self, other):
      return self.start_super_state == other.start_super_state and self.super_states == self.super_states
    
    def __ne__(self, other):
      return self.start_super_state != other.start_super_state or self.super_states != self.super_states

    
    def empt(self):
      self.start_super_state = SuperState()          
      self.end_super_state = set()             
      self.super_states = set()

    def visualize_normal(self):
        gra = Digraph(graph_attr={'rankdir':'LR'})
        id = 0
        for ss in self.super_states:
            if(ss.is_start):
                gra.node("", _attributes={'shape' : 'none'})
                gra.edge("", repr(ss))
            if(ss.is_end):
                gra.node(repr(ss), _attributes={'peripheries' : '2'})
            else:
                gra.node(repr(ss))
                id = id + 1
                

        for ss in self.super_states:
            labelsOfSource = ""
            for stt in ss.sub_states:
                labelsOfSource = labelsOfSource + stt.label + " , "

            
            for edg in ss.out_edges:
                gra.edge(repr(ss) , repr(edg.destination), label=edg.label)

        gra.format = 'png'
        gra.render('DFA', view=True)
        return gra.source

    def visualize(self, graph_label):
      gra = Digraph(graph_attr={'rankdir':'LR', "label":f"{graph_label}"})
      for ss in self.super_states:
        if(ss.is_start):
          gra.node("", _attributes={'shape' : 'none'})
          gra.edge("", ss.label)
        if(ss.is_end):
          gra.node(ss.label, _attributes={'peripheries' : '2'})
        else:
          gra.node(ss.label)
        
      for ss in self.super_states:
        for edg in ss.out_edges:
          gra.edge(ss.label , edg.destination.label, label=edg.label)

      gra.format = 'png'
      gra.render(f"{graph_label}", view= True)
      return gra.source
    

    def visualize_min_DFA (self):
      gra = Digraph(graph_attr={'rankdir':'LR', "label":"minimized DFA"})
      
      for ss in self.super_states:
        if(ss.is_start):
          gra.node("", _attributes={'shape' : 'none'})
          gra.edge("", ss.label)
        if(ss.is_end):
          gra.node(ss.label, _attributes={'peripheries' : '2'})
        else:
          gra.node(ss.label)
        
      for ss in self.super_states:
        for edg in ss.out_edges:
          gra.edge(ss.label , edg.destination, label=edg.label)
      gra.format = 'png'
      gra.render('minDFA', view=True)
      return gra.source
    



############################################################################################

class LowerTriangularMatrix:
   
  def __init__(self, size):
      self.size = size
      self.pairs = dict()
      for i in range(1, size):
         for j in range(i):
            new_pair = ("S"+str(i), "S"+str(j))
            self.pairs[tuple(sorted(new_pair))] = "∅"

  def fill_with_dfa(self, dfa: DFA):
    accept_states = dfa.get_accept_states()
    non_accept_states = dfa.get_non_accept_states()

    for ac_ss in accept_states:
        for non_ac_ss in non_accept_states:
          self.set(ac_ss.label, non_ac_ss.label, 'F')


  def iterate_to_min_dfa(self, dfa: DFA, input_chars: str):
    continue_iterating = True
    while continue_iterating:
      continue_iterating = False
      for pair in self.pairs.keys():
        if self.get(pair[0], pair[1]) == "∅":
            for char in input_chars:

              # get the destination of the current pair
              new_ss1 = dfa.get_super_state_from_label(pair[0]).get_destination(char)
              new_ss2 = dfa.get_super_state_from_label(pair[1]).get_destination(char)
              
              # if the pair does not exist in the matrix
              # or the pair is marked as ∅
              # or the pair is the same, continue
              if (new_ss1 is None and new_ss2 is None) or (new_ss1.label == new_ss2.label) or (self.get(new_ss1.label, new_ss2.label) == "∅"):
                continue

              # if one of the pairs exists and the other does not, mark the current pair as F
              if (new_ss1 is None) != (new_ss2 is None):
                  self.set(pair[0], pair[1], 'F')
                  continue_iterating = True
                  break

              # if the pair is marked as F, mark the current pair as F
              if self.get(new_ss1.label, new_ss2.label) == "F":
                self.set(pair[0], pair[1], 'F')
                continue_iterating = True
                break
          



  def get(self, i, j):
      return self.pairs[tuple(sorted((i, j)))]
  
  def set(self, i, j, value):
      self.pairs[tuple(sorted((i, j)))] = value

  def __str__(self):
      stringy = ""
      for i in range(1, self.size):
        for j in range(i):
          stringy = stringy + self.get(i, j) + " "
        stringy = stringy + "\n"
      return stringy
