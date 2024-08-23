# %%
from os import walk
import os, re
import os.path
import shlex
import subprocess
import logging
import json
import pandas as pd
import matplotlib.pyplot as plt
import platform

ASSETS_PATH = "assets/"
GRAPHS_PATH = os.path.join(ASSETS_PATH, "graphs/")

logging.basicConfig(level=logging.DEBUG, filename='run_exp_data.log', filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

"""
Usage mode:
1) all inputs should be inside of inputs directory
2) all inputs are executed 13 times
3) all outputs are save in the file called execution_log.txt
"""

BINARY_PROGRAM_LIST = ["verifica_algo"]
# INPUTS_FILE = "inputs"
TIMES_RUN = 13
INPUT_LIST = [str(i) for i in range(100)]

# def list_files_input():    
#     for (dirpath, dirnames, filenames) in walk(INPUTS_FILE):
#         for file in filenames:
#             full_path = os.path.abspath(dirpath) + "/" + file
#             INPUT_LIST.append(full_path)   

# %%
def run_code() -> dict:

    dict_executions = {
        "n": [],
        "total_comparisons": [],
        "execution_time(ns)": [],
    }
    logging.debug(f'Running the program with each input {TIMES_RUN} times')
    for BINARY_PROGRAM in BINARY_PROGRAM_LIST:
        for input in INPUT_LIST:
            print("./src/" + BINARY_PROGRAM + " " + input)
            cmd = shlex.split("./src/" + BINARY_PROGRAM + " " + input)
            for count_time in range(TIMES_RUN):
                logging.debug(f"Running input: {input} - Time {count_time}")
                process = subprocess.Popen(cmd,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
                stdout, stderr = process.communicate()            
                if not stderr:
                    logging.debug(f"Program output: - Time {count_time}")
                    logging.debug(f"---------------------------")
                    logging.debug(stdout)
                    logging.debug(f"---------------------------")
                    output = json.loads(stdout)
                    dict_executions["n"].append(output["n"])
                    dict_executions["total_comparisons"].append(output["total_comparisons"])
                    dict_executions["execution_time(ns)"].append(output["execution_time(ns)"])
    return dict_executions
    
def plot_graph(df: pd.DataFrame) -> None:

    if not os.path.isdir(ASSETS_PATH):
        os.mkdir(ASSETS_PATH)
    
    if not os.path.isdir(GRAPHS_PATH):
        os.mkdir(GRAPHS_PATH)

    df.groupby("n").mean().reset_index().plot(x="n", y="time_execution(seconds)")
    plt.title = "Time execution mean by n"
    plt.ylabel = "seconds"
    plt.savefig(os.path.join(GRAPHS_PATH, "time_execution_mean.png"))

    
    df.groupby("n").mean().reset_index().plot(x="n", y="total_comparisons")
    plt.savefig(os.path.join(GRAPHS_PATH, "total_comparisons.png"))

def log_specs():
    command = "cat /proc/cpuinfo"
    all_info = subprocess.check_output(command, shell=True).decode().strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            logging.debug(re.sub( ".*model name.*:", "", line,1))
            break

def main():

    # %%
    logging.debug(f'Experiment script executed on a {platform.processor()}')
    log_specs()
    dict_executions = run_code()

    # %%
    df_executions = pd.DataFrame.from_dict(dict_executions)
    df_executions['time_execution(seconds)'] = df_executions['execution_time(ns)'] * 1e-9
    df_executions.to_csv('executions.csv', index=False)

    # %%
    plot_graph(df_executions)
    
if __name__ == "__main__":
    main()
