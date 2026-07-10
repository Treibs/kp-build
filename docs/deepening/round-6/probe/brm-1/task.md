A rain-insurance policy: a buyer holds a `Policy` (premium paid at purchase, pooled). The
weather oracle (capability) marks each epoch rainy or dry. Settling a policy pays the holder
double the premium from the pool if the policy's epoch was rainy, and pays nothing (the
premium stays pooled) if it was dry — settlement consumes the policy either way and returns
the payout coin to the caller.
