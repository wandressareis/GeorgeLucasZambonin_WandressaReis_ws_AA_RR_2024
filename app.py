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
import numpy as np
import seaborn as sns
import math
from scipy.optimize import curve_fit

ASSETS_PATH = "assets/"
GRAPHS_PATH = os.path.join(ASSETS_PATH, "graphs/")

BINARY_PROGRAM_LIST = ["verifica_algo"]

TIMES_RUN = 13
INPUT_LIST = [str(i) for i in range(100)]

def linear(n, a, b):
    return a * n + b

def quadratic(n, a, b, c):
    return a * n**2 + b * n + c

def cubic(n, a, b, c, d):
    return a * n**3 + b * n**2 + c * n + d

def old_t(n):
    return 10_000*(n**2 - 5*n)

def actual_t(n):
    if n > 0:
        k = math.floor(n / 2)
        count = 10000 * n * (k - 2) * (k - 1) / 2
    else:
        count = 0
    return count

logging.basicConfig(level=logging.DEBUG, filename='run_exp_data.log', filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

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


def log_specs():
    command = "cat /proc/cpuinfo"
    all_info = subprocess.check_output(command, shell=True).decode().strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            logging.debug(re.sub( ".*model name.*:", "", line,1))
            break

def plot_t(df:pd.DataFrame):
    plt.clf()
    sns.lineplot(df, x='n', y='total_comparisons', label='Iterações reais', color='blue')
    sns.lineplot(df, x='n', y='old_t', label="T(n) slide", linestyle='--', color='red')
    sns.lineplot(df, x='n', y='actual_t', label='T(n) atual', linestyle='-.', color='orange')
    plt.title('Iterações x T(n)')
    plt.xlabel('n')
    plt.ylabel('iterações/t(n)')
    plt.legend()
    plt.savefig(os.path.join(GRAPHS_PATH, "func_custo_t.png"))

def plot_complexity(df):
    plt.clf()
    n = np.linspace(df['n'].min(), int(df['n'].max()*1.1), 50)

    # Ajustando as curvas
    popt_linear, _ = curve_fit(linear, df['n'], df['time_execution(seconds)'])
    popt_quadratic, _ = curve_fit(quadratic, df['n'], df['time_execution(seconds)'])
    popt_cubic, _ = curve_fit(cubic, df['n'], df['time_execution(seconds)'])


    # Verificando os parâmetros ajustados
    print(f'Parâmetros Linear: {popt_linear}')
    print(f'Parâmetros Quadrático: {popt_quadratic}')
    print(f'Parâmetros Cúbico: {popt_cubic}')

    # Plotando os dados e as curvas ajustadas
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='n', y='time_execution(seconds)', data=df, marker='o', label='Dados Originais')

    # Plot das curvas ajustadas
    # n = np.linspace(min(df['actual_t']), max(df['actual_t']), 100)
    sns.lineplot(x=n, y=linear(n, *popt_linear), label='Ajuste Linear', linestyle='--', color='r')
    sns.lineplot(x=n, y=quadratic(n, *popt_quadratic), label='Ajuste Quadrático', linestyle='--', color='g')
    sns.lineplot(x=n, y=cubic(n, *popt_cubic), label='Ajuste Cúbico', linestyle='-.', color='m')

    # Configurações do gráfico
    plt.ylim(bottom=-0.001)
    plt.title('Ajuste de Curvas - Tendência Assintótica')
    plt.xlabel('n')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.legend()

    plt.savefig(os.path.join(GRAPHS_PATH, "complexity_time.png"))

def plot_actual_t_projection(df:pd.DataFrame):
    plt.clf()
    popt_cubic, _ = curve_fit(cubic, df['n'], df['time_execution(seconds)'])
    n = np.linspace(df['n'].min(), int(df['n'].max()*5), 50)
    sns.lineplot(x=n, y=cubic(n, *popt_cubic), label='Ajuste Cúbico', linestyle='-.', color='m')
    sns.lineplot(x='n', y='time_execution(seconds)', data=df, linestyle='-', label='Dados Originais')
    plt.title('Projeção Tempo de Execução (segundos)')
    plt.xlabel('n')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.legend()
    plt.savefig(os.path.join(GRAPHS_PATH, "actual_t_projection.png"))

def main():

    logging.debug(f'Experiment script executed on a {platform.processor()}')
    log_specs()
    dict_executions = run_code()

    df_executions = pd.DataFrame.from_dict(dict_executions)
    df_executions['time_execution(seconds)'] = df_executions['execution_time(ns)'] * 1e-9
    df_executions.to_csv('executions.csv', index=False)

    
    df = df_executions.groupby("n").mean().reset_index()


    df['old_t'] = df['n'].apply(old_t)
    df['actual_t'] = df['n'].apply(actual_t)

    if not os.path.isdir(ASSETS_PATH):
        os.mkdir(ASSETS_PATH)
    
    if not os.path.isdir(GRAPHS_PATH):
        os.mkdir(GRAPHS_PATH)

    plot_t(df)
    plot_complexity(df)
    plot_actual_t_projection(df)
    #plot_graph(df)
    
if __name__ == "__main__":
    main()
