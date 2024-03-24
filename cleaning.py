#!/usr/bin/env python
# coding: utf-8

# # Cleaning & Preprocessing

# ## Imports

# In[1]:


# Import dependencies
import pandas as pd
import uuid
from sqlalchemy import create_engine


# ## Cleaning

# In[2]:


# Read CSV
filepath = 'resources/mxmh_survey_results.csv'
df = pd.read_csv(filepath)
df.info()


# In[3]:


# Function to reformat columns lowercase w/o spaces/braces
def col_mapper(old):
    lower = old.lower()
    underscore = lower.replace(' ', '_')
    new = underscore.replace('[', '').replace(']', '') # 1 level of abstraction
    return new


# In[4]:


df.rename(columns=col_mapper, inplace=True)
print(df.columns)


# In[5]:


# Add unique id column
df['uuid'] = [uuid.uuid4() for _ in range(len(df))]

# move it to first
first_col = df.pop('uuid')
df.insert(0, 'uuid', first_col)

df.head(2)


# In[6]:


# Replace improve with 1
df = df.replace({
    'Improve': 1,
    'No effect': 0,
    'Worsen': 0 # too few responses
})
df['music_effects'][0:5]


# In[7]:


# Remove unhelpful and potentially PII columns
cols_to_drop = [
    'bpm', # too few responses and too nonsensical answers
    'permissions', # everyone answered yes
    'timestamp' # potentially PII
    ]

cleaned_df = df.drop(columns=cols_to_drop)


# In[8]:


# Drop remaining rows containing any number of NaN
cleaned_df = cleaned_df.dropna()
print(f'{len(df)-len(cleaned_df)} rows dropped ({len(cleaned_df)} remaining)')


# ## Export to SQL

# In[9]:


cleaned_df['uuid'] = cleaned_df['uuid'].astype(str)
cleaned_df.info()


# In[10]:


# Initialize SQLAlchemy engine
engine = create_engine('sqlite:///resources/cleaned.db')


# In[11]:


cleaned_df.to_sql('main', con=engine, if_exists='replace', index=False)

