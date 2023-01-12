# Here we supose IA only plays with 'X'; lines and columns indexed from 0
# Example: choosing line = 0 and column = 2 produces:

#                      | |O 
#                     -----
#                      | | 
#                     -----
#                      | | 


class State:
    # Initial State
    def __init__(self):
        self.grid = [["" for column in range(3)] for line in range(3)]
        self.utility=None
    
    def copy(self):
        newState = State()
        newState.grid = [[self.grid[j][i] for i in range(3)]for j in range(3)]
        return newState
    
    def isFreeSpace(self,line,column) -> bool:
        return self.grid[line][column]==""
    
    def isEmpty(self):
        localSet = set()

        for line in self.grid:
            for element in line:
                localSet.add(element)

        if( len(localSet)==1 and "" in localSet):
            return True
        return False
                

    # States if there`s no possible movement
    def iPossibleMovement(self) -> bool:

        for line in self.grid:
            for element in line:
                 if element == "":
                    return True
                    
        return False

    # Marks a position at the grif
    def MarkPosition(self,line:int,column:int,player:chr):

        posElement = self.grid[line][column]

        if(posElement!=""):
            raise Exception(f"Position already taken by {posElement}")
        
        self.grid[line][column]=player

    # Return a list with possible sucessor states
    def getSucessors(self,player:chr) -> list:
        
        sucessors = []

        for line in range(3):
            for column in range(3):
                if self.isFreeSpace(line,column):
                    newState = self.copy()
                    newState.MarkPosition(line,column,player)
                    sucessors.append(newState)

        return sucessors

    
    # Provides visual representation of the board
    def __str__(self) -> str:
        ans = "Board: \n\n"

        for line in self.grid:
            for element in line:
                if element!="":
                    ans+=(element)
                else:
                    ans+=(" ")
                ans+=("|") 

            ans=ans[:-1]
            ans+=("\n"+5*'-'+'\n')

        ans=ans[:-6]
        ans+="\n\n"
        return ans
    
    # Checks if is a terminal state and stores utility value
    def TerminalTest(self) -> bool:

        # Checks if there`s only one character in a line
        for line in self.grid:
            localSet = set()
            for element in line:
                localSet.add(element)

            if(len(localSet)==1):
                if('X' in localSet):
                    self.utility = 1
                    return True
                elif('O' in localSet):
                    self.utility = -1
                    return True


        # Checks if there`s only one character in a column
        for column in range(3):
            localSet = set()
            for line in range(3):
                localSet.add(self.grid[line][column])

            if(len(localSet)==1):
                if('X' in localSet):
                    self.utility = 1
                    return True
                elif('O' in localSet):
                    self.utility = -1
                    return True

        # Checks if main diagonal was taken
        localSet = set()
        for pos in range(3):
            localSet.add(self.grid[pos][pos])
        if(len(localSet)==1):
            if('X' in localSet):
                self.utility = 1
                return True
            elif('O' in localSet):
                self.utility = -1
                return True

        # Checks if second diagonal was taken

        localSet = set()
        for pos in range(3):
            localSet.add(self.grid[2-pos][pos])
        if(len(localSet)==1):
            if('X' in localSet):
                self.utility = 1
                return True
            elif('O' in localSet):
                self.utility = -1
                return True
        
        # Checks if there`s a possible movement
        if self.iPossibleMovement():
            return False
        else:
            self.utility = 0
            return True

# returns the state taken from thepicked next action
def minMaxDecision(st:State)->State:
    v = maxValue(st)
    for sucessor in st.getSucessors('X'):
        if(minValue(sucessor)==v):
            return sucessor

# MaxValue funcion return an utility value
def maxValue(st:State) -> int:
    if st.TerminalTest():
        return st.utility

    v = -0x80000000

    for sucessor in st.getSucessors('X'):
        v = max(v,minValue(sucessor))
    return v


# MinValue funcion return an utility value
def minValue(st:State) -> int:
    # print("Doing minVal\n",st)
    if st.TerminalTest():
        return st.utility

    # Defeault = max int32_t value
    v = 0x7fffffff

    for sucessor in st.getSucessors('O'):
        v = min(v,maxValue(sucessor))
            
    return v

 
curState = State()

while not curState.TerminalTest():

    # AI turn
    print("Calculating machine choice...")
    curState = minMaxDecision(curState)

    # shows grid
    print(curState)

    # If AI won, the game is over
    if(curState.utility==1):
        print("AI won the game!")
        exit()

    if curState.TerminalTest():
        break

    # Player`s turn (intill he chooses a valid position)
    while(True):
        x,y = map(int,input("Insert your move`s row and column.\n").split())
        try:
            curState.MarkPosition(x,y,'O')
            break
        except:
            print("You can`t play at this position!!\n")

    print(curState)

    # If player won, the game is over
    if(curState.utility==-1):
        print("Congratulations! You won the game!")
        exit()

print("Oops, it`s a draw!")
