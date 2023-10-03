# importing module phonenumbers
import numpy as np # linear algebra
import pandas as pd # data processing
pd.options.mode.chained_assignment = None  # default='warn'


## load excel file 
df = pd.read_csv("grid_csv.csv", encoding='utf-8-sig')
print (df.shape)
df.head()


#specify columns that has values
main=['الاسم','رقم الحساب']
deduction=['حماية اجتماعية','تسوية','الانقطاع','تنفيذ','تأمين','سلف','الضريبة', 'نسبة التقاعد% من الراتب الاسمي']
allowance=['مخصصات النقل','نسبة المهنية','سيطرة نوعية','فنيين','هندسية'
           ,'منصب%من الراتب الاسمي', 'الشهادة نسبة% من الراتب الاسمي','الزوجية','مخصصات_استثنائية'
           ,'مخصصات امانة صندوق% من الراتب الاسمي','مخصصات امين المخزن% من الراتب الاسمي'
           ,'مخصصات فنية% من الراتب الاسمي','مخصصات اشعاع% من الراتب الاسمي','مخصصات مهنية'
           ,'الأطفال','مخصصات حاسبة% من الراتب الاسمي','فرق العلاوة', 'منصب','الخطورة','القانونية']


# all column names except the main
columns=list(set(df.columns) - set(main))

# calculate number of returned rows
columns_num=len(columns)*len(df[columns[0]])
#print(columns_num)


# create new empty file
new_df = pd.DataFrame(list())
new_df = pd.DataFrame(index=np.arange(columns_num+1), 
                      columns=['Nametext','Acc','Type','Type ID','Type code',
                               'Description','Percentage','Value'])
#new_df.to_csv('new_grid_data.csv')


l=0;
#loop through the value columns
for var in columns:
    #get type
    type='استقطاع'
    type_id=2
    type_code='002'
    if var in allowance: 
        type='استحقاق'
        type_id=1
        type_code='001'
    
    #fill the empty file with new values
    for i in range(0,len(df[var])):
        curr_val=float(df[var][i])
        val_len=len(str(curr_val))
        name=df['الاسم'][i]

        
        new_df['Nametext'][l]=name
        new_df['Acc'][l]=df['رقم الحساب'][i]
        new_df['Type'][l]=type
        new_df['Type ID'][l]=type_id
        new_df['Type code'][l]=type_code
        new_df['Description'][l]=var

    
        # check if it is percentage or not
        if(curr_val<100):
            new_df['Percentage'][l]="{0:.1f}".format(curr_val)
            new_df['Value'][l]=0
        else:
            new_df['Value'][l]="{0:.1f}".format(curr_val)
            new_df['Percentage'][l]=0
        l+=1    

 

# delete all rows where value=0 and percentage=0
indexValue = new_df[ (new_df['Value'].astype(float) < 1) & (new_df['Percentage'].astype(float) < 1) ].index
new_df.drop(indexValue , inplace=True)
new_df.head(15)

               
new_df.to_excel("new_grid_filled.xlsx")
#new_df.to_csv('grid_for_import.csv')
        