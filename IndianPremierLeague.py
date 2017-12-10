
# coding: utf-8

# # * **Indian Premier League** *
# 
# #### Its a professional Twenty20 cricket league in India contested during April and May of every year by teams representing Indian cities. The league was founded by the Board of Control for Cricket in India (BCCI) in 2007
# 
# 
# #### The IPL is the most-attended cricket league in the world and ranks sixth among all sports leagues.[5] In 2010, the IPL became the first sporting event in the world to be broadcast live on YouTube. The brand value of IPL in 2017 was US \$ 5.3 billion, according to Duff & Phelps. According to BCCI, the 2015 IPL season contributed ₹11.5 billion (US\$182 million) to the GDP of the Indian economy
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from numpy import median
init_notebook_mode(connected=True)
get_ipython().magic('matplotlib inline')


# In[2]:


ipl_deliveries=pd.read_csv('C:/Lectures/DataVisualization/ipl/deliveries.csv')
ipl_matches=pd.read_csv('C:/Lectures/DataVisualization/ipl/matches.csv')


# ### Lets see all the teams playing im IPL Matches

# In[3]:


print(ipl_deliveries.batting_team.unique())


# ### Total number of Batsmen and Bowlers participating in the tournament

# In[4]:


print("Total number of batsmen are :", len(ipl_deliveries.batsman.unique()))
print("Total number of bowlewr are :", len(ipl_deliveries.bowler.unique()))


# ### Number of matches playes from 2008 to 2012

# In[5]:


print("Number of matches played are :",len(ipl_deliveries.match_id.unique()))


# ### Lets plot number of matches played in each stadium/Venue

# In[6]:


Matches_at_Venu=ipl_matches.groupby('venue').count()[['id']].reset_index()


# In[7]:


Matches_at_Venu.head(10)


# In[8]:


fig, ax = plt.subplots()
fig.set_size_inches(11, 8)
sns.pointplot(y='venue',x='id',data=Matches_at_Venu,figsize=(20,20),linestyles="--",markers='o',color='r')
ax.set_xlabel("number of matches played")
ax.set_ylabel("Stadium")


# ### Lets see the runs scored by each team in all the seasons since 2008. 
# 
# The wins can be understood in tow ways, lets say we have teams A and B playing.
# 
# if A team sets a score and stops team B from achiving by taking all the wickets, it its called *win by runs*  
# 
# if A team is chasing a score set by B team and it achives with say n wickets remainig, its called *win by wickets*

# In[9]:


ipm1=ipl_matches.groupby(by='winner').sum()[['win_by_runs','win_by_wickets']]


# In[10]:


ipm1.plot(kind='bar',figsize=(12,8),grid=True,title='Team Score in all seasons')


# ### Bowler Economy
# 
# A bowlers economy can be understood as the number of runs given away for each ball bowled.

# In[11]:


# number of players dissmissed by a bowler
ipd1=ipl_deliveries.groupby(by='bowler').count()[['player_dismissed']]
#total number of runs given away by the bowler
ipd2=ipl_deliveries.groupby(by='bowler').sum()[['total_runs']]
#number of matches played by each player
ipd3=pd.DataFrame(ipl_deliveries.groupby(by='bowler')[['match_id']].nunique())
bowler=pd.concat([ipd1,ipd2,ipd3],axis=1)


# In[12]:


bowler=bowler.sort_values('match_id',ascending=False).reset_index()


# In[13]:


bowler.head()


# In[14]:


from mpl_toolkits.mplot3d import Axes3D


# In[15]:


fig=plt.figure(figsize=(10,12))
ax=fig.add_subplot(111,projection='3d',facecolor='c')
#ax.plot(xs=bowler.player_dismissed,ys=bowler.total_runs)
ax.plot_wireframe(X=bowler.player_dismissed,Y=bowler.total_runs,Z=(bowler.total_runs/(bowler.match_id*6)),rcount=1000)
ax.set_xlabel('Players_dismissed in all IPL seasons')
ax.set_ylabel('Runs given away by bowlers')
ax.set_zlabel('Bowling average throughout the seasons')


# ### Matches wone in cities

# In[16]:


fig=plt.figure(figsize=(10,12))
plt.subplot(polar=True)
sns.countplot(x='city',data=ipl_matches,palette='gist_earth')


# In[17]:


fig=plt.figure(figsize=(10,12))
plt.subplot(polar=False)
sns.countplot(y='venue',hue='city',data=ipl_matches,palette='seismic',linewidth=5,edgecolor=sns.color_palette("summer",25))
#sns.factorplot(y='venue',hue='city',data=ipl_matches,palette='seismic',kind='count',size=8,aspect=1,linewidth=10)


# ### runs scored by each team in all the season

# In[18]:


total_win=ipl_matches.groupby(['season','winner']).count()[['id']].reset_index()


# In[19]:


(sns.jointplot(x='season',y='id',data=total_win,size=10,ratio=5,color='m').plot_joint(sns.kdeplot,zborder=0,n_level=6)).set_axis_labels("Season", "Matches won")


# In[20]:


sns.factorplot(data=total_win,x='season',y='id',col='winner',col_wrap=3,size=2,kind='bar',aspect=2,saturation=2,
margin_titles=True)


# ### Matches played vs Matches lost by teams since 2008 to 2012

# In[21]:


team_stats=pd.DataFrame({'TotalMatches': ipl_matches.team1.value_counts()+ipl_matches.team2.value_counts()
                         ,'TotalWin':ipl_matches.winner.value_counts()})

team_stats=team_stats.reset_index()

team_stats.rename(columns={'index':'Teams'},inplace=True)


# In[22]:


team_stats.head(10)


# In[23]:


trace_TMatch = Bar(x=team_stats.Teams,
                  y=team_stats.TotalMatches,
                  name='Total Matches Played',
                  marker=dict(color='#ffcdd2'))

trace_WMatch = Bar(x=team_stats.Teams,
                y=team_stats.TotalWin,
                name='Matches Won',
                marker=dict(color='#A2D5F2'))

data = [trace_TMatch, trace_WMatch]
layout = Layout(title="Win vs Los comparison for each team",
                xaxis=dict(title='Teams'),
                yaxis=dict(title='Number of Matches '))
fig = Figure(data=data, layout=layout)

iplot(fig,filename='C:/Lectures/DataVisualization/ipl/stackbar')


# ### Number of times teams have wone a season finale

# In[24]:


# The final match of the year is the one we need so we remove all the duplicates from the data 
# and only keep the last row of the subset
season_winner=ipl_matches.drop_duplicates(subset=['season'], keep='last')[['season','winner']].reset_index(drop=True)
season_winner


# In[25]:


fig=plt.figure(figsize=(8,5))
plt.subplot()
sns.countplot(y='winner',data=season_winner,palette='coolwarm')


# In[ ]:





# In[ ]:




