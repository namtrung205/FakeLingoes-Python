from multiprocessing import Pool, TimeoutError
from gtts import gTTS
import os


# def myTimer(func, myArgs , window ,myTimeout=10):
#     with Pool(processes=2) as pool:
#         res = pool.apply_async(func, (myArgs,)) 
#         try:
#             print(res.get(timeout=myTimeout))
#         except TimeoutError:
#             print("We lacked patience and got a multiprocessing.TimeoutError")

#         print("For the moment, the pool remains available for more work")
#     # exiting the 'with'-block has stopped the pool
#     print("Now the pool is closed and no longer available")
    

def myTimer(func, myArgs ,myTimeout=10):
    with Pool(processes=1) as pool:
        res = pool.apply_async(func, (myArgs,)) 
        try:
            a = str(res.get(timeout=myTimeout))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")
            return None
        print("For the moment, the pool remains available for more work")
        return res.get(timeout=myTimeout)
    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
    