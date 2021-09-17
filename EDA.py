from LinkedinProfileAnalysisWithRFM import Main

df_ = Main.load_dataset()
df_preprocessing = Main.data_preprocessing(df_)
df_structure = Main.create_data_structure(df_preprocessing)
df_rfmscore = Main.create_rfm_score(df_structure)
df_segment = Main.create_segment(df_rfmscore)


def check_df_first(dataframe, head=5, tail=5):
    print(f"Head = {dataframe.head(head)}")
    print("###########################")
    print(f"Tail = {dataframe.tail(tail)}")
    print("###########################")
    print(f"Shape : {dataframe.shape}")
    print("###########################")
    print(f"Columns = {dataframe.columns}")
    print("###########################")
    print(f"Unique Name = {dataframe.name.nunique()}")
    print("###########################")
    print(f"info = {dataframe.info()}")


check_df_first(df_preprocessing)

df_preprocessing.head()

# Q1- What is the date that people last liked (recency) and the number of posts they liked (frequency)?
df_preprocessing.groupby("name").agg({"date_new": lambda x: x.min(),
                                      "url": lambda x: x.nunique()}).head()

# Q2- Who are the people who like the posts the least and the most?
df_preprocessing.groupby("name").agg({"url": "count"}).sort_values("url", ascending=False).head(10)
df_preprocessing.groupby("name").agg({"url": "count"}).sort_values("url", ascending=False).tail(10)

# Q3- Is there any missing value?
df_preprocessing.isnull().sum()


# Q4- check df structure
def check_structure_df(dataframe):
    print(f"frequency unique number = {dataframe['frequency'].unique()}")
    print(f"frequency max = {dataframe['frequency'].max()}")
    print(f"frequency describe = {dataframe['frequency'].describe().T}")
    print(f"info = {dataframe.info()}")


check_structure_df(df_structure)

# Q5- People with an rfm score of 1 and 5
df_rfmscore[df_rfmscore["recency"] == 1].head()
df_rfmscore[df_rfmscore["recency"] == 48].head()

# Q6- Recency value counts
df_rfmscore["recency"].value_counts()

# Q7- Top 10 likes
df_rfmscore.sort_values("frequency", ascending=False).head(10)

# Q8- segment champions
df_segment.loc[df_segment["segment"] == "champions", ["name"]]

# Q9- All links a person likes
df_preprocessing.loc[df_preprocessing["name"] == "Emrehan İnci", ["url"]]

# Q10- MERGE / What is a person's last favorite post with a frequency greater than 1?
df_merge = df_segment.merge(df_preprocessing, on="name", how="left")
df_merge = df_merge.drop(["personurl", "date"], axis=1)

df_merge.loc[df_merge["frequency"] > 1, ["name", "url", "date_new"]].groupby("name").agg(
    {"date_new": "min",
     "url": lambda x: x[:1]}).head()
