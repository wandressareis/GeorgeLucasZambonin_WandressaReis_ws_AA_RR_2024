import math

import matplotlib.pyplot as plt

def f(n:int):
    count = 0
    #for l in range(10000):
    for i in range(n - 5):
        for j in range(i + 2, int(n / 2), 1):
            for k in range(n):
                count += 10_000
    return count

def t(n:int):
    k = math.floor(n/2)
    return 10000*n*(min(n-5,k-1))*(min(n-5,k-2))/2

def plot_values(save_image_path:str, n_values:list=list(range(1, 30)), projection:float=1):
    n_values 
    theoretical_n_values = list(range(min(n_values), int(max(n_values)*projection)))
    operations = []

    for n in n_values:
        operations.append(f(n))

    theoretical_operations = []
    for n in theoretical_n_values:
        theoretical_operations.append(t(n))

    plt.plot(n_values, operations, label="Actual Operations", color='orange')
    plt.plot(theoretical_n_values, theoretical_operations, label="Theoretical T(n)", linestyle='-.', color='blue')

    plt.xlabel("n")
    plt.ylabel("Operations")
    plt.legend()
    plt.savefig(save_image_path)
    
if __name__ == "__main__":
    plot_values("assets/graphs/theorical_t_projection.png", projection=1, n_values=list(range(1,100)))