import random

'''
Implements profiled
'''

class Profiled:
    def __init__(self, trace_file):
        self.trace_file = trace_file   #trace file to read
        self.correct_pred = 0   #total number of correct predictions
        self.incorrect_pred = 0   #total number of incorrect predictions
        self.pt_size = 512   #size of the prediction buffer (CAN CHANGE)
        self.pt = [[0, 0] for _ in range(self.pt_size)]    #the prediction buffer as an array
        self.num_of_instructions = 5000000   #number of lines to read from the trace file (CAN CHANGE)
    
    #makes the prediction for each branch instruction in the trace file
    def predict(self):
        self.profile_run()   #first does th profile run to gather information 
        
        instruction_count = 0
        with open(self.trace_file, 'r') as file:
            for line in file:
                fields = line.strip().split()
                branch_addr = fields[0]   #extracts the branch address
                taken = int(fields[-1])   #extracts the taken field
                index = self.get_index(branch_addr)   #gets the index of the branch address
                
                if self.get_prediction(index) == taken:
                    self.correct_pred += 1   #increments if the prediciton was correct
                else:
                    self.incorrect_pred += 1   #increments if the prediciton was incorrect
                    
                instruction_count += 1
                if instruction_count >= self.num_of_instructions:    #checks if line limit is reached to stop the prediction algorithm
                    break
                    
        return (self.correct_pred, self.incorrect_pred, self.num_of_instructions)

    #does the profile run 
    def profile_run(self):
        with open(self.trace_file, 'r') as file:
            for line in file:
                fields = line.strip().split()
                branch_addr = fields[0]
                taken = int(fields[-1])
                index = self.get_index(branch_addr)

                self.update_pt(index, taken)
    
    #gets the index from the branch address
    def get_index(self, branch_addr):
        branch_addr_int = int(branch_addr, 16)
        index = branch_addr_int & (self.pt_size - 1)
        
        return index 
    
    #updates the prediction state in the buffer
    def update_pt(self, index, taken):
        if taken == 1:
            self.pt[index][0] += 1
        else:
            self.pt[index][1] += 1
            
    #gets the prediction from the buffer
    def get_prediction(self, index):
        taken_prob = self.pt[index][0] / (self.pt[index][0] + self.pt[index][1])
        
        if taken_prob > 0.5:
            return 1
        elif taken_prob < 0.5:
            return 0
        else:
            return random.randint(0, 1)