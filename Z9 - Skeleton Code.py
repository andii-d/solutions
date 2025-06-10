#Skeleton Program code for the AQA A Level Paper 1 Summer 2025 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

import re
import random
import math

def Main():
    NumbersAllowed = []
    Targets = []
    MaxNumberOfTargets = 20
    MaxTarget = 0
    MaxNumber = 0
    TrainingGame = False
    Choice = input("Enter y to play the training game, anything else to play a random game: ").lower()
    print()
    if Choice == "y":
        MaxNumber = 1000
        MaxTarget = 1000
        TrainingGame = True
        Targets = [-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 119]
    else:
        MaxNumber = 10
        MaxTarget = 50
        Targets = CreateTargets(MaxNumberOfTargets, MaxTarget)        
    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
    PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber)
    input()
    
def PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber):
    FreezePosition = -1 # Init the position of the frozen number
    Score = 0
    GameOver = False
    while not GameOver:
        DisplayState(Targets, NumbersAllowed, Score, FreezePosition)
        if FreezePosition == -1: # Always ask the player the at first if they want to freeze a number
            FreezeAsk = input('Would you like to freeze a number?').lower()
            if FreezeAsk == 'y':
                FreezePosition = int(input(f'Enter the position from 1-20 of the target to freeze: ')) - 1 # Take away one because of 0 based indexing
                DisplayState(Targets, NumbersAllowed, Score, FreezePosition) # Display what freezing the selected target will look like
        else:
            FreezeInput = input(f'Would you like to unfreeze target position {FreezePosition + 1}? Enter y/n: ').lower() # Ask the user if they would like to unfreeze the target
            # This resets FreezePos. to -1 
            if FreezeInput == 'y':
                FreezePosition = -1
                DisplayState(Targets, NumbersAllowed, Score, FreezePosition) # Redisplay the targets with no frozen number 
        UserInput = input("Enter an expression: ")
        print()
        if CheckIfUserInputValid(UserInput):
            UserInputInRPN = ConvertToRPN(UserInput)
            if CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
                IsTarget, Score = CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score)
                if IsTarget:
                    NumbersAllowed = RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed)
                    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
        Score -= 1
        if Targets[0] != -1:
            GameOver = True
        else:
            Targets = UpdateTargets(Targets, TrainingGame, MaxTarget, FreezePosition) # Update the targets     
    print("Game over!")
    DisplayScore(Score)
    
def CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score):
    UserInputEvaluation = EvaluateRPN(UserInputInRPN)
    UserInputEvaluationIsATarget = False
    if UserInputEvaluation != -1:
        for Count in range(0, len(Targets)):
            if Targets[Count] == UserInputEvaluation:
                Score += 2
                Targets[Count] = -1
                UserInputEvaluationIsATarget = True        
    return UserInputEvaluationIsATarget, Score
    
def RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed):
    UserInputInRPN = ConvertToRPN(UserInput)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in NumbersAllowed:
                NumbersAllowed.remove(int(Item))
    return NumbersAllowed

def UpdateTargets(Targets, TrainingGame, MaxTarget, FreezePosition):
    for Count in range (0, len(Targets) - 1):
        if Count == FreezePosition:
            Targets[Count - 1] = Targets[Count + 1]
        else:
            Targets[Count] = Targets[Count + 1]
    Targets.pop()
    if TrainingGame:
        Targets.append(Targets[-1])
    else:
        Targets.append(GetTarget(MaxTarget))
    return Targets

def CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
    Temp = []
    for Item in NumbersAllowed:
        Temp.append(Item)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in Temp:
                Temp.remove(int(Item))
            else:
                return False            
    return True

def CheckValidNumber(Item, MaxNumber):
    if re.search("^[0-9]+$", Item) is not None:
        ItemAsInteger = int(Item)
        if ItemAsInteger > 0 and ItemAsInteger <= MaxNumber:
            return True            
    return False
    
def DisplayState(Targets, NumbersAllowed, Score, FreezePosition):
    DisplayTargets(Targets, FreezePosition)
    DisplayNumbersAllowed(NumbersAllowed)
    DisplayScore(Score)    

def DisplayScore(Score):
    print("Current score: " + str(Score))
    print()
    print()
    
def DisplayNumbersAllowed(NumbersAllowed):
    print("Numbers available: ", end = '')
    for N in NumbersAllowed:
        print(str(N) + "  ", end = '')
    print()
    print()
    
def DisplayTargets(Targets, FreezePosition):
    print("|", end = '')
    for T in Targets:
        if T == -1:
            print(" ", end = '')
        else:
            if T == Targets[FreezePosition] and FreezePosition != -1: # Only set the frozen targets to those that are required
                print(f'<{T}>', end = '') 
            else:
                print(T, end = '')           
        print("|", end = '')
    print()
    print()

def ConvertToRPN(UserInput):
    Position = 0
    Precedence = {"+": 2, "-": 2, "*": 4, "/": 4}
    Operators = []
    Operand, Position = GetNumberFromUserInput(UserInput, Position)
    UserInputInRPN = []
    UserInputInRPN.append(str(Operand))
    Operators.append(UserInput[Position - 1])
    while Position < len(UserInput):
        Operand, Position = GetNumberFromUserInput(UserInput, Position)
        UserInputInRPN.append(str(Operand))
        if Position < len(UserInput):
            CurrentOperator = UserInput[Position - 1]
            while len(Operators) > 0 and Precedence[Operators[-1]] > Precedence[CurrentOperator]:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()                
            if len(Operators) > 0 and Precedence[Operators[-1]] == Precedence[CurrentOperator]:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()    
            Operators.append(CurrentOperator)
        else:
            while len(Operators) > 0:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()
    return UserInputInRPN

def EvaluateRPN(UserInputInRPN):
    S = []
    while len(UserInputInRPN) > 0:
        while UserInputInRPN[0] not in ["+", "-", "*", "/"]:
            S.append(UserInputInRPN[0])
            UserInputInRPN.pop(0)        
        Num2 = float(S[-1])
        S.pop()
        Num1 = float(S[-1])
        S.pop()
        Result = 0.0
        if UserInputInRPN[0] == "+":
            Result = Num1 + Num2
        elif UserInputInRPN[0] == "-":
            Result = Num1 - Num2
        elif UserInputInRPN[0] == "*":
            Result = Num1 * Num2
        elif UserInputInRPN[0] == "/":
            Result = Num1 / Num2
        UserInputInRPN.pop(0)
        S.append(str(Result))       
    if float(S[0]) - math.floor(float(S[0])) == 0.0:
        return math.floor(float(S[0]))
    else:
        return -1

def GetNumberFromUserInput(UserInput, Position):
    Number = ""
    MoreDigits = True
    while MoreDigits:
        if not(re.search("[0-9]", str(UserInput[Position])) is None):
            Number += UserInput[Position]
        else:
            MoreDigits = False            
        Position += 1
        if Position == len(UserInput):
            MoreDigits = False
    if Number == "":
        return -1, Position
    else:
        return int(Number), Position    

def CheckIfUserInputValid(UserInput):
    if re.search("^([0-9]+[\\+\\-\\*\\/])+[0-9]+$", UserInput) is not None:
        return True
    else:
        return False

def GetTarget(MaxTarget):
    return random.randint(1, MaxTarget)
    
def GetNumber(MaxNumber):
    return random.randint(1, MaxNumber)   

def CreateTargets(SizeOfTargets, MaxTarget):
    Targets = []
    for Count in range(1, 6):
        Targets.append(-1)
    for Count in range(1, SizeOfTargets - 4):
        Targets.append(GetTarget(MaxTarget))
    return Targets
    
def FillNumbers(NumbersAllowed, TrainingGame, MaxNumber):
    if TrainingGame:
        return [2, 3, 2, 8, 512]
    else:
        while len(NumbersAllowed) < 5:
            NumbersAllowed.append(GetNumber(MaxNumber))      
        return NumbersAllowed

if __name__ == "__main__":
    Main()