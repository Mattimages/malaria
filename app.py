import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly as pt


"""
# Welcome to the export assay data-processing web-app
please begin by inputting the clariostar excel file!
"""
uploaded_file = st.file_uploader("Upload you data from the Clariostar;\n make sure the rows are labeled A-H and the rows 1-12(or fewer) ")
if uploaded_file is not None:
    
    dataframe = pd.read_excel(uploaded_file, index_col= 0)
    df = st.data_editor(dataframe)
    #st.write(dataframe)
names_list=[]
for i in range(int(st.number_input('Num:'))): 
    name = st.text_input(f"enter the name of sample {i+1}")
    names_list.append(name)
f"these are your values?{names_list}"

checkmark=st.checkbox('Yes!')
if checkmark:
    st.write("loading")
    sample_names=names_list
    ##creating the list/cleaning the data
    dict={}
    for index in df.index:
        for i in range(len(df.loc[index])):
            dict[index+str(i+1)]=df.loc[index].iloc[i]
        df2 = pd.DataFrame.from_dict(dict, orient='index', columns=['value'])
    df2["sample"]="blank"
    df2=df2.reset_index(drop=False)
    df2.loc[::4,"sample"]=sample_names[0]
    df2.loc[1::4,"sample"]=sample_names[1]
    df2.loc[2::4,"sample"]=sample_names[2]
    for i in range(len(df2)):
        df2.loc[i,"row"]=df2['index'][i][0]
        df2.loc[i,"number"]=df2['index'][i][1:]
    ##this is wring the buffer goes every eight and by row probably save in dict stage
    ##im gonna split index into a and the focking thing and then just hardcode it :)))))
    #df2['buffer']=4
    mask= (df2['row']=="A")  | (df2['row']=="E")
    df2.loc[mask,'buffer']=1
    mask= (df2['row']=="B")  | (df2['row']=="F")
    df2.loc[mask,'buffer']=2
    mask= (df2['row']=="C")  | (df2['row']=="G")
    df2.loc[mask,'buffer']=3
    mask= (df2['row']=="D")  | (df2['row']=="H")
    df2.loc[mask,'buffer']=4

    import plotly.graph_objects as go

    fig = go.Figure(data=go.Heatmap(
        x=df2['number'],
        y=df2['row'],
        z=df2['buffer'],
        xgap=2,  # gap between x-axis grid lines
        ygap=2,

        #colorbar=color_scale
        text=[f' {value}<br> {buffer}<br> {sample}' for value, buffer, sample in zip(df2['value'], df2['buffer'], df2['sample'])],
        hoverinfo='text'
    ))
    #print(text2)
    ###

    fig.update_traces(
        #hoverinfo=text,

        #text=df2['index'],  # Add text to be displayed on each square
        texttemplate='%{text}',   # Template to display the text
        textfont={"size":8}  # Font color for the text

    )
    fig.update_yaxes(autorange="reversed")
    st.write(" # Is everything labeled correctly?")
    st.write(fig)
    checkmark2=st.checkbox('Yes!!')
    if checkmark2:
        df_final=pd.DataFrame()
        for sample in set(df2["sample"].values):
            for buffer in set(df2["buffer"].values):

                mean=df2[(df2["sample"]==sample)&(df2["buffer"]==buffer)]["value"].mean()
                std=df2[(df2["sample"]==sample)&(df2["buffer"]==buffer)]['value'].std()
                new_row = pd.DataFrame({'sample':[sample],'buffer':[buffer], 'mean': [mean], 'std': [std]})

                df_final = pd.concat([df_final, new_row], ignore_index=True)

        
        for i, value in enumerate(df_final["buffer"]):

            mask=(df_final['buffer']==value) & (df_final['sample']=="blank")
            #print("mask",int(df_final.loc[mask,"mean"]))
            temp_mean=df_final.loc[i,"mean"]
            temp_blank=df_final.loc[mask,"mean"]
            temp_blank=float(temp_blank.iloc[0])
            df_final.loc[i, "normalized_value"]= temp_mean/temp_blank

        st.write(df_final)
    
