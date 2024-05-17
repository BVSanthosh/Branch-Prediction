# Branch Prediction

### How to run:
python branch_predictor.py <prediction strategy> <trace file>
  - prediction strategy can be: "always_taken" (for always taken), "two_bit" (for two-bit predictor), "gshare" (for gshare) or "profiled" (for profiled)
  - trace file needs to be a valid filename 

Note: the buffer size and the number of lines in the trace file to read can be changed in the constructor for each of the prediction strategies
