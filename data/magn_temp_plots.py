import numpy as np
import matplotlib.pyplot as plt
import csv
import os

folder = "C:\\Users\\savva\\Documents\\GitHub\\ising_model_2.0\\data\\magn_data"
folder2 = "C:\\Users\\savva\\Documents\\GitHub\\ising_model_2.0\\pngs\\"
texfolder = "C:\\Users\\savva\\OneDrive - University of Cambridge\\Part2\\Computational Projects\\ising_model\\Report\\texfigures\\"

def plot_1():
    """
    magnetisation vs temperature with different lattice sizes
    """
    p_files = []
    dim = 2
    # please change file path when running on different devices
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt") and not file.endswith(").txt"):
            p_files.append(os.path.join(folder,file))

    L_list = []
    fig, ax = plt.subplots()
    ax.axvline(2.2692, label="$T_c$", linestyle="--",color="k")
    for p_file in p_files:
        D = int(((os.path.splitext(os.path.basename(p_file))[0]).split('_',3)[2])[0])
        if (D != dim):
            continue
        L = (os.path.splitext(os.path.basename(p_file))[0]).split('_',3)[3]
        avgM = []
        errM = []
        T = []
        if (L not in L_list):
            L_list.append(L)
            with open(p_file) as csvfile:
                lines = csv.reader(csvfile, delimiter=' ')
                for row in lines:
                    T.append(float(row[0]))
                    avgM.append(float(row[1]))
                    errM.append(float(row[2]))
            ax.errorbar(T, avgM, errM, ls='',marker='+', label="L = "+str(L))

    ax.set_title("<|Magnetisation|> vs Temperature")
    ax.set_ylabel("m")
    ax.set_xlabel(r"T / $J/k_B$")
    ax.legend()
    fig.savefig(folder2+"magn_vs_temp.png")
    fig.savefig(texfolder+"magn_vs_temp.pdf")


def plot_2():
    """
    magnetisation vs temperature with different lattice sizes
    """
    p_files = []
    dim = 3
    # please change file path when running on different devices
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt") and not file.endswith(").txt"):
            p_files.append(os.path.join(folder,file))

    L_list = []
    fig, ax = plt.subplots(figsize=(12,8))
    ax.axvline(2.2692, label="$T_c$", linestyle="--",color="k")
    for p_file in p_files:
        D = int(((os.path.splitext(os.path.basename(p_file))[0]).split('_',3)[2])[0])
        if (D != dim):
            continue
        L = (os.path.splitext(os.path.basename(p_file))[0]).split('_',3)[3]
        avgM = []
        errM = []
        T = []
        if (L not in L_list):
            L_list.append(L)
            with open(p_file) as csvfile:
                lines = csv.reader(csvfile, delimiter=' ')
                for row in lines:
                    T.append(float(row[0]))
                    avgM.append(float(row[1]))
                    errM.append(float(row[2]))
            ax.errorbar(T, avgM, errM, ls='',marker='+', label="L = "+str(L))

    ax.set_title("<|Magnetisation|> vs Temperature")
    ax.set_ylabel("m")
    ax.set_xlabel(r"T / $J/k_B$")
    ax.legend()
    fig.savefig(folder2+"magn_vs_temp_3D.png")
    fig.savefig(texfolder+"magn_vs_temp_3D.pdf")


def main():
    #plot_1()
    plot_2()
    plt.show()

if (__name__ == '__main__'):
    main()
