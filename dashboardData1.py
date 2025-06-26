import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
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

train_df['DisbursalDate'] = pd.to_datetime(train_df['DisbursalDate'], errors='coerce')
# Table Introduction
table_data = {
    "Loan Details": ['Customer ID', 'Amount Disbursed', 'Asset Cost',
                     'Loan to Value Ratio', 'Disbursal Date', 'Manufacturer ID', 
                     'State ID', 'Branch ID'],
    "Customer Identification": ['Phone Number Availability', 'ID Availability',
                                'Tax ID Availability', 'Driving Card Availability',
                                'Passport Availability', 'Employment Category', 
                                'Age', 'Credit Score Category'],
    "Repayment History": ['Number of Opened Accounts', 'Number of Active Loans', 'Number of Inquiries', 'Credit History Length', 
                          'Number of Delayed Payments', 'Number of Delinquents Acts (Last 6 Months)',
                          'Average Account Age']
}
max_len = max(len(col) for col in table_data.values())
for key in table_data:
    table_data[key] += ['']* (max_len-len(table_data[key]))
info = pd.DataFrame(table_data)
info.reset_index(drop = True, inplace = True)


def monthly_line_plot():

  train_df['DisbursalMonth'] = train_df['DisbursalDate'].dt.to_period('M')
  monthly_loan_counts = train_df.groupby('DisbursalMonth').size()
  monthly_defaulted_counts = train_df[train_df['loan_default'] == 1].groupby('DisbursalMonth').size()
  monthly_loan_counts.index = monthly_loan_counts.index.to_timestamp()
  monthly_defaulted_counts.index = monthly_defaulted_counts.index.to_timestamp()

  fig, ax = plt.subplots(figsize=(10, 5))
  ax.plot(monthly_loan_counts.index, monthly_loan_counts.values, label='All Loans (Monthly)', color='darkblue', lw=2.5)
  ax.plot(monthly_defaulted_counts.index, monthly_defaulted_counts.values, label='Defaulted Loans (Monthly)', color='maroon', lw=2.5)

  ax.set_xlabel('Disbursal Month')
  ax.set_ylabel('Number of Loans')
  ax.set_title('Monthly Loan and Defaulted Loan Counts')
  ax.legend()
  ax.grid(True)
  fig.tight_layout()
  
  st.pyplot(fig)

def loan_number_pie():
    
  labels = ['Defaulted\nLoan', 'Settled\nLoan']
  explode = [0.15, 0]

  loan_counts = [train_df['loan_default'].value_counts()[1], train_df['loan_default'].value_counts()[0]]

  # Define colors
  colors1 = ['#c22734', '#1679bf']
  # Create subplots
  fig = plt.figure(figsize=(5, 5))

  # Pie chart 1: Loan Counts
  plt.pie(
      loan_counts,
      labels=labels,
      colors=colors1,
      explode=explode,
      autopct='%.0f%%',
      shadow=True,
      startangle=0,
      labeldistance=1.1,
      textprops={'fontsize': 10}
  )
  plt.title('\nDistribution of Loans by \nRepayment Status', fontsize=13)
  plt.axis('equal')
  plt.tight_layout()
  st.pyplot(fig)

def loan_amount_pie():
  # Prepare data
  labels = ['Defaulted\nLoan', 'Settled\nLoan']
  explode = [0.15, 0]

  loan_amounts = train_df['disbursed_amount'].groupby(train_df['loan_default']).sum()[::-1]

  # Define colors
  colors2 = ['#c22734', '#1679bf']
  # Create subplots
  fig = plt.figure(figsize=(5, 6))

  plt.pie(
      loan_amounts,
      labels=labels,
      colors=colors2,
      explode=explode,
      autopct='%.0f%%',
      shadow=True,
      startangle=0,
      labeldistance=1.1,
      textprops={'fontsize': 10}
  )
  plt.title('\nDistribution of Disbursed Amounts\nby Repayment Status', fontsize=13)
  plt.axis('equal')

  plt.tight_layout()
  st.pyplot(fig)
    
def disburse_bar15():
  
  max_disbursed_amount = train_df['disbursed_amount'].max()

  range_1_max = max_disbursed_amount * 0.15

  all_loans_range1 = train_df[train_df['disbursed_amount'] <= range_1_max]['disbursed_amount']
  default_loans_range1 = train_df[(train_df['loan_default'] == 1) & (train_df['disbursed_amount'] <= range_1_max)]['disbursed_amount']

  fig, axes = plt.subplots(1, figsize=(10, 5))

  bins = 40
  axes.hist([default_loans_range1, all_loans_range1], bins=bins,
              label=['Defaulted Loans', 'All Loans'],
              color=['salmon', 'skyblue'],
              edgecolor='black', alpha=0.7,
              histtype='barstacked')
  axes.set_xlabel('Disbursed Amount'.replace('_', ' ').capitalize())
  axes.set_ylabel('Number of Loans')
  axes.set_title('Distribution of Loans with Disbursed Amount ≤ 15% of Maximum')
  axes.legend()
  axes.grid(True)

  plt.tight_layout()
  st.pyplot(fig)

def ltv_bar():
  fig = plt.figure(figsize = (10,4.5))
  all_loans = train_df['ltv']
  default_loans = train_df[train_df['loan_default'] == 1]['ltv']
  bins = 40
  
  plt.hist([default_loans, all_loans], bins=bins,
              label=['Defaulted Loans', 'All Loans'],
              color=['salmon', 'skyblue'],
              edgecolor='black', alpha=0.7,
              histtype = 'barstacked'
          )

  plt.xlabel('Disbursed LtV Ratio'.replace('_', ' ').capitalize())
  plt.ylabel('Number of Loans')
  plt.title(f'Histogram of LtV Ratio')
  plt.legend()
  plt.grid(True)
  st.pyplot(fig)
  
def carbrand_bar():
  
  fig = plt.figure(figsize = (10,4.5))
  loan_brands =   train_df.groupby('manufacturer_id').agg(
    total_loans=('loan_default', 'count'),
    defaulted_loans = ('loan_default', 'sum'),
  ).sort_values(by = 'defaulted_loans', ascending = False).reset_index()
  
  sns.barplot(data=loan_brands, x=loan_brands.index, y='total_loans', color='steelblue', label = 'Number of Total Loans')
  sns.barplot(data=loan_brands, x=loan_brands.index, y='defaulted_loans', color='tomato',
              label = 'Number of Defaulted Loans')
  custom_text = Line2D([], [], linestyle='None', marker='', label='% -- Percentage of Loans Number')
  
  plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], custom_text])
  total_all = loan_brands['total_loans'].sum()
  for i in range(len(loan_brands)):
    total = loan_brands.loc[i, 'total_loans']
    ratio = total / total_all if total > 0 else 0
    
    text = f"{ratio:.1%}"

    fontsize = 9
    plt.text(i, total + max(loan_brands['total_loans']) * 0.01, text,
            ha='center', va='bottom', fontsize=fontsize, color='black')
    
    plt.title('Total Loans for Each Manufacturer')
    plt.xticks(ticks = loan_brands.index, labels = loan_brands['manufacturer_id'])
    plt.ylim([0, max(loan_brands['total_loans']) * 1.2])
    plt.xlabel('Manufacturer ID')
    plt.ylabel('Number of Loans')
    
    plt.grid(axis = 'y', linestyle = '--')
    
  st.pyplot(fig)
  
def monthly_brand(manufacturer_ids):
    palette = dict(zip(manufacturer_ids, plt.get_cmap("tab10").colors[:len(manufacturer_ids)]))
    filtered_df = train_df[train_df['manufacturer_id'].isin(manufacturer_ids)].copy()

    # Ensure datetime format and extract month
    filtered_df['DisbursalDate'] = pd.to_datetime(filtered_df['DisbursalDate'], errors='coerce')
    filtered_df['DisbursalMonth'] = filtered_df['DisbursalDate'].dt.to_period('M')

    # Group by month and manufacturer, count number of loans
    monthly_loan_counts = (
        filtered_df
        .groupby(['DisbursalMonth', 'manufacturer_id'])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )

    # Convert PeriodIndex to Timestamp for plotting
    monthly_loan_counts.index = monthly_loan_counts.index.to_timestamp()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    for mid in manufacturer_ids:
        ax.plot(monthly_loan_counts.index, monthly_loan_counts[mid],
                label=f'Manufacturer ID {mid}', linewidth=2.5, color = palette[mid])

    ax.set_xlabel('Disbursal Month')
    ax.set_ylabel('Number of Loans')
    ax.set_title('Monthly Loan Counts by Manufacturer ID')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

def carbrand_avg(manufacturer_ids):
  palette = dict(zip(manufacturer_ids, plt.get_cmap("tab10").colors[:len(manufacturer_ids)]))
  avg_disbursed = train_df.groupby('manufacturer_id')['asset_cost'].mean()
  avg_disbursed = avg_disbursed[avg_disbursed.index.isin(manufacturer_ids)].sort_values(ascending=False)
  fig = plt.figure(figsize = (5,6))
  
  ordered_ids = avg_disbursed.index.tolist()
  bar_colors = [palette[mid] for mid in ordered_ids]
  sns.barplot(y = avg_disbursed.index.astype(str), x = avg_disbursed.values, palette=bar_colors)
  plt.title('Asset Cost \nby Manufacturer ID')
  plt.ylabel('Manufacturer ID')
  plt.xlabel('Asset Cost (₹)')
  plt.grid(axis = 'x', linestyle = '--')
  fig.tight_layout()
  st.pyplot(fig)