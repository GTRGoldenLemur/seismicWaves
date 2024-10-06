#py -3 -m pip install pandas
#C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe -m pip install --upgrade pip

#scikit-learning: try to machine learning to analyse clusters, and distinguish

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_moon_catalog():
    link = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/training/catalogs/"+"apollo12_catalog_GradeA_final"+".csv"
    f = pd.read_csv(link)

    return [np.array(f['filename'].tolist()), np.array(f['time_rel(sec)'].tolist()),  np.array(f['mq_type'].tolist())]

def get_moon_mq(cat, fn):
    res = []
    n = 0
    for file_n in cat[0]:
        if file_n == fn:
            res.append( [cat[0][n], cat[1][n], cat[2][n] ] )
        n+=1
    return res
#cat_file = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/"+"xa.s12.00.mhz.1970-01-19HR00_evid00002.csv"

#file_name = "xa.s12.00.mhz.1970-01-09HR00_evid00007" #"xa.s12.00.mhz.1969-12-16HR00_evid00006"
#cat_file = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/test/data/S12_GradeB/"+file_name+".csv"

def analyze_moon(file_name, cat_file):

    
    cat = pd.read_csv(cat_file)

    moon_cata = get_moon_catalog()
    moon_q = get_moon_mq(moon_cata, file_name)

    print(moon_q)



    csv_times = np.array(cat['time_rel(sec)'].tolist())
    csv_data = np.array(cat['velocity(m/s)'].tolist())

    def average(a=0, b=len(csv_data))->float:
        a = int(max(0, a))
        b = int(min(b, len(csv_data)))
        
        sum = 0
        for s in csv_data[a:b]:
            sum+=abs(s)
        return sum/(b-a)

    av = average()

    fig,ax = plt.subplots(1,1,figsize=(10,3))
    #hist = ax[1]
    #ax = ax[0]
    ax.plot(csv_times,csv_data)
    #ax.set_ylim(av)



    ax.hlines(y=av, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Average")
    ax.hlines(y=av*2, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Threshold", linestyles="dashed")
    ax.hlines(y=0, xmin=min(csv_times), xmax=max(csv_times),colors="blue", label="Zero")


    averages = []
    seismic_act = [[0, 0, ""]] # [..., [start, end, type], ... ]

    interval = 4*60*4
    for n in range(0, len(csv_data), interval):

        local_av = average(n-interval/2, n+interval/2)

        ax.hlines(y=local_av, xmin=csv_times[int(max(n-interval/2, 0))], xmax=csv_times[int(min(n+interval/2, len(csv_times)-1))], colors="green", label="Local Average")

        if (local_av > av * 2):
            if (seismic_act[-1][1] != "") and (local_av > 1.5*averages[-1]):
                seismic_act.append([csv_times[n - interval*5//2], "", ""])

                # print("Seism start: ", seismic_act[-1])

        else:
            if seismic_act[-1][1] == "":
                if csv_times[n]-seismic_act[-1][0] > interval:
                    seismic_act[-1][1] = csv_times[n + interval*5//2]

                    print("Seism at: ", seismic_act[-1])

                    ax.axvline(x=seismic_act[-1][0], c="red")
                    ax.axvline(x=csv_times[n + interval*5//2], c="red", linestyle=":")
                else:
                    seismic_act.pop(-1)


        averages.append(local_av)

    #print(np.array(np.repeat(0, len(csv_data)), dtype="float64"), csv_data)

    #hist = plt.scatter(csv_data, np.array(np.repeat(0, len(csv_data)), dtype="float64"))

    #hist = plt.hist(np.multiply(abs(csv_data), 100))

    for t in moon_q:
        ax.axvline(x=t[1], c="orange", linestyle=":")

    plt.show()

    return [csv_times, csv_data], seismic_act, averages

fn = "xa.s12.00.mhz.1970-01-09HR00_evid00007"
cf = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/test/data/S12_GradeB/"+fn+".csv"

analyze_moon(fn, cf)


def get_mars_catalog():
    link = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/mars/training/catalogs/"+"Mars_InSight_training_catalog_final"+".csv"
    f = pd.read_csv(link)

    return [np.array(f['filename'].tolist()), np.array(f['time_rel(sec)'].tolist())]

def get_mars_q(cat, fn):
    res = []
    n = 0
    for file_n in cat[0]:
        if file_n == fn+".csv":
            res.append( [cat[0][n], cat[1][n] ] )
        n+=1
    return res


def analyze_mars(file_name, cat_file):
    
    cat = pd.read_csv(cat_file)

    mars_cata = get_mars_catalog()
    mars_q = get_mars_q(mars_cata, file_name)

    print("MarsQuakes", mars_q)



    csv_times = np.array(cat['rel_time(sec)'].tolist())
    csv_data = np.array(cat['velocity(c/s)'].tolist())

    def average(a=0, b=len(csv_data))->float:
        a = int(max(0, a))
        b = int(min(b, len(csv_data)))
        
        sum = 0
        for s in csv_data[a:b]:
            sum+=abs(s)
        return sum/(b-a)

    av = average()

    fig,ax = plt.subplots(1,1,figsize=(10,3))
    #hist = ax[1]
    #ax = ax[0]
    ax.plot(csv_times,csv_data)
    #ax.set_ylim(av)



    ax.hlines(y=av, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Average")
    ax.hlines(y=av*1.5, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Threshold", linestyles="dashed")
    ax.hlines(y=0, xmin=min(csv_times), xmax=max(csv_times),colors="blue", label="Zero")


    averages = []
    seismic_act = [[0, 0, ""]] # [..., [start, end, type], ... ]

    interval = 20*12
    for n in range(0, len(csv_data), interval):

        local_av = average(n-interval/2, n+interval/2)

        ax.hlines(y=local_av, xmin=csv_times[int(max(n-interval/2, 0))], xmax=csv_times[int(min(n+interval/2, len(csv_times)-1))], colors="green", label="Local Average")

        if (local_av > av * 1.5):
            if (seismic_act[-1][1] != ""):
                seismic_act.append([csv_times[n - interval*5//2], "", ""])

                print("Seism start: ", seismic_act[-1])

        else:
            if seismic_act[-1][1] == "":
                if csv_times[n]-seismic_act[-1][0] > interval//2-1:
                    seismic_act[-1][1] = csv_times[n + interval*5//2]

                    print("Seism at: ", seismic_act[-1])

                    ax.axvline(x=seismic_act[-1][0], c="red")
                    ax.axvline(x=csv_times[n + interval*5//2], c="red", linestyle=":")
                else:
                    seismic_act.pop(-1)


        averages.append(local_av)

    #print(np.array(np.repeat(0, len(csv_data)), dtype="float64"), csv_data)

    #hist = plt.scatter(csv_data, np.array(np.repeat(0, len(csv_data)), dtype="float64"))

    #hist = plt.hist(np.multiply(abs(csv_data), 100))

    for t in mars_q:
        ax.axvline(x=t[1], c="orange", linestyle=":")
    
    plt.show()

    #Start:           End:
    seismic_act[0][0], seismic_act[-1][1]

    return [csv_times, csv_data], seismic_act, averages


#Training Data
fn = ["XB.ELYSE.02.BHV.2022-01-02HR04_evid0006", "XB.ELYSE.02.BHV.2022-02-03HR08_evid0005"][0]
fc = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/mars/training/data/"+fn+".csv"

#Test Data
fn = ["XB.ELYSE.02.BHV.2019-05-23HR02_evid0041", "XB.ELYSE.02.BHV.2019-07-26HR12_evid0033", "XB.ELYSE.02.BHV.2019-07-26HR12_evid0034", "XB.ELYSE.02.BHV.2019-09-21HR03_evid0032", "XB.ELYSE.02.BHV.2021-05-02HR01_evid0017"][4]
fc = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/mars/test/data/"+fn+".csv"


#analyze_mars(fn, fc)
