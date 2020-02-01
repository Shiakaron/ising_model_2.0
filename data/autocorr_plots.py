import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy.optimize import curve_fit

def gauss(x, mean, sigma, scale, offset):
    return (scale*np.exp(-((x-mean)/sigma)**2)+offset)

def power_fit(x,pow,scale,offset):
    return (scale*np.power(x,pow)+offset)

def plot_1():
    """
    Plot tau_e vs temperature
    """
    p_files = []
    folder = "C:\\Users\\savva\\Documents\\GitHub\\ising_model_2.0\\data\\autocorrelation_data\\initial_investigation"
    for file in sorted(os.listdir(folder)):
        if file.startswith("autocorr_times") and file.endswith("L.txt"):
            p_files.append(os.path.join(folder,file))

    fig, ax = plt.subplots()
    ax.axvline(2.2692, label="$T_c$", linestyle="--",color="k")
    for p_file in p_files:
        L = (os.path.splitext(os.path.basename(p_file))[0]).split('_',4)[2]
        T_list = []
        tau_list = []
        with open(p_file) as csvfile:
            lines = csv.reader(csvfile, delimiter=' ')
            for row in lines:
                T_list.append(float(row[0]))
                tau_list.append(float(row[1]))
        ax.plot(T_list,tau_list,marker='+',label="L = "+str(L))
    ax.set_title("Time lag vs Temperature")
    ax.set_ylabel(r"$\tau_e / sweeps$")
    ax.set_xlabel("T / K")
    ax.set_yscale("log")
    ax.legend()
    fig.savefig(folder+"\\tau_e_vs_temp.png")
    plt.show()

def plot_2():
    """
    1. fit gauss/lorentz on tau vs T for different L to get tau_peak
    2. plot of tau_peak vs L
    """
    L_list = []
    value_list = []
    error_list = []
    folder="C:\\Users\\savva\\Documents\\GitHub\\ising_model_2.0\\data\\autocorrelation_data\\peak_investigation"
    p_files = []
    for file in sorted(os.listdir(folder)):
        if file.startswith("autocorr_peak") and file.endswith("L.txt"):
            p_files.append(os.path.join(folder,file))

    fig, axs = plt.subplots(1,2,figsize=(16,6))
    fig.suptitle("Time lag vs Temperature")

    for p_file in p_files:
        L = (os.path.splitext(os.path.basename(p_file))[0]).split('_',4)[2]
        T = []
        tau = []
        tau_err = []
        with open(p_file) as csvfile:
            lines = csv.reader(csvfile, delimiter=' ')
            for row in lines:
                T.append(float(row[0]))
                tau.append(float(row[1]))
                tau_err.append(float(row[2]))

        if int(L) in [16,20,24,28,32,36,40]:
            axs[0].errorbar(T,tau,tau_err,marker='+',linestyle=" ",label=L)
            np.seterr(all="ignore")
            try:
                popt, pcov = curve_fit(gauss, T, tau, sigma=tau_err, absolute_sigma=True, maxfev=3000, p0=[2.3, 0.1, 100, 0], bounds=((2.28,-np.inf,-np.inf,-np.inf),(2.32,np.inf,np.inf,np.inf)))
                value_list.append(popt[2]+popt[3])
                error = abs(np.sqrt(abs((np.diag(pcov)))[2]) - np.sqrt(abs((np.diag(pcov))[3]))) + max(tau_err)
                if (np.isfinite(error)):
                    #print(error)
                    error_list.append(error)
                else:
                    max_tau = max(tau)
                    # value_list.append(max_tau)
                    error_list.append(tau_err[tau.index(max_tau)])
                x = np.linspace(T[0],T[-1],100)
                axs[0].plot(x,gauss(x, *popt), color="c",linewidth=1)
                # print("popt :",popt)
                # print("pcov^2 :",np.diag(pcov))
                # print(value_list[-1],error_list[-1])
            except:
                print("couldnt do gauss fit")
                # max_tau = max(tau)
                # value_list.append(max_tau)
                # error_list.append(tau_err[tau.index(max_tau)])
            L_list.append(int(L))
            print(L_list[-1],value_list[-1],error_list[-1])

    print(L_list)
    print(value_list)
    print(error_list)
    axs[1].errorbar(L_list,value_list,error_list,marker='+',linestyle=" ")
    popt2, pcov2 = curve_fit(power_fit, L_list, value_list, sigma=error_list, absolute_sigma=True, maxfev=2000, p0=[1,1,0])
    x2 = np.linspace(L_list[0],L_list[-1],100)
    axs[1].plot(x2,power_fit(x2,*popt2))
    axs[1].set_ylabel(r"$\tau_e$")
    axs[1].set_xlabel("L")


    #axs[1].legend()
    print(popt2[0],abs(np.sqrt(abs((np.diag(pcov)))[0])))
    axs[0].legend()
    axs[0].set_ylabel(r"$\tau_e$")
    axs[0].set_xlabel("T")



    fig.savefig(folder+"\\tau_e_peak_vs_temp.png")

    plt.show()

def main():
    # plot_1()
    plot_2()

if (__name__ == '__main__'):
    main()
