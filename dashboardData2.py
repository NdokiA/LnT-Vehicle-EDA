import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import seaborn as sns 
import pickle 
import streamlit as st 

plt.rcParams['font.family'] = 'DejaVu Sans Mono'

train_df = pd.read_csv('dataset/processed.csv')
#Load dictionaries
with open('dataset/CNS_label.pkl', 'rb') as f:
    CNS_label = pickle.load(f)
with open('dataset/emp_label.pkl', 'rb') as f:
    emp_label = pickle.load(f)


def age_hist():
    
    all_loans = train_df['age']
    default_loans = train_df[train_df['loan_default'] == 1]['age']
    bins = 40
    fig = plt.figure(figsize = (10,4.5))
    plt.hist([default_loans, all_loans], bins=bins,
                label=['Defaulted Loans', 'Total Loans'],
                color=['salmon', 'skyblue'],
                edgecolor='black', alpha=0.7,
                histtype = 'barstacked'
            )

    plt.xlabel('Age (Years)'.replace('_', ' ').capitalize())
    plt.ylabel('Number of Loans')
    plt.title(f'Distribution of Loans by Age')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    st.pyplot(fig)

def state_bar():
  
    fig = plt.figure(figsize = (10,4.5))
    loan_emp =   train_df.groupby('State_ID').agg(
        total_loans=('loan_default', 'count'),
        defaulted_loans = ('loan_default', 'sum'),
    ).sort_values(by = 'defaulted_loans', ascending = False).reset_index()
    
    sns.barplot(data=loan_emp, x=loan_emp.index, y='total_loans', color='steelblue', label = 'Number of Total Loans')
    sns.barplot(data=loan_emp, x=loan_emp.index, y='defaulted_loans', color='tomato',
                label = 'Number of Defaulted Loans')
    custom_text = Line2D([], [], linestyle='None', marker='', label='% -- Percentage of Loans Number')
    
    plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], custom_text])
    total_all = loan_emp['total_loans'].sum()
    for i in range(len(loan_emp)):
        total = loan_emp.loc[i, 'total_loans']
        ratio = total / total_all if total > 0 else 0
        
        text = f"{ratio:.1%}"

        fontsize = 9
        plt.text(i, total + max(loan_emp['total_loans']) * 0.01, text,
                ha='center', va='bottom', fontsize=fontsize, color='black')
        
        plt.title('Total Loans for Each State')
        plt.xticks(ticks = loan_emp.index, labels = loan_emp['State_ID'])
        plt.ylim([0, max(loan_emp['total_loans']) * 1.2])
        plt.xlabel('State ID')
        plt.ylabel('Number of Loans')
        
        plt.grid(axis = 'y', linestyle = '--')
    st.pyplot(fig)
    
def emp_bar():
  
    fig = plt.figure(figsize = (10,4.5))
    loan_emp =   train_df.groupby('Employment_Category').agg(
        total_loans=('loan_default', 'count'),
        defaulted_loans = ('loan_default', 'sum'),
    ).sort_values(by = 'defaulted_loans', ascending = False).reset_index()
    
    sns.barplot(data=loan_emp, x=loan_emp.index, y='total_loans', color='steelblue', label = 'Number of Total Loans')
    sns.barplot(data=loan_emp, x=loan_emp.index, y='defaulted_loans', color='tomato',
                label = 'Number of Defaulted Loans')
    custom_text = Line2D([], [], linestyle='None', marker='', label='% -- Percentage of Loans Number')
    
    plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], custom_text])
    total_all = loan_emp['total_loans'].sum()
    for i in range(len(loan_emp)):
        total = loan_emp.loc[i, 'total_loans']
        default_total = loan_emp.loc[i, 'defaulted_loans']
        ratio = total / total_all if total > 0 else 0
        ratio_default = default_total/total if total > 0 else 0
        
        text = f"{ratio:.1%}"

        fontsize = 9
        plt.text(i, total + max(loan_emp['total_loans']) * 0.01, text,
                ha='center', va='bottom', fontsize=fontsize, color='black')
        plt.text(i, default_total + max(loan_emp['total_loans']) * 0.01,
                f"Default Ratio: {ratio_default:.1%}",
                ha='center', va='bottom', fontsize=fontsize, color='black')
        
        plt.title('Total Loans for Each Employment Category')
        plt.xticks(ticks = loan_emp.index, labels = loan_emp['Employment_Category'].map(emp_label))
        plt.ylim([0, max(loan_emp['total_loans']) * 1.2])
        plt.ylabel('Number of Loans')
        plt.xlabel("")
        
        plt.grid(axis = 'y', linestyle = '--')
    st.pyplot(fig)
    
# Summary of loans by ID availability
id_loaner = train_df[['loan_default',
       'ID_Availability', 'Tax_ID_Availability', 'Driving_Card_Availability',
       'Passport_Availability']]

rows = []

for col in id_loaner.columns[1:]:
    grouped = id_loaner.groupby(col)['loan_default'].agg(
        Total_Loans='count',
        Defaulted_Loans='sum'
    ).reset_index()
    grouped['ID_Type'] = col
    grouped.rename(columns={col: 'Availability'}, inplace=True)
    rows.append(grouped)

id_summary = pd.concat(rows, ignore_index=True)
id_summary = id_summary[['ID_Type', 'Availability', 'Total_Loans', 'Defaulted_Loans']]

def id_bar():

    fig = plt.figure(figsize=(10, 4.5))

    sns.barplot(
        data=id_summary,
        x='ID_Type',
        y='Total_Loans',
        hue='Availability',
        palette='Blues',
        legend = False
    )

    sns.barplot(
        data=id_summary,
        x='ID_Type',
        y='Defaulted_Loans',
        hue='Availability',
        palette='Reds',
        alpha=0.6,
        dodge=True,
        legend = False
    )

    id_types = id_summary['ID_Type'].unique()
    bar_width = 0.2

    for i, id_type in enumerate(id_types):
        for j, availability in enumerate([0, 1]):

            y = id_summary[(id_summary['ID_Type'] == id_type) & (id_summary['Availability'] == availability)]['Total_Loans'].values
            y_def = id_summary[(id_summary['ID_Type'] == id_type) & (id_summary['Availability'] == availability)]['Defaulted_Loans'].values

            y_pos = y
            if y-y_def < 10000:
                y_pos = y+7000
            if len(y) > 0:
                x = i - bar_width if availability == 0 else i + bar_width
                label = 'Available' if availability == 1 else 'Not Available'
                plt.text(
                    x, y_pos[0] + max(id_summary['Total_Loans']) * 0.01,
                    label,
                    ha='center', va='bottom', fontsize=9, color='black'
                )
                plt.text(
                    x,y_def[0] + max(id_summary['Total_Loans']) * 0.01,
                    f"{y[0] / id_summary['Total_Loans'].sum():.1%}",
                    ha='center', va='bottom', fontsize=9, color='black'
                )


    plt.title('Total and Defaulted Loans by ID Availability')
    plt.xlabel('ID Type')
    plt.ylabel('Number of Loans')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.grid(axis='y')
    st.pyplot(fig)

id_loaner['ID_Count'] = id_loaner[['ID_Availability', 'Tax_ID_Availability',
                                   'Driving_Card_Availability', 'Passport_Availability']].sum(axis=1)

id_count_summary = id_loaner.groupby('ID_Count')['loan_default'].agg(
    Total_Loans='count',
    Defaulted_Loans='sum'
).reset_index()

def id_count_bar():
    fig = plt.figure(figsize=(10, 4.5))

    sns.barplot(x=id_count_summary['ID_Count'], y=id_count_summary['Total_Loans'], color='steelblue', label = 'Number of Total Loans')
    sns.barplot(x=id_count_summary['ID_Count'], y=id_count_summary['Defaulted_Loans'], color='tomato', label = 'Number of Defaulted Loans')

    # Annotate default rate on top of total loans
    for i in range(len(id_count_summary)):
        total = id_count_summary.loc[i, 'Total_Loans']
        defaulted = id_count_summary.loc[i, 'Defaulted_Loans']
        all = id_count_summary['Total_Loans'].sum()
        
        ypos = total 
        if total - defaulted < 2000:
            ypos = total + 7000
        default_ratio = defaulted/total if total > 0 else 0 
        ratio = total/ all
        plt.text(i, defaulted + max(id_count_summary['Total_Loans']) * 0.01,
                f"Default Ratio: {default_ratio:.1%}", ha='center', va='bottom', fontsize=9, color='black')
        plt.text(i, ypos + max(id_count_summary['Total_Loans']) * 0.01,
                f"{ratio:.1%}", ha='center', va='bottom', fontsize=9, color='black')

    # Formatting
    plt.title('Number of Loans vs. Number of IDs Provided')
    plt.xlabel('Number of IDs Provided')
    plt.ylabel('Number of Loans')
    plt.legend()
    plt.grid(axis='x')
    plt.tight_layout()
    st.pyplot(fig)

def categorize_credit_score(n):
    match n:
        case n if n <= 3:
            return "Very-Low\nRisk"
        case n if 3 < n <= 6:
            return "Low Risk"  
        case n if 6 < n <= 8:
            return "Medium Risk"
        case n if 8 < n <= 10:
            return "High Risk"
        case n if 10< n <= 12:
            return "Very-High\nRisk"
        case 13:
            return "No Bureau\nHistory"
        case _:
            return "Unscored"
        
def creditscore_bar():
  
    fig = plt.figure(figsize = (10,4))
    train_df['CREDIT_SCORE_CATEGORY'] = train_df['CREDIT_SCORE_CATEGORY'].apply(categorize_credit_score)
    loan_cre =   train_df.groupby('CREDIT_SCORE_CATEGORY').agg(
        total_loans=('loan_default', 'count'),
        defaulted_loans = ('loan_default', 'sum'),
    ).sort_values(by = 'defaulted_loans', ascending = False).reset_index()
    
    sns.barplot(data=loan_cre, x=loan_cre.index, y='total_loans', color='steelblue', label = 'Number of Total Loans')
    sns.barplot(data=loan_cre, x=loan_cre.index, y='defaulted_loans', color='tomato',
                label = 'Number of Defaulted Loans')
    custom_text = Line2D([], [], linestyle='None', marker='', label='% -- Percentage of Loans Number')
    
    plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], custom_text])
    total_all = loan_cre['total_loans'].sum()
    for i in range(len(loan_cre)):
        total = loan_cre.loc[i, 'total_loans']
        default_total = loan_cre.loc[i, 'defaulted_loans']
        ratio = total / total_all if total > 0 else 0
        ratio_default = default_total/total if total > 0 else 0
        
        text = f"{ratio:.1%}"

        fontsize = 9
        plt.text(i, total + max(loan_cre['total_loans']) * 0.01, text,
                ha='center', va='bottom', fontsize=fontsize, color='black')
        
        plt.title('Total Loans for Each Credit Score Category')
        plt.xticks(ticks = loan_cre.index, labels = loan_cre['CREDIT_SCORE_CATEGORY'], rotation=45)
        plt.ylim([0, max(loan_cre['total_loans']) * 1.2])
        plt.ylabel('Number of Loans')
        plt.xlabel("")
        plt.grid(axis = 'y', linestyle = '--')
    st.pyplot(fig)

def categorize_borrower(n):
    if n < 1:
        return 'First-time Borrower'
    elif 1 <= n <= 5:
        return 'Established Borrower'
    else:
        return 'Seasoned Borrower'
    
def accountsnum_bar():
    # Ensure categorization is applied
    train_df['borrower_type'] = train_df['PRI_NO_OF_ACCTS'].apply(categorize_borrower)

    # Maintain consistent order for bar chart and legend
    category_order = ['First-time Borrower', 'Established Borrower', 'Seasoned Borrower']
    borrower_counts = train_df['borrower_type'].value_counts().reindex(category_order)
    borrower_defaults = train_df[train_df['loan_default'] == 1]['borrower_type'].value_counts().reindex(category_order)

    fig, ax = plt.subplots(figsize=(10, 5))

    bar_width = 0.4
    y = range(len(category_order))

    # Plot total loans
    ax.barh(
        [i + bar_width/2 for i in y], 
        borrower_counts, 
        height=bar_width, 
        color='#66b3ff', 
        label='Total Loans'
    )
    # Plot defaulted loans
    ax.barh(
        [i - bar_width/2 for i in y], 
        borrower_defaults, 
        height=bar_width, 
        color='#ff9999', 
        label='Defaulted Loans'
    )

    ax.set_yticks(y)
    ax.set_yticklabels(category_order, fontsize=12)
    ax.set_xlabel('Number of Loans', fontsize=13)
    ax.set_title('Loans by Borrower Type', fontsize=15)
    legend_elements = [
        Patch(facecolor='#66b3ff', label='Total Loans'),
        Patch(facecolor='#ff9999', label='Defaulted Loans'),
        Patch(facecolor='none', edgecolor='none', label='First-time Borrower: 0 accounts'),
        Patch(facecolor='none', edgecolor='none', label='Established Borrower: 1–5 accounts'),
        Patch(facecolor='none', edgecolor='none', label='Seasoned Borrower: >5 accounts'),
    ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10, frameon=True)
    
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)

def overdue_hist():
    # Filter data for loans with PRI_NO_OF_ACCTS > 0 and PRI_OVERDUE_ACCTS < 5
    filtered_df_below_5 = train_df[(train_df['PRI_NO_OF_ACCTS'] >5) & (train_df['PRI_OVERDUE_ACCTS'] < 5)].copy()

    # Separate defaulted and non-defaulted loans in the filtered data
    all_overdue_below_5 = filtered_df_below_5['PRI_OVERDUE_ACCTS']
    default_overdue_below_5 = filtered_df_below_5[filtered_df_below_5['loan_default'] == 1]['PRI_OVERDUE_ACCTS']

    # Plotting the histogram for < 5 overdue accounts
    fig =plt.figure(figsize=(10, 5))
    plt.hist([default_overdue_below_5, all_overdue_below_5],
                bins=range(0, 6), # Bins from 0 to 5 (exclusive of 5)
                label=['Defaulted Loans', 'All Loans'],
                color=['salmon', 'skyblue'],
                edgecolor='black', alpha=0.7,
                histtype='barstacked')

    plt.title('Distribution of Overdue Accounts (Less than 5) on Experienced Loaners')
    plt.xlabel('Number of PRI Overdue Accounts')
    plt.ylabel('Number of Loans')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)