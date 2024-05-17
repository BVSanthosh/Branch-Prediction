import math

'''
Implements two-bit predictor
'''

class TwoBit:
    def __init__(self, trace_file):
        self.trace_file = trace_file   #trace file to read
        self.correct_pred = 0   #total number of correct predictions
        self.incorrect_pred = 0   #total number of incorrect predictions
        self.bpb_size = 512   #size of the prediction buffer (CAN CHANGE)
        self.bpb = [0 for _ in range(self.bpb_size)]   #the prediction buffer as an array
        self.num_of_instructions = 5000000   #number of lines to read from the trace file (CAN CHANGE)
        
    #makes the prediction for each branch instruction in the trace file
    def predict(self):
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
                    
                self.update_bpb(index, taken)   #call to update the buffer using the prediction outcome
                
                instruction_count += 1
                if instruction_count >= self.num_of_instructions:   #checks if line limit is reached to stop the prediction algorithm
                    break
            
        return (self.correct_pred, self.incorrect_pred, self.num_of_instructions)
    
    #gets the index from the branch address
    def get_index(self, branch_addr):
        branch_addr_int = int(branch_addr, 16)
        index = branch_addr_int & (self.bpb_size - 1)
        
        return index 
    
    #gets the prediction from the buffer
    def get_prediction(self, index):
        if self.bpb[index] <= 1:
            return 0
        else:
            return 1
    
    #updates the prediction state in the buffer
    def update_bpb(self, index, taken):
        if taken == 0:
            if self.bpb[index]  <= 2:
                self.bpb[index] = 0
            else:
                self.bpb[index] = 2
        else:
            if self.bpb[index] >= 1:
                self.bpb[index] = 3
            else:
                self.bpb[index] = 1