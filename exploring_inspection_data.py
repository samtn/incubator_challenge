# coding: utf-8

# In[1]:

import graphlab


# In[2]:

data = graphlab.SFrame.read_csv_with_errors('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')


# In[3]:

data = data[0]

# In[167]:

data_per_case = data.groupby(key_columns=['CAMIS', 'PHONE' ], 
             operations= {'Count':graphlab.aggregate.COUNT('CAMIS'), 
                          'average_score': graphlab.aggregate.MEAN('SCORE'),
                          'min_score': graphlab.aggregate.MIN('SCORE'),
                          'max_score': graphlab.aggregate.MAX('SCORE'),
                          'std_score': graphlab.aggregate.STD('SCORE'),
                          'flag_freq': graphlab.aggregate.FREQ_COUNT('CRITICAL FLAG'),
                          'code_freq': graphlab.aggregate.FREQ_COUNT('VIOLATION CODE')})


# In[28]:

critical_descs = data[data['CRITICAL FLAG'] == 'Critical']


# In[37]:

critical_descs.groupby(key_columns='CAMIS', 
             operations= {'Count':graphlab.aggregate.COUNT('CAMIS')}).num_rows()


# In[65]:

critical_data = critical_descs.groupby(key_columns='VIOLATION CODE', 
                       operations= {'Count':graphlab.aggregate.COUNT('VIOLATION CODE'),
                                    'descs':graphlab.aggregate.FREQ_COUNT('VIOLATION DESCRIPTION')})


# In[66]:

def remove_punctuation(text):
    import string
    return text.translate(None, string.punctuation) 

no_punc = data['VIOLATION DESCRIPTION'].apply(remove_punctuation)


# In[71]:

critical_data['Freq'] = critical_data['Count'] / 240621.
critical_data.sort('Count', ascending=False).print_rows(num_rows=50)


# In[75]:

critical_data[critical_data['VIOLATION CODE']=='05E']['descs']


# In[209]:

import matplotlib
get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud


# In[115]:

text = ''
for row in critical_data.sort('Count', ascending=False).head():
    words = row['descs'].keys()[0]
    for i in range(int(row['Freq']*100)):
        text += words

# In[134]:

wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('wordcloud.png', dpi=300)


# In[132]:

wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[168]:

N_total  = data_per_case.num_rows()
def has_critical(dic):
    if 'Critical' in dic and dic['Critical'] > 0:
        return 1
    else:
        return 0
data_per_case['has_critical'] = data_per_case['flag_freq'].apply(has_critical)

data_per_case['has_critical'].sum() / float(N_total)

# In[182]:

import re
def make_key(text):
    return '1'+re.sub("[^0-9]", "", str(text))
data_per_case['phone_key'] = data_per_case['PHONE'].apply(make_key)


# In[179]:

yelp_data = graphlab.load_sframe('nyc_food_yelp.tsv')


# In[198]:

def get_review(phone):
    arr = yelp_data[yelp_data['Phone'] == int(phone)]['Review']
    if len(arr) > 0:
        return arr[0]
    else:
        return -1
data_per_case['yelp review'] = data_per_case['phone_key'].apply(get_review)


# In[295]:

from operator import is_not
from functools import partial

matplotlib.rcParams['lines.linewidth'] = 3.0
rev_vals = data_per_case[data_per_case['yelp review'] >= 0]['yelp review'].unique()
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)


data_to_plot =[]
labels=[]
for i in rev_vals.sort():
    a = data_per_case[data_per_case['yelp review'] == i]['max_score']
    a = filter(partial(is_not,None) ,a)
    data_to_plot.append(a)
    labels.append(str(i))


ax.axhspan(0, 13,facecolor='green',linewidth=0.0, alpha=0.3)
ax.axhspan(13, 27,facecolor='yellow',linewidth=0.0, alpha=0.3)
ax.axhspan(27, 159,facecolor='red',linewidth=0.0, alpha=0.2)
#ax.axhline(y=13, xmin=0, xmax=6, c='green',linewidth=1.0, alpha=0.6)

ax.boxplot(data_to_plot)

ax.set_xticklabels(labels)
ax.set_xlabel('Yelp Review', fontsize=20)
ax.set_ylabel('Maximum Inspection Score', fontsize=20)
ax.set_ylim([0,100])

fig.savefig('yelp_review_vs_inspection_score.png', dpi=600)


# In[254]:

data_per_case[data_per_case['max_score'] >  20].num_rows()


# In[294]:

from operator import is_not
from functools import partial

matplotlib.rcParams['lines.linewidth'] = 3.0
rev_vals = data_per_case[data_per_case['yelp review'] >= 0]['yelp review'].unique()
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)


data_to_plot =[]
labels=[]
for i in rev_vals.sort():
    a = data_per_case[data_per_case['yelp review'] == i]['min_score']
    a = filter(partial(is_not,None) ,a)
    data_to_plot.append(a)
    labels.append(str(i))


ax.axhspan(0, 13,facecolor='green',linewidth=0.0, alpha=0.3)
ax.axhspan(13, 27,facecolor='yellow',linewidth=0.0, alpha=0.3)
ax.axhspan(27, 159,facecolor='red',linewidth=0.0, alpha=0.2)
#ax.axhline(y=13, xmin=0, xmax=6, c='green',linewidth=1.0, alpha=0.6)

ax.boxplot(data_to_plot)

ax.set_xticklabels(labels)
ax.set_xlabel('Yelp Review', fontsize=20)
ax.set_ylabel('Maximum Inspection Score', fontsize=20)
ax.set_ylim([0,60])

fig.savefig('yelp_review_vs_inspection_score_min.png', dpi=600)

