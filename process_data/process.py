import pandas as pd


def process_titanic_data(data):
    # Ensure data is a list of dictionaries with 'Age', 'Name', 'Sex', and 'Pclass' fields
    
    titanic = data.get('titanic_data')
    df = pd.DataFrame(titanic)
   
    #if not isinstance(df, pd.DataFrame):
       # return {"error": "Invalid data format. Expected a list of dictionaries."}
       
    # Filter out entries with missing Age and perform calculations
    max_age_person = df.loc[df['Age'].idxmax(), 'Name']
    min_age_person = df.loc[df['Age'].idxmin(), 'Name']
    count_age_above_40 = df[(df['Age'] > 40)].shape[0]
    count_females_above_40 = df[((df['Age'] > 40) & (df['Sex'] == 'female'))].shape[0]
    pclass_gender_count = df.groupby(['Pclass', 'Sex']).size().unstack(fill_value=0).to_dict()
    fare_sum_per_class = df.groupby('Pclass')['Fare'].sum().to_dict()
    
      # Convert int64 values to native Python types
    #fare_sum_per_class = {k: int(v) for k, v in fare_sum_per_class.items()}
    #pclass_gender_count = {k: {kk: int(vv) for kk, vv in v.items()} for k, v in pclass_gender_count.items()}
    
    
    # Prepare response data
    response = {
        "max_age_name": max_age_person if max_age_person else None,
        "min_age_name": min_age_person if min_age_person else None,
        "count_age_above_40": count_age_above_40,
        "count_females_above_40": count_females_above_40,
        "pclass_gender_count": pclass_gender_count,
        'fare_sum_per_class': fare_sum_per_class,
    }
   
    return response
#result = process_titanic_data(df)

#print(result)
