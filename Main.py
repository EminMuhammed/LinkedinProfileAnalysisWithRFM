import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.max_rows', None)


def load_dataset():
    """
    load posts dataset

    Returns
    -------
    Dataframe
    """

    df_ = pd.read_excel("D:\VERİBİLİMİOKULU\VERİSETLERİ\post_bilgileri.xlsx")
    df = df_.copy()
    return df


def data_preprocessing(dataframe):
    """
    Edits are made in the date field.

    Parameters
    ----------
    dataframe: dataframe
    dataframe

    Returns
    -------
    Dataframe
    """

    dataframe = dataframe.loc[:, 0:]
    dataframe.columns = ["url", "date", "personurl", "name"]
    dataframe["date_new"] = [i.replace("Düzenlendi", "").replace("•", "").strip() for i in dataframe["date"]]
    dataframe["date_new"] = [str(int(i.replace("yıl", "").strip()) * 48) if "yıl" in i else i for i in
                             dataframe["date_new"]]
    dataframe["date_new"] = [str(int(i.replace("ay", "").strip()) * 4) if "ay" in i else i for i in
                             dataframe["date_new"]]
    dataframe["date_new"] = [i.replace("hafta", "").strip() if "hafta" in i else i for i in dataframe["date_new"]]

    return dataframe


def create_data_structure(dataframe):
    """
    data structure is created for rfm

    Parameters
    ----------
    dataframe: Dataframe
    dataframe

    Returns
    -------
    Dataframe
    """

    dataframe = dataframe.groupby("name").agg({"date_new": "min",
                                               "url": "count"})
    dataframe.columns = ['recency', 'frequency']
    dataframe["recency"] = dataframe["recency"].astype("int64")

    return dataframe


def create_rfm_score(dataframe):
    """
    rfm scores are generated

    Parameters
    ----------
    dataframe: Dataframe
    dataframe

    Returns
    -------
    Dataframe
    """

    dataframe["recency_score"] = pd.qcut(dataframe['recency'].rank(method="first"), 5, labels=[5, 4, 3, 2, 1])
    dataframe["frequency_score"] = pd.cut(dataframe['frequency'], bins=[0, 4, 8, 13, 17, 20], labels=[1, 2, 3, 4, 5])
    dataframe["RFM_SCORE"] = (dataframe['recency_score'].astype(str) +
                              dataframe['frequency_score'].astype(str))

    return dataframe


def create_segment(dataframe):
    """
    create segments

    Parameters
    ----------
    dataframe: Dataframe
    Dataframe

    Returns
    -------
    Dataframe
    """

    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    dataframe['segment'] = dataframe['RFM_SCORE'].replace(seg_map, regex=True)
    dataframe = dataframe.reset_index()
    return dataframe


df_ = load_dataset()
df_preprocessing = data_preprocessing(df_)
df_structure = create_data_structure(df_preprocessing)
df_rfmscore = create_rfm_score(df_structure)
df = create_segment(df_rfmscore)
