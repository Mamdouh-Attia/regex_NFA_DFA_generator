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
    def __init__(self):
        self.start_super_state: SuperState = None          
        self.super_states: set[SuperState] = set() 
        self.accept_super_states: set[SuperState] = set()

    
                      

    '''Just makes a new empty DFA, and a legit SuperState then insert this initial SuperState into the Empty DFA then return the DFA'''
    def __init__(self, nfa: NFA):
      self.start_super_state = SuperState()
      self.start_super_state.is_start = True
      self.start_super_state.label = "S0"
      
      self.start_super_state.sub_states = nfa.start.get_epsilon_closure()
      self.start_super_state.out_edges = []
      
      self.super_states = set()
      self.super_states.add(self.start_super_state)

      self.accept_super_states = set()

      
    '''takes a list of states, returns the matching SuperState if the list already'''
    def get_super_state(self, super_state: SuperState):
      for ss in self.super_states:
        if ss == super_state:
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
        for SSTT in self.super_states:
            if(SSTT.is_start):
                gra.node("", _attributes={'shape' : 'none'})
                gra.edge("", repr(SSTT))
            if(SSTT.is_end):
                gra.node(repr(SSTT), _attributes={'peripheries' : '2'})
            else:
                gra.node(repr(SSTT))
                id = id + 1
                

        for SSTT in self.super_states:
            labelsOfSource = ""
            for stt in SSTT.sub_states:
                labelsOfSource = labelsOfSource + stt.label + " , "

            
            for edg in SSTT.out_edges:
                gra.edge(repr(SSTT) , repr(edg.destination), label=edg.label)

        gra.format = 'png'
        gra.render('DFA', view=True)
        return gra.source

    def visualize_cleaned(self):
      gra = Digraph(graph_attr={'rankdir':'LR', "label":"DFA"})
      id = 0
      for SSTT in self.super_states:
        if(SSTT.is_start):
          gra.node("", _attributes={'shape' : 'none'})
          gra.edge("", SSTT.label)
        if(SSTT.is_end):
          gra.node(SSTT.label, _attributes={'peripheries' : '2'})
        else:
          gra.node(SSTT.label)
        id = id + 1
        
      for SSTT in self.super_states:
        for edg in SSTT.out_edges:
          gra.edge(SSTT.label , edg.destination.label, label=edg.label)

      gra.format = 'png'
      gra.render('DFA', view= True)
      return gra.source
    



