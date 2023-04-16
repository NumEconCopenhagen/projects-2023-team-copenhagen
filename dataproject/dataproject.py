def plot_e(df, country): 
    I = df['country'] == country
    ax=df.loc[I,:].plot(x='year', y='rec_demean', style='-o', legend=False)
    ax=df.loc[I,:].plot(x='year', y='gdp_demean', style='-o', legend=False)
    
