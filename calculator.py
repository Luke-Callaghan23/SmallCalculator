class Number():
    signs  = ['a', 's', 'm', 'd', 'p']
    levels = {'a':1, 's':1, 'm':2, 'd':2, 'p':3}   #The PEMDAS significancy of each operation
    def __init__(self, equation, prevLevel):
        self.equation = equation
        self.sign  = 'e'             #The default self.sign is 'e', so when the sign becomes not 'e', that means we know we've come across a sign operation
        self.left  = None              #The number to the left of this one
        self.right = None             #The number to the right of this one
        self.num   = 0                  #The number that this evaluates to
        self.prevLevel = prevLevel     #The PEMDAS significancy of this number's 'parent'
        self.warning = self.solve()  #The only time Number.solve() does not retur None is when there is a level break (basically, when PEMDAS is out of place)
    def solve(self):
        length = len(self.equation)
        iterCount  = 0                 #iterCount is the loop variable
        parenCount = -1              #parenCount is incremented when a '(' is found and decremented when a ')' is found.  When parenCount == 0, then we know that we've reached a point in the equation where there are no hanging parenthesis 
        firstParen = -1                 #firstParen holds the index of the first opening parenthesis in the equation
        lastParen  = -1                 #lastParen holds the index of the closing parenthesis corresponding to firstParen
        for char in self.equation:
            if char == '(':
                if parenCount == -1:        #parenCount starts at -1 to keep a flag for having never found an opening parenthesis
                    parenCount = 0
                parenCount += 1             #parenCount is incremented when a '(' is found
                if firstParen == -1:        #if there were no parenthesis found before this, then obviously this is the first opening parenthesis,
                    firstParen = iterCount  #    and firstParen is reset
            elif char == ')':
                parenCount -= 1                #parenCount is decremented when a ')' is found
                lastParen = iterCount        #lastParen is reset to parenCount
                if parenCount == 0 and length - 1 == iterCount:        #This is used to deal with the case when the equation follows: '(equation)' [as in, an equation that is wholly inside of parentheses]
                    if self.sign != 'e':
                        self.equation = self.equation[firstParen+1:lastParen]
                        self.solve()
                    else:
                        self.num = float(self.equation[firstParen+1:lastParen])
            else:
                if iterCount == length - 1 and parenCount == -1 and self.sign == 'e':  #This is used to handle the case where the equation follows: 'number' [as in, the 'equation' is really just some number]
                    self.num = float(self.equation)
                    return
                if inList(Number.signs, char):
                    if parenCount == -1 or parenCount == 0:
                        self.right = Number(self.equation[iterCount+1:], Number.levels[char])
                        self.left  = Number(self.equation[:iterCount], Number.levels[char])
                        if Number.levels[char] < self.prevLevel: ##If the level of the 'parent' of this number is higher than this, then that operatio
                            self.num  = self.left.num   #self.num is set to the left child's number, so when we return to the parent, that number is used in the parent's operation
                            self.sign = char            #self.sign is reset so that the parent can later perform the right operation on self.right
                            return self.right            #This is the only case wherein Number.solve() will return a non-Nonetype
                        nums = (self.left.num, self.right.num)  #Creates the nums tuple used in the loop below
                        operation = char
                        while True: #A while True loop, but, at max, it only loops twice.  The only time that it loops twice is when the next operation is of a lower PEMDAS significancy than the current one
                            if operation == 'a':                #M
                                self.num = nums[0] + nums[1]
                            elif operation == 's':                #A
                                self.num = nums[0] - nums[1]
                            elif operation == 'm':                #T
                                self.num = nums[0] * nums[1]
                            elif operation == 'd':                #H
                                if self.right.num != 0:
                                    self.num = nums[0] / nums[1]
                                else:
                                    print('Error! Division by zero.')
                                    self.num = 'e'
                            elif operation == 'p':                #!
                                self.num = nums[0] ** nums[1]
                            if self.right.warning != None:                #If the right number has a warning, then that loop must continue
                                nums = (self.num, self.right.warning.num) #The current number and the right's warning number being the nums tuple
                                operation = self.right.sign               #The sign being the right's sign
                                self.right.warning = None 
                            else:
                                break
                        return
                    else:
                        self.sign = char
            iterCount += 1
def inList(array, target):
    for item in array:
        if item == target:
            return True
    return False
if __name__ == '__main__':
    answering = True
    answer = 'e'
    print("a = addition       ('2a2' = 2+2)")
    print("s = subtraction    ('2s2' = 2-2)")
    print("m = multiplication ('2m2' = 2*2)")
    print("d = division       ('2d2' = 2/2)")
    print("p = power          ('2p2' = 2^2)")
    while answering:
        if answer != 'e':
            print("Use 'A' to represent your previous answer")
        print("Enter 'e' to quit")
        equation = input('Please enter your equation: ')
        if equation == 'e':
            answering = False
        else:
            if answer != 'e' and ('A' in equation):
                equation = equation.replace('A', str(answer.num))
            answer = Number(equation, -1)
            if answer != 'e':
                print(f'The Answer is: {answer.num}\n\n')