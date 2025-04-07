from dotenv import load_dotenv

import time
import os

from tools.hevy import HevyTool

if(__name__ == "__main__") :
    
    load_dotenv()

    user_name = os.getenv("HEAVY_USER_NAME")
    user_password = os.getenv("HEAVY_PASSWORD")

    start_time = time.time()

    tool = HevyTool(user_name, user_password)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Initialisation : {duration:.2f} seconds")
    
    start_time = time.time()

    end_time = time.time()
    duration = end_time - start_time
    print(f"Request time : {duration:.2f} seconds")
    
