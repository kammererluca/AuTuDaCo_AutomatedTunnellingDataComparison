#!/usr/bin/env python
# coding: utf-8

# # AuTuDaCo - Automized Tunneling Data Comparsion

# In[1]:


import pandas as pd


# In[2]:


import numpy as np


# In[3]:


import matplotlib.pyplot as plt
import matplotlib as mpl


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


#%matplotlib inline#GUI toolkit (inline, notebook, tk) können gewechselt werden


# 

# # expected data

# In[6]:


def einlesen(index):
    path = index # Soll-Daten
    df = pd.read_excel(path) # Daten einlesen
    df = df.transpose() #Zeilen mit Spalten vertauschen
    df.columns = df.iloc[0] # Spaltenüberschriften setzen
    df = df.iloc[1:]
    df = df.iloc[::2] # jede zweite Zeile löschen
    df = df.reset_index() # index reset
    df = df.rename({'index' : 'HB'}, axis=1) # rename index to HB
    df = df.rename({'km (from-to)' : 'HB start [m]'}, axis=1) # rename index to HB
    HB_end = df['HB start [m]'] + df['length [m]'] # neue variable mit HB Endwerten 
    df.insert(2, 'HB end [m]', HB_end) # HB Endwerte als Spalte im Dataframe einfügen
    df = df.apply(pd.to_numeric, errors='coerce') # alle im Dataframe in  ein numerisches Format übertragen
    df = df.iloc[1:]
    df = df.drop(df.columns[[0]], axis=1)
    return df
    df.close()
df = einlesen(r"C:\Users\luca9\Documents\UNI\Bachelorarbeit\read_excel_python\Bsp.Daten_form.xlsx")
df


# # Rock mass type (RMT`)

# In[7]:


def rmt_go(df, index1, index2):
    rmt = df.iloc[0:,index1:index2] # gibt alle Werte für RMT zurück
    rmt.isnull()
    rmt.dropna() # löscht Zeilen ohne Werte
    rmt.dropna(axis=1) # löscht Spalten ohne Werte
    rmt['sum'] = rmt.iloc[:,3:32].sum(axis=1) # Addiert die Werte aus jeder Zeile und neue Spalte 'sum'
    length = rmt['HB end [m]'].iloc[-1:] # nimmt den letzten Wert aus HB_end und wandelt den Eintrag in eine Zahl um
    rmt['percent'] = rmt.iloc[:,4:32].sum(axis=0)
    rmt['percent'] = round(rmt['sum']/int(length)*100,2) # length umwandeln in int Variable
    tot_percent = rmt['percent'].sum(axis=0) # Kontrolle ob in Summe genau 100%
    tot_length = rmt['sum'].sum(axis=0) # Kontrolle ob in Summe genau die Tunnel-Länge
    rmt.loc['Sum', 3:] = rmt.sum(axis=0) #neue Zeile einfügen und Summe für jeden RMT
    rmt1 = rmt.loc['percent', 3:] = round(rmt.loc['Sum']/int(length)*100,2) # prozentueller Anteil für jeden RMT
    return rmt, tot_length, tot_percent # Speichert die verwendeten Variablen ab und schließt die Funktion
    rmt.close()
rmt, tot, per = rmt_go(df, 0, 31)
rmt


# # Anteil an RMT` je HB

# In[8]:


df_percentage = pd.DataFrame()
a = np.arange(18)
for number in a:
    xs = []
    for i in rmt.iloc[number,3:-2]: # rmt1 zu rmt verändert
        if i == 0:
            xs.append(0)
        elif i != 0:
            xs.append(round(i,2))
    ys = [round(x*100/rmt['length [m]'],2).iloc[number] for x in xs] # rmt1 zu rmt verändert
    df_percentage[f'HB {number}'] = ys
print(df_percentage)


# In[9]:


tmp_df = df_percentage.transpose()
tmp_df.plot(kind="bar",figsize=(30,8))
plt.legend(loc="upper left")
plt.ylabel('percentage')
plt.show()

df_percentage.transpose().plot(kind='bar',figsize=(25,10),stacked=True)
plt.legend()
plt.show()


# # Support type (ST`)

# In[72]:


def st_go(df, index1, index2):
    st = df.iloc[0:,index1:index2] # gibt alle Werte für ST zurück
    st.isnull() # gibt boolean Werte false/true aus wenn ein Eintrag null ist
    st.dropna() # löscht Zeilen ohne Werte
    st.dropna(axis=1) # löscht Spalten ohne Werte
    st['sum'] = st.iloc[:,0:].sum(axis=1) # Addiert die Werte aus jeder Zeile und fügt eine neue Spalte 'sum' hinzu
    length = df['HB end [m]'].iloc[-1:]
    st['percent'] = round((st['sum']/int(length))*100,2)
    tot_percent = st['percent'].sum(axis=0) # Kontrolle ob in Summe genau 100%
    tot_length = st['sum'].sum(axis=0)
    st.loc['Sum', 0:] = st.sum(axis=0) #fügt eine neue Zeile ein und bildet die Summe für jeden ST
    st.loc['percent', 0:-1] = round(st.loc['Sum']/int(length)*100,2) #berechnet den prozentuellen Anteil für jedes ST
    return st, tot_length, tot_percent
    st.close()
st, tot, per = st_go(df, 31, 47)
st
# print(st2)
# Die Fehlermeldung warnt, dass das Verwenden von .loc[] in diesem Zusammenhang in Zukunft zu Type errors führen kann
# An der Stelle von .loc[] sollte daher .iloc[] mit Positionen verwendet werden


# ## Anteil ST je HB

# In[71]:


df_percentage_st = pd.DataFrame()
b = np.arange(18)
for number in b:
    xs_st = []
    for i in st.iloc[number,0:-2]:
        if i == 0:
            xs_st.append(0)
        elif i != 0:
            xs_st.append(round(i,2))
    ys_st = [round(x*100/st['sum'],2).iloc[number] for x in xs_st]
    df_percentage_st[f'HB {number}'] = ys_st
    print(xs_st)
    print(ys_st)
    print('------')
print(df_percentage_st)


# In[48]:


tmp_df_st = df_percentage_st.transpose()
tmp_df_st.plot(kind="bar",figsize=(17,6))
plt.legend(loc="upper left")
plt.ylabel('percentage')
plt.show() 


df_percentage_st.transpose().plot(kind='bar',figsize=(17,6),stacked=True)
plt.legend()
plt.legend(["RMT20","RMT21","RMT22","RMT3","RMT24","RMT5","RMT26","RMT27","RMT7","RMT19"])
plt.show()


# # system behaviour (SB`)

# In[70]:


def sb_go(df, index1, index2):
    sb = df.iloc[0:,index1:index2] # gibt alle Werte für ST zurück
    sb.isnull() # gibt boolean Werte false/true aus wenn ein Eintrag null ist
    sb.dropna() # löscht Zeilen ohne Werte
    sb.dropna(axis=1) # löscht Spalten ohne Werte
    sb['sum'] = sb.iloc[:,0:].sum(axis=1) # Addiert die Werte aus jeder Zeile und fügt eine neue Spalte 'sum' hinzu
    length = df['HB end [m]'].iloc[-1:]
    sb['percent'] = round((sb['sum']/int(length))*100,2)
    tot_percent = sb['percent'].sum(axis=0) # Kontrolle ob in Summe genau 100%
    tot_length = st['sum'].sum(axis=0)
    sb.loc['Sum', 0:] = sb.sum(axis=0) #fügt eine neue Zeile ein und bildet die Summe für jeden ST
    sb.loc['percent', 0:-1] = round(sb.loc['Sum']/int(length)*100,2) #berechnet den prozentuellen Anteil für jedes ST
    return sb, tot_length, tot_percent
    sb.close()
sb, tot, per = sb_go(df, 47, 56)
sb


# # Percentage of SB per HB

# In[14]:


df_percentage_sb = pd.DataFrame()
b = np.arange(9)
for number in b:
    xs_sb = []
    for i in sb.iloc[number,0:-2]:
        if i == 0:
            xs_sb.append(0)
        elif i != 0:
            xs_sb.append(round(i,2))
    ys_sb = [round(x*100/sb['sum'],2).iloc[number] for x in xs_sb]
    df_percentage_sb[f'HB {number}'] = ys_sb


# In[15]:


# Die Breite der HB sollte in die Balken miteinfließen

tmp_df_sb = df_percentage_sb.transpose()
tmp_df_sb.plot(kind="bar",figsize=(30,8))
plt.legend(loc="upper left")
plt.ylabel('percentage')
plt.grid(True)
plt.show() # Die values müssen die Information der RMT's beinhalten.

df_percentage_sb.transpose().plot(kind='bar',figsize=(25,10),stacked=True, width = 0.9)
plt.legend()
plt.grid(True)
# plt.legend(["RMT20","RMT21","RMT22","RMT3","RMT24","RMT5","RMT26","RMT27","RMT7","RMT19"])
plt.show()
# Legende sollte die verschiedenen RMT's beinhalten


# # real data

# In[16]:


df2 = einlesen(r"C:\Users\luca9\Documents\UNI\Bachelorarbeit\read_excel_python\Bsp.Daten_form - IST - aktuell.xlsx")


# # Rock mass type (RMT)

# In[69]:


rmt2, tot, per = rmt_go(df2, 0, 31)
rmt2


# # RMT - Comparison (Expected data - real data)

# In[18]:


def _color_red(value):
    color = 'red' if value != 0 else 'black'  
    return 'color: %s' % color

def vergleich(rmt, rmt2):
    rmt_diff = rmt.copy()
    for y in range(rmt.shape[0]):
        for x in range(rmt.shape[1]):
            if(rmt.iloc[y, x] != rmt2.iloc[y, x]):
                rmt_diff.iloc[y, x] = rmt.iloc[y, x] - rmt2.iloc[y, x]
    
   
    rmt_diff = rmt_diff.style.applymap(_color_red, subset=rmt_diff.columns[3:-2])
    return rmt_diff
  
rmt_diff = vergleich(rmt, rmt2)

rmt_diff


# # Percentage RMT per HB

# In[68]:


df2_percentage_rmt2 = pd.DataFrame()
b = np.arange(18)
for number in b:
    xs_rmt2 = []
    for i in rmt2.iloc[number,3:-2]:
        if i == 0:
            xs_rmt2.append(0)
        elif i != 0:
            xs_rmt2.append(round(i,2))
    ys_rmt2 = [round(x*100/rmt2['sum'],2).iloc[number] for x in xs_rmt2]
    df2_percentage_rmt2[f'HB {number}'] = ys_rmt2
    print(xs_rmt2)
    print(ys_rmt2)
    print('------')
print(df2_percentage_rmt2)


# # RMT_expected & RMT_real
# ### taking into account the width of HB

# In[67]:


#-----------------------------------------------------------------------------------'
# work in progress
#-----------------------------------------------------------------------------------'
# df_percentage_array = df_percentage_rmt.cumsum(axis=0).values # kumulative Summe ueber die Reihen (in Richtung Column)
# df2_percentage_array = df2_percentage_rmt2.cumsum(axis=0).values

# fig, ax = plt.subplots(figsize=(24, 8)) # erstellt plot mit einem Axis (ax) element

# ax.bar(x_pos_ist, df_percentage_array[0], width=width, label=f'ST{0}_soll')
# ax.bar(x_pos_soll, df2_percentage_array[0], width=width, label=f'ST{0}_ist')
# for i in range(15):
#    # ax.bar(x_pos_ist,y_ist[i][1:], width=width, label=f'SB{i}') # label damit pyhton weiß was in Legende zu schreiben
#     ax.bar(x_pos_ist, df_percentage_array[i+1]-df_percentage_array[i], bottom=df_percentage_array[i], width=width, label=f'ST{i+1}_soll')
#     ax.bar(x_pos_soll, df2_percentage_array[i+1]-df2_percentage_array[i], bottom=df2_percentage_array[i], width=width, label=f'ST{i+1}_ist')
#     plt.xticks(x_pos_label, x_label)
#     plt.legend()
#     plt.tight_layout()
#     plt.grid(True)


# # Support type (ST) - Comparsion

# In[65]:


st2, tot, per = st_go(df2, 31, 47)
st2


# In[22]:


def _color_red(value):
    color = 'red' if value != 0 else 'black'  
    return 'color: %s' % color

def vergleich(st, st2):
    st_diff = st.copy()
    for y in range(st.shape[0]):
        for x in range(st.shape[1]):
            if(st.iloc[y, x] != st2.iloc[y, x]):
                st_diff.iloc[y, x] = st.iloc[y, x] - st2.iloc[y, x]
    
   
    st_diff = st_diff.style.applymap(_color_red, subset=st_diff.columns[0:-2])
    return st_diff
  
st_diff = vergleich(st, st2)

st_diff


# # Percentage ST per HB

# In[64]:


df2_percentage_st2 = pd.DataFrame()
b = np.arange(18)
for number in b:
    xs_st2 = []
    for i in st2.iloc[number,0:-2]:
        if i == 0:
            xs_st2.append(0)
        elif i != 0:
            xs_st2.append(round(i,2))
    ys_st2 = [round(x*100/st2['sum'],2).iloc[number] for x in xs_st2]
    df2_percentage_st2[f'HB {number}'] = ys_st2
    print(xs_st2)
    print(ys_st2)
    print('------')
print(df2_percentage_st2)


# # system behaviour (SB)

# In[61]:


sb2, tot, per = sb_go(df2, 47, 57)
sb2


# # Comparsion SB_expected / SB_real

# In[60]:


def _color_red(value):
    color = 'red' if value != 0 else 'black'  
    return 'color: %s' % color

def vergleich(sb, sb2):
    sb_diff = sb.copy()
    for y in range(sb.shape[0]):
        for x in range(sb.shape[1]):
            if(sb.iloc[y, x] != sb2.iloc[y, x]):
                sb_diff.iloc[y, x] = sb.iloc[y, x] - sb2.iloc[y, x]
    
   
    sb_diff = sb_diff.style.applymap(_color_red, subset=sb_diff.columns[0:-2])
    return sb_diff
  
sb_diff = vergleich(sb, sb2)

display(sb_diff)


# # percentual distribution of SB per HB

# In[59]:


df2_percentage_sb2 = pd.DataFrame()
b = np.arange(9)
for number in b:
    xs_sb2 = []
    for i in sb2.iloc[number,0:-2]:
        if i == 0:
            xs_sb2.append(0)
        elif i != 0:
            xs_sb2.append(round(i,2))
    ys_sb2 = [round(x*100/sb2['sum'],2).iloc[number] for x in xs_sb2]
    df2_percentage_sb2[f'HB {number}'] = ys_sb2
    print(xs_sb2)
    print(ys_sb2)
    print('------')
print(df2_percentage_sb2)


# In[28]:


# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:42:43 2022

@author: unterl12
"""
# =============================================================================
# import data
# =============================================================================
import pandas as pd

df = pd.read_excel(r"C:\Users\luca9\Documents\UNI\Bachelorarbeit\read_excel_python\Bsp.Daten_form.xlsx") # Daten einlesen
df = df.transpose() # Zellen mit Spalten vertauschen
df.columns = df.iloc[0] # Spaltenüberschriften setzen
df = df.iloc[1:] # erste leere Zeilen vor HB1 löschen
df = df.iloc[::2] # jede zweite Zeile löschen
df = df.reset_index()
df = df.rename({'index' : 'HB'}, axis=1) # rename index to HB
df = df.rename({'km (from-to)' : 'HB start [m]'}, axis=1) # rename index to HB
HB_end = df['HB start [m]'] + df['length [m]'] # neue variable mit HB Endwerten 
df.insert(2, 'HB end [m]', HB_end) # HB Endwerte als Spalte im Dataframe einfügen
df = df.apply(pd.to_numeric, errors='coerce') # alle im Dataframe in  ein numerisches Format übertragen
#df.loc[df['RMT 1'] == 0, 'RMT2.1'] = 1
#df['RMT 1'].iloc[-1:]
# df = df.drop(df.index[[0]]) #0te Zeile hat nan values -> diese wird gelölscht

df2 = pd.read_excel(r"C:\Users\luca9\Documents\UNI\Bachelorarbeit\read_excel_python\Bsp.Daten_form - IST - aktuell.xlsx") # Daten einlesen
df2 = df2.transpose() # Zellen mit Spalten vertauschen
df2.columns = df2.iloc[0] # Spaltenüberschriften setzen
df2 = df2.iloc[1:] # erste leere Zeilen vor HB1 löschen
df2 = df2.iloc[::2] # jede zweite Zeile löschen
df2 = df2.reset_index() # index reset
df2 = df2.rename({'index' : 'HB'}, axis=1) # rename index to HB
df2 = df2.rename({'km (from-to)' : 'HB start [m]'}, axis=1) # rename index to HB
HB_end2 = df2['HB start [m]'] + df2['length [m]'] # neue variable mit HB Endwerten 
df2.insert(2, 'HB end [m]', HB_end2) # HB Endwerte als Spalte im Dataframe einfügen
df2 = df2.apply(pd.to_numeric, errors='coerce') # alle im Dataframe in  ein numerisches Format übertragen
#df2 = df2.drop(df2.index[[0]])

df['sum_RMT'] = df.iloc[:,4:32].sum(axis=1)
df2['sum_RMT'] = df2.iloc[:,4:32].sum(axis=1)
#print(df2_sb)
# =============================================================================
# arrange data for plotting
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np


df_transp = df.transpose()
df_sb = df_transp.iloc[48:-1] # filtern nach support behvaiour

df2_transp = df2.transpose()
df2_sb = df2_transp.iloc[48:-1] # filtern nach support behvaiour

x_label = ['HB0_ist', 'HB0_soll', 'HB1_ist', 'HB1_soll', 'HB2_ist', 'HB2_soll',
           'HB3_ist', 'HB3_soll', 'HB4_ist', 'HB4_soll', 'HB5_ist', 'HB5_soll',
           'HB6_ist', 'HB6_soll', 'HB7_ist', 'HB7_soll', 'HB8_ist', 'HB8_soll',
           'HB9_ist', 'HB9_soll', 'HB10_ist', 'HB10_soll', 'HB11_ist', 'HB11_soll',
           'HB12_ist', 'HB12_soll', 'HB13_ist', 'HB13_soll', 'HB14_ist', 'HB14_soll',
           'HB15_ist', 'HB15_soll', 'HB16_ist', 'HB16_soll', 'HB17_ist', 'HB17_soll']

x_pos_ist = np.arange(0,36,2)
x_pos_soll = np.arange(1,37,2)
x_pos_label = np.arange(0,36,1)

y_ist=[] # leere liste für ist Werte
for i in range(9): # schleife die jede Zeile aus dataframe mit support behaviour der liste hinzufügt
    y_ist.append(df2_sb.iloc[i].values)
    
y_soll = [] # ditto für soll Werte
for i in range(1,9):
    y_soll.append(df_sb.iloc[i].values) # change dataframe to dataframe with soll values
    
width = [] # leere Liste für Breite der bars
for i in range(18):
    width.append(round(df['length [m]'][i]/df['length [m]'].max(), 2)) # ith value in df / max length of columns
    #width.append(round(df['length [m]'][i]/df['length [m]'].sum() *5, 2)) # ith vaue in df / Gesamtlänge

# =============================================================================
# plot - here the problem is that the bars are not stacked!!
# =============================================================================

# fig, ax = plt.subplots(figsize=(24, 6)) # erstellt plot mit einem Axis (ax) element

# for i in range(8):
#     ax.bar(x_pos_ist,y_ist[i][1:], width=width, label=f'ST{i}') # label damit pyhton weiß was in Legende zu schreiben
#     ax.bar(x_pos_soll, y_soll[i][1:], width=width, label=f'ST{i}')
#     plt.xticks(x_pos_label, x_label)
#     plt.legend()
#     plt.tight_layout()


# In[58]:


# df_percentage_array = df_percentage_st.cumsum(axis=0).values # kumulative Summe ueber die Reihen (in Richtung Column)
# #df2_percentage_array = df2_percentage_st.cumsum(axis=0).values

# fig, ax = plt.subplots(figsize=(24, 6)) # erstellt plot mit einem Axis (ax) element

# ax.bar(x_pos_ist, df_percentage_array[0], width=width, label=f'ST{0}')
# for i in range(15):
# #     ax.bar(x_pos_ist,y_ist[i][1:], width=width, label=f'SB{i}') # label damit pyhton weiß was in Legende zu schreiben
#     ax.bar(x_pos_ist, df_percentage_array[i+1]-df_percentage_array[i], bottom=df_percentage_array[i], width=width, label=f'ST{i+1}')
#     #ax.bar(x_pos_ist, df2_percentage_array[i+1]-df2_percentage_array[i], bottom=df2_percentage_array[i], width=width, label=f'SB{i+1}')
#     plt.xticks(x_pos_label, x_label)
#     plt.legend()
#     plt.tight_layout()


# # ST_expected & ST_real
# ### taking into account the width of HB

# In[56]:


# 'soll Werte' kumulative Summe ueber die Reihen (in Richtung Column)
df_percentage_array = df_percentage_st.cumsum(axis=0).values
df2_percentage_array = df2_percentage_st2.cumsum(axis=0).values # selbiges für zweiten Datensatz - 'ist Werte'

fig, ax = plt.subplots(figsize=(15, 7)) # Größe definieren

ax.bar(x_pos_ist, df_percentage_array[0], width=width, label=f'ST{0}_soll')
ax.bar(x_pos_soll, df2_percentage_array[0], width=width, label=f'ST{0}_ist')

# erstellen der stacked bars
for i in range(15):
    ax.bar(x_pos_ist, df_percentage_array[i+1]-df_percentage_array[i],
           bottom=df_percentage_array[i], width=width, label=f'ST{i+1}_soll')
    ax.bar(x_pos_soll, df2_percentage_array[i+1]-df2_percentage_array[i],
           bottom=df2_percentage_array[i], width=width, label=f'ST{i+1}_ist')
    plt.xticks(x_pos_label, x_label, rotation=90)
    plt.tight_layout()
    plt.grid(True)
    
plt.ylabel('percentage')    
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, edgecolor='black')


# In[9]:


import matplotlib as mp
print(mp.__version__)


# In[ ]:




