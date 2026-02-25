import streamlit as st
import processor , help
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Analyst", layout="wide")
st.sidebar.title("WhatsApp Analyst 📊")
with st.sidebar.expander('whatsapp_analyst' , expanded= True):
    upload_file =  st.file_uploader("Choose file")

if upload_file is None:

    st.info("Please enter your file")
    st.stop()

if upload_file is not None:

    st.header("Your chats deatil is here")
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = processor.processor(data)
   


    #fetching list of member

    user_name = df['user'].unique().tolist()
    user_name.remove('group_notification')
    user_name.sort()
    user_name.insert(0, "Overall")

    selected_name = st.sidebar.selectbox("Show Analysis W.r.t.", user_name)

    # analyst button

    tabs = st.tabs(["Overview", "Wordcloud", "Emojis", "Timeline", "Activity Map"])
    
    with tabs[0]:
        with st.container():
            if st.sidebar.button("Show Analysis"):
                
                num , word , media , link = help.fetch_stats(selected_name , df)

                col1 , col2 , col3 , col4= st.columns(4)

            
                st.metric("Total Messages" , num)
        
                st.metric("Total Word" , word)
                        
                st.metric("Total Media" , media)
                        
                st.metric("Total Links" , link)

                # most active member 

                if selected_name == 'Overall':
                    st.title('Most Active Member')
                    x , new_df = help.most_active_member(df)
                    fig , ax = plt.subplots()
                    col1 , col2 = st.columns(2)

                    with col1:
                        ax.bar(x.index , x.values)
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        with st.expander("View Full Table"):
                            st.dataframe(new_df)
    
    # Wordcloud
    with tabs[1]:
        with st.container():
            st.title("Word Clouds")
            df_wc = help.create_word_cloud(selected_name , df)
            fig , ax = plt.subplots(figsize = (4 , 3))
            ax.imshow(df_wc)
            plt.tight_layout()
            ax.axis("off")
            st.pyplot(fig)


    # Emoje analyst
    with tabs[2]:
        with st.container():
            emoji_df = help.emoji_helper(selected_name , df)
            st.title("Most Common Emoji")

            col1 , col2 = st.columns(2)

            with col1 :
                st.dataframe(emoji_df)

            with col2 :

                if emoji_df.empty:
                    st.error("No emojis found.")
                else:
                    fig , ax = plt.subplots(figsize =(4 , 3))
                    ax.pie(emoji_df['count'] , labels= emoji_df['emoji'] ,  autopct='%0.1f%%' , startangle=90)
                    plt.tight_layout()
                    st.pyplot(fig)

    # timeline on basic month

    with tabs[3]:
        with st.container():
            st.title("Monthly Activity")
            month_timeline = help.month_timeline(selected_name , df)

            timeline_option = st.radio("Select Timeline Type :" , 
                                    ["Monthly" , "Daily"] , horizontal= True)

            if timeline_option == "Monthly":

                fig , ax = plt.subplots(figsize =(4, 3))
                plt.plot(month_timeline['time'] , month_timeline['message'] ,  marker='o')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)


        # timeline on basic 

            elif timeline_option == "Daily":
            
            
                daily_timeline = help.date_timeline(selected_name ,df) 
                st.title("Daily Timeline")
                fig , ax = plt.subplots(figsize=(4, 3))
                plt.plot(daily_timeline['only_date'] , daily_timeline['message'] , color="#603ab8")
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)



    # Acitvity map
    with tabs[4]:
        with st.container():
            st.title("Activity map")

            Activity_option = st.radio("Select your Type" , ["Weekly Activity " , "Monthly Activity" , "Activity Heatmap"])

            if Activity_option == "Weekly Activity ":

                st.header("Weekly Activity")
                busy_date = help.weekly_activity(selected_name , df)
                fig , ax = plt.subplots(figsize =(4, 3))
                ax.bar(busy_date.index.astype(str) , busy_date.values , color="#1f7e6c")
                plt.xticks(rotation = 'vertical')
                plt.tight_layout()
                st.pyplot(fig)

            
            elif Activity_option == "Monthly Activity":
                st.header("Monthly Activity")
                busy_month = help.monthly_activity(selected_name , df)
                fig , ax = plt.subplots(figsize =(4 , 3))
                ax.bar(busy_month.index.astype(str) , busy_month.values , color = 'black')
                plt.xticks(rotation = 'vertical')
                plt.tight_layout()
                st.pyplot(fig)

                    # Activity heatmap

            elif Activity_option == "Activity Heatmap":

                user_heatmap = help.activity_heatmap(selected_name , df)
                fig, ax = plt.subplots(figsize=(4,3))
                sns.heatmap(user_heatmap, ax=ax , linewidths=0.5)
                plt.tight_layout()
                st.pyplot(fig)




