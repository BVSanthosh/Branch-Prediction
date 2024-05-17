import sys
import time

from always_taken import AlwaysTaken
from two_bit import TwoBit
from gshare import GShare
from profiled import Profiled

'''
Starting point of the branch prediction algorithms
'''

def main():
    correct_pred = 0   #total number of correct predictions
    incorrect_pred = 0   #total number of incorrect predictions
    total_instructions = 0   #total number of instructions read from trace file
    mispred_penalty = 7   #number of cycles wasted when a misprediction occurs
    correct_pred_cost = 1   #number of cycles for when a prediction is correct
    
    if len(sys.argv) < 2:
        print("python branch_predictor.py <prediction_strat> <trace_file>")
        return

    pred_strat = sys.argv[1]   #the prediction strategy to use
    trace_file = sys.argv[2]   #the trace file to read
    
    start_time = time.time()
    
    if pred_strat == "always_taken":   #uses always taken 
        always_taken = AlwaysTaken(trace_file)
        correct_pred, incorrect_pred, total_instructions = always_taken.predict()
    elif pred_strat == "two_bit":   #uses two-bit predictor 
        two_bit = TwoBit(trace_file)
        correct_pred, incorrect_pred, total_instructions = two_bit.predict()
    elif pred_strat == "gshare":   #uses gshare
        gshare = GShare(trace_file)  
        correct_pred, incorrect_pred, total_instructions = gshare.predict()
    elif pred_strat == "profiled":   #uses profiled
        profiled = Profiled(trace_file)
        correct_pred, incorrect_pred, total_instructions = profiled.predict()
        
    end_time = time.time()
    duration = round(end_time - start_time, 2)   #execution time with the branch prediciton algorithm
    accuracy = round(correct_pred / (correct_pred + incorrect_pred) * 100, 2)   #accuracy as a percentage
    total_cycles = (correct_pred * correct_pred_cost) + (incorrect_pred * mispred_penalty)   #Total number of cycles to execute all the branch instructions (hypothetical)
    cpi = round(total_cycles / total_instructions, 2)   #total number of cycles per branch instruction (hypothetical)
    
    print(f"Execution time: {duration} sec")
    print(f"Accuracy: {accuracy}%")
    print("Total Cycles with Prediction: ", total_cycles)
    print("CPI: ", cpi)
            
if __name__ == "__main__":
    main()