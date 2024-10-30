import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import shapiro


# read in files written by export_necrosis.groovy
basepath = '/path/to/folder/and/folder2'

folder = 'alldata_necrosis/output' # relevant for 25868 and 14550
folder2 = '11571_necrosis/output' # relevant for 11571


## 25868
csv_healthy25868 = glob.glob(basepath + folder + r'/25868$1.?$HE$HE$OR$001*.svs Annotations.txt') # healthy
csv_sick25868 = glob.glob(basepath + folder + r'/25868$2.?$HE$HE$OR$001*.svs Annotations.txt') # sick
csv_treatment = glob.glob(basepath + folder + r'/25868$3.?$HE$HE$OR$001*.svs Annotations.txt') # treatment
csv_prophylaxis = glob.glob(basepath + folder + r'/25868$4.?$HE$HE$OR$001*.svs Annotations.txt') # prophylaxis 


## 14550 
csv_healthy14550 = glob.glob(basepath + folder + r'/14550$A?_PBS$HE$HE$OR$001.svs Annotations.txt') # healthy
csv_sick14550IV = glob.glob(basepath + folder +'/14550$B*$HE$HE$OR$001.svs Annotations.txt')    # sick IV
csv_sickIP =  glob.glob(basepath + folder +'/14550$C*$HE$HE$OR$001.svs Annotations.txt')    # sick IP

csv1mgIV = glob.glob(basepath + folder + r'/14550$D?_P13_1mg_IV$HE$HE$OR$001.svs Annotations.txt') # 1mg IV
csv1mgIP = glob.glob(basepath + folder + r'/14550$E?_P13_1mg_IP$HE$HE$OR$001.svs Annotations.txt') # 1mg IP
csv2_5mgIV = glob.glob(basepath + folder + r'/14550$F?_P13_2.5mg_IV$HE$HE$OR$001.svs Annotations.txt') # 2.5mg IV
csv2_5mgIP = glob.glob(basepath + folder + r'/14550$G?_P13_2.5mg_IP$HE$HE$OR$001.svs Annotations.txt') # 2.5mg IP
csv5mgIV = glob.glob(basepath + folder + r'/14550$H?_P13_5mg_IV$HE$HE$OR$00*.svs Annotations.txt') # 5mg IV
csv5mgIP = glob.glob(basepath + folder + r'/14550$I?_P13_5mg_IP$HE$HE$OR$001.svs Annotations.txt') # 5mg IP                                   

## 11571
csv_healthy11571 = glob.glob(basepath + folder2 + r'/11571$Group1*$US$SCAN$OR$001*.svs Annotations.txt') # healthy
csv_sick11571 = glob.glob(basepath + folder2 + r'/11571$Group2*$US$SCAN$??$001*.svs Annotations.txt') # sick
csv_bpti11571 = glob.glob(basepath + folder2 + r'/11571$Group3*$US$SCAN$OR$001*.svs Annotations.txt') # bpti
csv_spink11571 = glob.glob(basepath + folder2 + r'/11571$Group4*$US$SCAN$OR$001*.svs Annotations.txt') # spink


def prepcsvs(csvs):
    '''Read in csvs and concatenate them into one dataframe'''
    dfs = [pd.read_csv(f, sep='\t') for f in csvs]
    df = pd.concat(dfs, ignore_index=True)
    return df


def prepare_data(df):
    """ Input: dataframe of image features
        Output: dataframe with one row per image, containing the ratio of necrotic cells to exocrine cells
    """
    # unique list of images 
    image_names = df.Image.unique()

    rowlist = [] # One row per image
    for name in image_names:
        exobool = df[df.Image == name].Classification == "Exocrine"
        exocrine_a = df[df.Image == name][exobool]['Area µm^2'].values[0] # exocrine area

        necrobool = df[df.Image == name].Classification == "Necrosis"
        necrosis_a = df[df.Image == name][necrobool]['Area µm^2'] # necrosis area
        if len(necrosis_a) == 0: # if no necrosis
            necrosis_a = 0
        else:
            necrosis_a = necrosis_a.values[0]

        new_row = {'Image': name, 'Exocrine_a': exocrine_a, 'Necrosis_a': necrosis_a, 'ratio': 100 * (necrosis_a/exocrine_a)}
        rowlist.append(new_row)

    results = pd.DataFrame(rowlist)
    return results

def getlowSEM(results): 
    '''Get lower bound of SEM'''
    return np.mean(results['ratio']) - stats.sem(results['ratio'])

def gethighSEM(results):
    '''Get upper bound of SEM'''
    return np.mean(results['ratio']) + stats.sem(results['ratio'])

def areaweight(df): 
    '''Mean weighted by exocrine area'''
    total_a = np.sum(df['Exocrine_a'])
    total_a_n = np.sum(df['Necrosis_a'])
    return 100 * (total_a_n/total_a)


## Read in dataframe from CSV
# 25868
df_healthy = prepcsvs(csv_healthy25868)
df_sick = prepcsvs(csv_sick25868)
df_prophylaxis = prepcsvs(csv_prophylaxis)
df_treatment = prepcsvs(csv_treatment)

# 14550
df_healthy14550 = prepcsvs(csv_healthy14550)
df_sick14550IV = prepcsvs(csv_sick14550IV)
df_sickIP = prepcsvs(csv_sickIP)
df1mgIV = prepcsvs(csv1mgIV)
df1mgIP = prepcsvs(csv1mgIP)
df2_5mgIV = prepcsvs(csv2_5mgIV)
df2_5mgIP = prepcsvs(csv2_5mgIP)
df5mgIV = prepcsvs(csv5mgIV)
df5mgIP = prepcsvs(csv5mgIP)

# 11571
df_healthy11571 = prepcsvs(csv_healthy11571)
df_sick11571 = prepcsvs(csv_sick11571)
df_spink11571 = prepcsvs(csv_spink11571)
df_bpti11571 = prepcsvs(csv_bpti11571)


## dataframe: One row per image, columns: Image name, exocrine area, necrotic area, ratio of necrotic to exocrine area
# 25868
results_healthy = prepare_data(df_healthy)
results_sick = prepare_data(df_sick)
results_prophylaxis = prepare_data(df_prophylaxis)
results_treatment = prepare_data(df_treatment)

# 11571
results_healthy11571 = prepare_data(df_healthy11571)
results_sick11571 = prepare_data(df_sick11571)
results_spink11571 = prepare_data(df_spink11571)
results_bpti11571 = prepare_data(df_bpti11571)

# 14550
results_healthy14550 = prepare_data(df_healthy14550)
results_sick14550IV = prepare_data(df_sick14550IV)
results_sickIP = prepare_data(df_sickIP)
results1mgIV = prepare_data(df1mgIV)
results1mgIP = prepare_data(df1mgIP)
results2_5mgIV = prepare_data(df2_5mgIV)
results2_5mgIP = prepare_data(df2_5mgIP)
results5mgIV = prepare_data(df5mgIV)
results5mgIP = prepare_data(df5mgIP)


## Plotting
def plot_violin(results, title): 
    fig, ax = plt.subplots()
    violins = ax.violinplot([result['ratio'] for result in results], showmeans=True, showmedians=False)


    linec = 'dimgrey'
    violins['cbars'].set_edgecolor(linec)
    violins['cmins'].set_edgecolor(linec)
    violins['cmaxes'].set_edgecolor(linec)
    violins['cmeans'].set_edgecolor(linec)

    for i, result in enumerate(results): 
        ax.scatter(np.random.normal(i+1, 0.05, len(result['ratio'])), result['ratio'], c = 'k')
        ax.scatter(i+1, areaweight(result), marker = 'D', c = 'blue')
        ax.scatter(i+1, getlowSEM(result), marker = '_', c = 'red')
        ax.scatter(i+1, gethighSEM(result), marker = '_', c = 'red')

    for body in violins['bodies']:
        body.set_facecolor('gray')


    ax.set_ylabel('necrotic cells : tissue area [%]', fontsize=16)
    ax.set_xlabel('Treatment', fontsize=16)
    ax.tick_params(axis='y', labelsize=13)
    ax.set_xticks(range(1, len(results)+1))
    ax.set_xticklabels(title, fontsize=13)

# 25868
plot_violin([results_healthy, results_sick, results_treatment, results_prophylaxis], ["PBS", "Caer", "Caer/\nFc-SPINK1", "Caer/\nFc-SPINK1 proph"])

# 25868 without 2.2 and 2.3    
results_sick_clean = results_sick[~results_sick['Image'].str.contains('2.2')] # remove 2.2
results_sick_clean = results_sick_clean[~results_sick_clean['Image'].str.contains('2.3')] # remove 2.3

plot_violin([results_healthy, results_sick_clean, results_treatment, results_prophylaxis], ["PBS", "Caer clean", "Caer/\nFc-SPINK1", "Caer/\nFc-SPINK1\nproph"])


# 14550 IV
plot_violin([results_healthy14550, results_sick14550IV, results1mgIV, results2_5mgIV, results5mgIV], ["PBS", "Caerulein", "1 mg IV", "2.5 mg IV", "5 mg IV"])

# 14550 IP
plot_violin([results_healthy14550, results_sickIP, results1mgIP, results2_5mgIP, results5mgIP], ["PBS", "Caerulein", "1 mg IP", "2.5 mg IP", "5 mg IP"])

# 11571
plot_violin([results_healthy11571, results_sick11571, results_bpti11571, results_spink11571], ["PBS", "Caerulein", "Fc-BPTI", "Fc-SPINK1"])

# 11571 without image 2.5
results_sick11571_no2_5 = results_sick11571[results_sick11571['ratio'] != results_sick11571['ratio'][0]]
plot_violin([results_healthy11571, results_sick11571_no2_5, results_bpti11571, results_spink11571], ["PBS", "Caerulein", "Fc-BPTI", "Fc-SPINK1"])

# 11571 without 2.5, sick and bpti combined
combined = pd.concat([results_sick11571_no2_5, results_bpti11571], ignore_index=True)
plot_violin([results_healthy11571, results_sick11571_no2_5, results_bpti11571, combined, results_spink11571], ["PBS", "Cer", "Cer/\nFc-BPTI", "Cer + Cer/\nFc-BPTI", "Cer/\nFc-SPINK1"])
plt.show()

##### Statistical tests
# Test for normality 
W = [] 
p = []

## Test for normality using Shapiro-Wilk test
totest = [results_healthy14550, results_sickIP, results1mgIP, results2_5mgIP, results5mgIP, results_sick14550IV, results1mgIV, results2_5mgIV, results5mgIV, results_healthy11571, results_sick11571_no2_5, results_bpti11571, results_spink11571, combined, results_healthy, results_sick, results_prophylaxis, results_treatment]
not_normal = []

for i in totest:
    W.append(shapiro(i['ratio'])[0])
    p.append(shapiro(i['ratio'])[1])
    if shapiro(i['ratio'])[1] < 0.05:
        not_normal.append(i['Image'])


print("the following batches are unlikely to be normal distributed", not_normal)


def logodds(results): 
    p = results['ratio']/100
    q = 1 - p 
    return p/q


def welchs(one, two, logodds, message = None):
    odds1 = logodds(one)
    odds2 = logodds(two)
    if message:
        print(message)
    print(stats.ttest_ind(odds1, odds2, alternative='greater', equal_var=False))


def mannwhitney(one, two, message = None):
    if message:
        print("MWU: ", message)
    print(stats.mannwhitneyu(one, two, alternative='greater', method='exact'))


# 11571
print('healthy11571 ', shapiro(results_healthy11571['ratio'])) # probably not normal
print('sick11571 ', shapiro(results_sick11571_no2_5['ratio']))
print('bpti11571 ', shapiro(results_bpti11571['ratio']))
print('spink11571 ', shapiro(results_spink11571['ratio'])) # probably not normal
print('bpti11571 + sick11571 ', shapiro(combined['ratio']))

mannwhitney(combined['ratio'], results_spink11571['ratio'], message='caer + bpti vs spink:')
mannwhitney(results_sick11571_no2_5['ratio'], results_spink11571['ratio'], message='caer vs spink:')
mannwhitney(results_sick11571_no2_5['ratio'], results_bpti11571['ratio'], message='caer vs bpti:')
mannwhitney(results_sick11571_no2_5['ratio'], results_healthy11571['ratio'], message='caer vs healthy:')


# 25868
print('healthy25868 ', shapiro(results_healthy['ratio'])) # probably not normal
print('sick25868 ', shapiro(results_sick['ratio'])) # probably not normal
print('sick25868 clean ', shapiro(results_sick_clean['ratio'])) 
print('prophylaxis25868 ', shapiro(results_prophylaxis['ratio'])) # probably not normal
print('treatment25868 ', shapiro(results_treatment['ratio']))

mannwhitney(results_sick['ratio'], results_prophylaxis['ratio'], message='caer vs prophylaxis:')
mannwhitney(results_sick['ratio'], results_treatment['ratio'], message='caer vs treatment:')
mannwhitney(results_sick['ratio'], results_healthy['ratio'], message='caer vs healthy:')

mannwhitney(results_sick_clean['ratio'], results_prophylaxis['ratio'], message='caer clean vs prophylaxis:')
mannwhitney(results_sick_clean['ratio'], results_treatment['ratio'], message='caer clean vs treatment:')
mannwhitney(results_sick_clean['ratio'], results_healthy['ratio'], message='caer clean vs healthy:')


# 14550 IV
print('sick14550IV ', shapiro(results_sick14550IV['ratio'])) 
print('1mgIV ', shapiro(results1mgIV['ratio']))
print('2.5mgIV ', shapiro(results2_5mgIV['ratio']))
print('5mgIV ', shapiro(results5mgIV['ratio']))
print('healthy14550 ', shapiro(results_healthy14550['ratio']))

welchs(results_sick14550IV, results5mgIV, logodds, message='caer IV vs 5mg IV:')
welchs(results_sick14550IV, results2_5mgIV, logodds, message='caer IV vs 2.5mg IV:')
welchs(results_sick14550IV, results_healthy14550, logodds, message='caer IV vs healthy:')


# 14550 IP
print('healthy14550 ', shapiro(results_healthy14550['ratio']))
print('sickIP ', shapiro(results_sickIP['ratio']))
print('1mgIP ', shapiro(results1mgIP['ratio']))
print('2.5mgIP ', shapiro(results2_5mgIP['ratio']))
print('5mgIP ', shapiro(results5mgIP['ratio']))

welchs(results_sickIP, results1mgIP, logodds, message='caer IP vs 1mg IP:')
welchs(results_sickIP, results2_5mgIP, logodds, message='caer IP vs 2.5mg IP:')
welchs(results_sickIP, results5mgIP, logodds, message='caer IP vs 5mg IP:')
welchs(results_sickIP, results_healthy14550, logodds, message='caer IP vs healthy:')



