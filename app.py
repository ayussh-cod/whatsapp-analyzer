import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode("utf-8")
     df=preprocessor.preprocess(data)
     user_list=df['users'].unique().tolist()
     user_list.sort()
     user_list.insert(0,"Overall")
     selected_user=st.sidebar.selectbox("show analysis wrt", user_list)
     if st.sidebar.button("Show Analysis"):
          num_messages,words,media_c,nums_links= helper.fetch_stats(selected_user,df)
          st.title("Top Statistics")
          col1,col2,col3,col4=st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(num_messages)
          with col2:
               st.header("Total Words")
               st.title(words )
          with col3:
               st.header("Total Media")
               st.title(media_c)
          with col4:
               st.header("Links Shared")
               st.title(nums_links)
           #tiemline
          timeline=helper.monthly_timeline(selected_user,df)
          fig,axis=plt.subplots()

          axis.plot(timeline['time'], timeline['message'])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          st.title("Daily Timeline")
          daily_timeline = helper.daliy_Time_line(selected_user, df)
          fig, axis = plt.subplots()

          axis.plot(daily_timeline['only_date'], daily_timeline['message'])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          st.title("Activity_map")
          col1,col2=st.columns(2)
          with col1:
               st.header("Most Busy Day")
               busy_day=helper.week_Activity_map(selected_user,df)
               fig,axis=plt.subplots()
               axis.bar(busy_day.index,busy_day.values)
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
          with col2:
               st.header("Most Busy Month")
               busy_month = helper.month_activity_map(selected_user, df)
               fig, axis = plt.subplots()
               axis.bar(busy_month.index, busy_month.values)
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
          st.title("Weekly activity heatmap")
          user_heatmap=helper.activity_heatmap(selected_user,df)
          fig, axis = plt.subplots()
          axis=sns.heatmap(user_heatmap)
          st.pyplot(fig)













          if selected_user == 'Overall':
               x,new_df=helper.most_busy_users(df)
               fig,ax=plt.subplots()

               col1,col2=st.columns(2)
               with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(new_df)
          df_wc=helper.create_wordcloud(selected_user,df)
          fig,ax=plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)
          # emoji analysis
          emoji_df=helper.emoji_helper(selected_user,df)
          st.dataframe(emoji_df)




