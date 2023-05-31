##Define a function F_mpt to return math placement level between 1 and 7
def F_mpt(mfund, aalg, tag):
    if np.isnan(mfund):
        return np.nan
    if mfund < 355:
        return 1
    elif mfund < 465 and aalg < 455:
        return 2
    elif mfund < 465:
        return 3
    elif aalg < 400:
        return 4
    elif aalg < 555:
        return 5
    elif aalg < 575:
        return 6
    elif aalg>575 and tag<555:
       return 6
    else:
        return 7

##varible order:
###### [gpa, mgpa, mact, mpt, sen]

## gpa is overall gradepoint average (capped at 4)
##mgpa is math gpa calculated during transcript review
##mact is math ACT
##mpt is math placement level as determined by mfund, aalg, tag
##sen is assessment of senior year math achievement. Ranges from 0 to 10. Determined during transcript review. SEE RUBRIC!!
 


##H_none: determines MATHH with no ACT, no MPT. Uses mgpa and sen from transcript review
def H_none(gpa, mgpa, sen):
    agpa = (gpa + mgpa) / 2

    if sen >= 8:
        if agpa >= 3.5:
            return 7
        elif agpa >= 3.25:
            return 6
        elif agpa >= 3:
            return 5
        elif agpa >= 2.5:
            return 4
        else:
            return 3
    elif sen >= 5 and sen < 8:
        if agpa >= 3.5:
            return 6
        elif agpa >= 3.25:
            return 5
        elif agpa >= 2.5:
            return 4
        else:
            return 3
    elif sen >= 3 and sen < 5:
        if agpa > 3.5:
            return 5
        elif agpa >= 3:
            return 4
        elif agpa >= 2.5:
            return 3
        else:
            return 2
    else:  # sen < 3
        if agpa > 3.5:
            return 4
        elif agpa >= 3:
            return 3
        elif agpa >= 2.5:
            return 2
        else:
            return 1

##H_mpt: determines MATHH with additional info of MPT only
def H_mpt(gpa, mgpa, mpt, sen):
    h0 = H_none(gpa, mgpa, sen)

    if mpt <= h0 - 2:
        return h0 
    elif mpt<=h0:
        return h0
    else:
        return min(h0 + 1, 7)

##H_mact: determines MATHH with additional info of MACT only
def H_mact(gpa, mgpa, mact, sen):
    h0 = H_none(gpa, mgpa, sen)

    if h0 >= 5:
        return h0
    else:
        if mact >= 23:
            return 5
        elif mact == 22:
            return 4
        elif mact == 21:
            return 3
        elif mact > 16:
            return 2
        else:
            return 1


##H_both: determines MATHH with additional info of  both MACT and MPT
def H_both(gpa,mgpa,mact,mpt, sen):
    value2 = H_none(gpa, mgpa, sen)
    value3 = H_mpt(gpa, mgpa, mpt, sen)
    value6 = H_mact(gpa, mgpa, mact, sen)

    return max(value2, value3, value6)

##This function takes a dataframe with specific column names and classifies cases by "Type". 
##Depending on Type, one of the four H functions will later be used to determine MATHH
def process_dataframe(df):
    df_typed = df.copy()
    df_typed['Type'] = 'x'
    ##cap GPA at 4.0
    df_typed['GPA'] = df_typed['GPA'].apply(lambda x: min(x, 4) if not pd.isna(x) else 'x')
    
    df_typed.loc[(df['MACT'].isna()) & (df['MGPA'].notna()) & (df['MPT'].isna()) & (df['SEN'].notna()),'Type'] = 'h_none'
    df_typed.loc[(df['MACT'].isna()) & (df['MPT'].notna())& (df['MGPA'].notna()) & (df['SEN'].notna()), 'Type'] = 'h_mpt'
    df_typed.loc[(df['MACT'].notna()) & (df['MPT'].notna()) &(df['MGPA'].isna()) & (df['SEN'].isna()), 'Type'] = 'expedited'
    df_typed.loc[(df['MACT'].notna()) & (df['MPT'].isna())& (df['MGPA'].notna()) & (df['SEN'].notna()), 'Type'] = 'h_mact'
    df_typed.loc[(df['MACT'].notna()) & (df['MPT'].notna())& (df['MGPA'].notna()) & (df['SEN'].notna()), 'Type'] = 'h_both'

    return df_typed    

def apply_model(row):
    if row['Type'] == 'h_none':
        return H_none(row['GPA'], row['MGPA'], row['SEN'])
    elif row['Type'] == 'h_mpt':
        return H_mpt(row['GPA'], row['MGPA'], row['MPT'], row['SEN'])
    elif row['Type'] == 'h_mact':
        return H_mact(row['GPA'], row['MGPA'], row['MACT'], row['SEN'])
    elif row['Type'] == 'h_both':
        return H_both(row['GPA'],row['MGPA'], row['MACT'], row['MPT'], row['SEN'])
    else:
        return None 

