#py -3 -m pip install pandas
#C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe -m pip install --upgrade pip

#scikit-learning: try to machine learning to analyse clusters, and distinguish

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def analyze_moon(file_name, cat_file):

    
    cat = pd.read_csv(cat_file)

    start_t = datetime.strptime(cat.iloc[1]["time_abs(%Y-%m-%dT%H:%M:%S.%f)"],'%Y-%m-%dT%H:%M:%S.%f')

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



    #ax.hlines(y=av, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Average")
    #ax.hlines(y=av*2, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Threshold", linestyles="dashed")
    ax.hlines(y=0, xmin=min(csv_times), xmax=max(csv_times),colors="blue", label="Zero")


    averages = []
    seismic_act = [[0, 0, ""]] # [..., [start, end, type], ... ]

    interval = 4*60*4
    for n in range(0, len(csv_data), interval):

        local_av = average(n-interval/2, n+interval/2)

        #ax.hlines(y=local_av, xmin=csv_times[int(max(n-interval/2, 0))], xmax=csv_times[int(min(n+interval/2, len(csv_times)-1))], colors="green", label="Local Average")

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

    #ax.set_facecolor("#000000")

    ax.set_title('Wave before being filtered', fontweight='bold')

    plt.show()

    seismic_act.pop(0)

    return [csv_times, csv_data], seismic_act, averages, start_t, "A"


def analyze_mars(file_name, cat_file):
    
    cat = pd.read_csv(cat_file)


    start_t = datetime.strptime(cat.iloc[1]["time(%Y-%m-%dT%H:%M:%S.%f)"],'%Y-%m-%dT%H:%M:%S.%f')

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



    #ax.hlines(y=av, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Average")
    #ax.hlines(y=av*1.5, xmin=min(csv_times), xmax=max(csv_times),colors="red", label="Threshold", linestyles="dashed")
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
                    #ax.axvline(x=seismic_act[-1][0], c="black")
                    #ax.axvline(x=csv_times[n + interval*5//2], c="black", linestyle=":")
                    print("Seism TOO short: ", csv_times[n]-seismic_act[-1][0])
                    seismic_act.pop(-1)


        averages.append(local_av)
    

    ax.set_title('Wave before being filtered', fontweight='bold')
    plt.show()

    seismic_act.pop(0)

    return [csv_times, csv_data], seismic_act, averages, start_t, "B"

def get_only_quake_data(r):
    data = {"Time (s)": [], "Speed (m/s)":[]}
    for q in r[1]:
        s_index, = np.where(np.isclose(r[0][0], q[0]))
        e_index, = np.where(np.isclose(r[0][0], q[1]))

        e_index = int(e_index[0])
        s_index = int(s_index[0])

        print(e_index, q[0])
        data["Time (s)"] = np.concatenate(data["Time (s)"], r[0][0][s_index:e_index])
        data["Speed (m/s)"] = np.concatenate(data["Speed (m/s)"], r[0][1][s_index:e_index])

    # s_index, = np.where(np.isclose(r[0][0], r[1][0][0]))
    # e_index, = np.where(np.isclose(r[0][0], r[1][-1][1]))

    # data["Time (s)"] = r[0][0][s_index:e_index]
    # data["Speed (m/s)"] = r[0][1][s_index:e_index]

    return pd.DataFrame(data)


def download_light_data(analysed, path):

    eArr = np.repeat("", len(analysed[0][0]))
    eArr[0] = analysed[3]

    time = {True: 'time_rel(sec)', False: 'rel_time(sec)'}[analysed[4].upper() == 'A']
    velocity = {True: 'velocity(m/s)', False: 'velocity(c/s)'}[analysed[4].upper() == 'A']
    ab_tim = {True: 'time_abs(%Y-%m-%dT%H:%M:%S.%f)', False: "time(%Y-%m-%dT%H:%M:%S.%f)"}[analysed[4].upper() == 'A']

    data = {ab_tim: eArr,time:analysed[0][0], velocity: analysed[0][1]}

    df = pd.DataFrame(data)
    df.to_csv(path+".LightData.csv", index=False, header=True)

    quakes = {"Start":[], "End":[]}

    for q in analysed[1]:
        quakes["Start"].append(q[0])
        quakes["End"].append(q[1])

    qdf = pd.DataFrame(quakes)
    qdf.to_csv(path+".Quakes.csv", index=True, header=True)

def analyse(path, t):
    path = path.replace('"', '')
    if (t.lower() == "a"):
        return analyze_moon("", path)
    elif (t.lower() == "b"):
        return analyze_mars("", path)


def read_and_filter_csv():
    filepath = str(input("Write file path: ")).replace('"', "")
    try:
        moon_mars = str(input("Is it a moon (A) or mars (B) file: "))
        file = pd.read_csv(filepath)
        time = {True: 'time_rel(sec)', False: 'rel_time(sec)'}[moon_mars.upper() == 'A']
        velocity = {True: 'velocity(m/s)', False: 'velocity(c/s)'}[moon_mars.upper() == 'A']
        intervalos_tiempo = analyse(filepath, moon_mars)[1]
        seismic_wave = pd.DataFrame(columns=list(file.columns.values))
        for i, f, _ in intervalos_tiempo:
            seismic_wave = pd.concat([seismic_wave, file[file[time].isin([int(i) + t for t in range(1, int(f - i) + 1)])]])
        ratio = seismic_wave.shape[0] / file.shape[0]
        return seismic_wave, time, velocity, ratio
    except FileNotFoundError:
        print("File not found")


def draw_wave(w, t, v, r):
    csv_times = np.array(w[t].tolist())
    csv_data = np.array(w[v].tolist())
    # Plot the trace!
    fig,ax = plt.subplots(1,1,figsize=(10,3))
    ax.plot(csv_times,csv_data)
    # Make the plot pretty
    #ax.set_xlim([min(csv_times),max(csv_times)])
    ax.set_ylabel('Velocity (m/s)')
    ax.set_xlabel('Time (s)')
    ax.set_title(f'Filtered wave. It is {int(1/r)} times smaller', fontweight='bold')
    # Plot where the arrival time is

    plt.show()

def download_wave(w, path):
    w.to_csv(path+".LightData.csv", index=False, header=True)

# for n in range(1, 5):
#     l = str(input(""))
#     r = analyse(l, "A")
#     download_light_data(r, "C:/Users/Usuario/Downloads/NasaSpaceApps2024/DataAnalysed/MoonWave"+str(n))

final = read_and_filter_csv()
draw_wave(*final)

#download_wave(final[0], "C:/Users/Usuario/Downloads/NasaSpaceApps2024/FilteredWaves/ShortenWave3.csv")