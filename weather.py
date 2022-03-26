import pandas as pd
import streamlit as st
import numpy as np
from plotly import express as px
st.header('Data Analyzer')
st.caption('~made by aniket das')
file = st.sidebar.file_uploader('upload your csv file here')
if file:
    try:
        x = pd.read_csv(file)
    except ValueError:
        st.error('error in file format')
    base_column = st.sidebar.selectbox(label='select the base column',options=x.columns)
    analysis_column = st.sidebar.selectbox(label='select the analysis column',options=x.columns,)
    if base_column != analysis_column:
        st.subheader('percent wise analysis')
        analysis = x.groupby(base_column)[analysis_column].value_counts(normalize=True).to_frame()
        dis = analysis.copy()
        analysis = analysis.unstack().reset_index()
        analysis = analysis.set_index(base_column)
        analysis = analysis*100
        col = analysis.columns
        analysis.replace(np.nan,0,inplace=True)
        analysis[col] = analysis[col].applymap('{:,.2f}%'.format)
        st.table(analysis)
        data = analysis.to_csv().encode('utf-8')
    
        st.download_button('download',data,'file.csv','text/csv',key='download-csv')
        st.subheader('count wise analysis')
        count = x.groupby(base_column)[analysis_column].value_counts().to_frame()
        count = count.unstack().reset_index()
        count = count.set_index(base_column)
        count_col = count.columns
        count.replace(np.nan,0,inplace=True)
        observed = count.copy()
        count['total'] = count.sum(axis=1)
        count.loc['Total'] = count.sum()
        st.table(count)
        c_data = count.to_csv().encode('utf-8')
        st.download_button('download',c_data,'file.csv','text/csv',key='download-count-csv')
    graph = st.sidebar.radio('show graph',['no','yes'])
    if (base_column != analysis_column) and graph == 'yes':
        dis.rename(columns={analysis_column:'percent'},inplace=True)
        dis = dis.reset_index()
        dis['percent'] = dis['percent']*100
        fig = px.bar(y=dis['percent'],x=dis[base_column],title=analysis_column,color=dis[analysis_column],template='simple_white',labels={'y':'percent','x':base_column},text=dis['percent'].apply(lambda x: "{0:1.2f}%".format(x)))
       
        st.plotly_chart(fig)
    st.sidebar.header('Chi-Square Test')
    do = st.sidebar.radio('do a chi-square test ?',options=['no','yes'])
        
    if do == 'yes':
        g_total = count[count.columns[-1]].iloc[-1]
        n_col = len(count.columns)-1
        n_row = len(count.index)-1
        st.header('Chi-Square Test')
        st.subheader('observed values(O)')
        st.table(count)
        st.subheader('expected values(E)')
        exp = np.outer(count[count.columns[-1]][0:n_row],count.iloc[-1][0:n_col])
        exp = pd.DataFrame(exp)
        exp.columns = observed.columns
        exp.index = observed.index
        exp = exp.div(g_total)
        exp['total'] = exp.sum(axis=1)
        exp.loc['Total'] = exp.sum()
        st.table(exp)
        st.subheader('calculation of chi-square value')
        st.write("forumula = ((O-E)^2)/E")
        diff = ((count-exp)**2)/exp
        arr = diff.to_numpy()
        st.table(diff)
        chi_value = round(np.sum(arr),2)
        st.info('Chi square value is '+str(chi_value))
        st.subheader('degree of freedom')
        deg = (len(analysis.columns)-1)*(len(analysis.index)-1)
        st.info('degree of freedom is'+ str(deg))
        tb = pd.read_csv('table.csv',index_col=0)
        st.subheader('significance factor')
        p = st.selectbox('choose the significance factor(if no idea put 0.05)',options=tb.columns)
        st.subheader('critical value')
        cv = tb[str(p)].iloc[deg-1]
        st.write(cv)
        st.info('critcal value is '+ str(cv))
        if chi_value > float(cv):
            st.write(f"since chi_value({chi_value}) is greater than critical value({cv})")
            st.warning('your H1 hypotheisis is proven')
            st.write('there is a **significant** relation ship between'+base_column+"and"+analysis_column)
        if chi_value < float(cv):
            st.write(f"since chi_value({chi_value}) is less than critical value({cv})")
            st.warning('your H0 hypotheisis is proven')
            st.write('there is **no significant** relation ship between '+ base_column +" and "+analysis_column)
