'''
Implements always taken
'''

class AlwaysTaken:
    def __init__(self, trace_file):
        self.trace_file = trace_file   #trace file to read
        self.correct_pred = 0   #total number of correct predictions
        self.incorrect_pred = 0   #total number of incorrect predictions
        self.num_of_instructions = 5000000   #number of lines to read from the trace file
        
    #makes the prediction for each branch instruction in the trace file
    def predict(self):
        instruction_count = 0
        
        with open(self.trace_file, 'r') as file:
            for line in file:
                fields = line.strip().split()
                taken = int(fields[-1])   #extracts the taken field
                
                if taken == 1:
                    self.correct_pred += 1   #increments if the prediciton was correct
                else:
                    self.incorrect_pred += 1   #increments if the prediciton was incorrect
                    
                instruction_count += 1
                if instruction_count >= self.num_of_instructions:   #checks if line limit is reached to stop the prediction algorithm
                    break
            
        return (self.correct_pred, self.incorrect_pred, self.num_of_instructions)