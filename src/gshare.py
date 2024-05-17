import math

'''
Implements gshare
'''

class GShare:
    def __init__(self, trace_file):
        self.trace_file = trace_file   #trace file to read
        self.correct_pred = 0   #total number of correct predictions
        self.incorrect_pred = 0   #total number of incorrect predictions
        self.pht_size = 512   #size of the prediction buffer (CAN CHANGE)
        self.pht = [0 for _ in range(self.pht_size)]   #the prediction buffer as an array
        self.ghr_size = int(math.log2(self.pht_size))   #size of the global predictor (number of previous taken values to save)
        self.ghr = 0   #the global predictior
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
                    self.correct_pred += 1  #increments if the prediciton was correct
                else:
                    self.incorrect_pred += 1  #increments if the prediciton was incorrect
                
                self.update_ghr(taken)   #call to update the global predictor 
                self.update_pht(index, taken)   #call to update the buffer using the prediction outcome
                
                instruction_count += 1
                if instruction_count >= self.num_of_instructions:   #checks if line limit is reached to stop the prediction algorithm
                    break
            
        return (self.correct_pred, self.incorrect_pred, self.num_of_instructions)
    
    #gets the index from the branch address
    def get_index(self, branch_addr):
        branch_addr_int = int(branch_addr, 16)
        index = (branch_addr_int ^ self.ghr) & (self.pht_size - 1)
        
        return index 
    
    #gets the prediction from the buffer
    def get_prediction(self, index):
        if self.pht[index] <= 1:
            return 0
        else:
            return 1
    
    #updates the prediction state in the buffer
    def update_pht(self, index, taken):
        if taken == 0:
            if self.pht[index]  <= 2:
                self.pht[index] = 0
            else:
                self.pht[index] = 2
        else:
            if self.pht[index] >= 1:
                self.pht[index] = 3
            else:
                self.pht[index] = 1
    
    #updates the global predictor
    def update_ghr(self, taken):
        self.ghr = ((self.ghr << 1) | taken) & ((1 << self.ghr_size) - 1)