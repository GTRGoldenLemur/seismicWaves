#py -3 -m pip install pandas
#C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe -m pip install --upgrade pip
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

file_name =  "xa.s12.00.mhz.1970-04-25HR00_evid00006" #"xa.s12.00.mhz.1970-03-26HR00_evid00004" #"xa.s12.00.mhz.1970-03-25HR00_evid00003"
cat_file = "C:/Users/Usuario/Downloads/NasaSpaceApps2024/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/"+file_name+".csv"
cat = pd.read_csv(cat_file)


moon_cata = get_moon_catalog()
moon_q = get_moon_mq(moon_cata, file_name)

print(moon_q)



csv_times = np.array(cat['time_rel(sec)'].tolist())
csv_data = np.array(cat['velocity(m/s)'].tolist())

fig,ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(csv_times,csv_data)
#ax.set_ylim(av)

def average(a=0, b=len(csv_data))->float:
    a = int(max(0, a))
    b = int(min(b, len(csv_data)))
    
    sum = 0
    for s in csv_data[a:b]:
        sum+=abs(s)
    return sum/(b-a)

av = average()

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


for t in moon_q:
    ax.axvline(x=t[1], c="orange", linestyle=":")

plt.show()