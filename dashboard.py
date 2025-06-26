import streamlit as st  
import dashboardData1 as dd1
import dashboardData2 as dd2
import pandas as pd

st.set_page_config(page_title='Loan Payment EDA', page_icon=':bar_chart:', layout='wide')
st.title('Vehicle Loan Payment Analysis')

st.markdown("<br>", unsafe_allow_html=True)

#Introductory Section
col11, _, col12 = st.columns([0.7,0.2, 1.5]) 

with col11:
    st.markdown(
    """
    <h2 style='text-align: left'>Data Overview</h2>
    
    <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
    <p>
    This dashboard presents an exploratory data analysis of vehicle loan defaults based on the 
    <a href="https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction/data" target="_blank">
    L&T Vehicle Loans Dataset</a>, which contains over 200,000 records. After feature engineering, the dataset includes various attributes related to loan performance and borrower profiles.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

with col12:
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(dd1.info, use_container_width=True)

#Company Summary Section 1 
st.markdown("""
            <h2 style = 'text-align: left'>Loan Performance Summary</h2>
            """,
            unsafe_allow_html=True)

#SubSection 1.1: Loan Details
pol11, pol12, pol13 = st.tabs(['Overall Loan Performance', 'Amount of Disbursed Loans', 'Early Remarks'])

with pol11:
    cp10, _, cp11, cp12 = st.columns([0.4,0.1,1,0.5])
    with cp10:
        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        This section highlights monthly loan performance trends. 
        <br>
        Loan disbursements surged from July to November 2018, with a peak in October. 
        <br>
        This period also saw a sharp increase in defaults, with about 22% of all 2018 loans defaulting by year-end.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
        
    with cp11:
        dd1.monthly_line_plot()
    with cp12:
        dd1.loan_number_pie()

with pol12: 
    cp13, _, cp14, cp15 = st.columns([0.4,0.1,1,0.5])

    with cp13:
        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        This section shows the distribution of loans by amounts disbursed and loan to value ratio. 
        <br>
        Loans distribution is limited up to 15% of the maximum disbursed amount which is ₹990.572 because up to 99.97% loans fall within this range.
        <br>
        The amount of defaulted loans cause up to 22% of the total disbursed amount which reaches ₹2.8 billion
        </p>        
        </div>
        """,
        unsafe_allow_html=True
        )
    
    with cp14:
        minpol1, minpol2 = st.tabs(['Disbursed Amounts', 'Loan to Value (ltv) Ratio'])
        with minpol1:
            dd1.disburse_bar15()
        with minpol2:
            dd1.ltv_bar()
    with cp15:
        dd1.loan_amount_pie()

with pol13:
    cp16, _, cp17, cp18 = st.columns([0.4,0.1,1,0.5])
    
    with cp16:

        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        We deduced that the surge in number of loans applicants is caused by increased interest in a certain automotive brands.
        <br>
        This corresponds to the informations regarding average disbursed amount and monthly number of applicants coming from these 6 most popular brands (manufacturer IDs)
        </p>        
        </div>
        """,
        unsafe_allow_html=True
        )
    with cp18:
        dd1.carbrand_avg([86, 45, 51, 48, 49, 120])
    with cp17:
        minpol3, minpol4 = st.tabs(['Number of Loans', 'Monthly Loan Counts'])
        with minpol3:
            dd1.carbrand_bar()
        with minpol4:
           dd1.monthly_brand([86, 45, 51, 48, 49, 120])
        
    
#Subection 1.2: 

st.markdown("""
            <h2 style = 'text-align: left'>Categorical Analysis of Disbursed Loan</h2>
            """,
            unsafe_allow_html=True)

pol21, pol22, pol23 = st.tabs(['Demographic', 'Identification', 'Credit Score'])

with pol21:
    cp21, _, cp22 = st.columns([0.4,0.1,1])
    
    with cp21:
        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        This section shows the distribution of loans by demographic attributes, notably
        age, state of residence, and employment category.
        <br><br>
        Based on these analysis we could infer that the majority of applicants are young adults, 
        coming from the state numbered 4, 6, and 3, with more than 50% of all applicants being self-employed.
        
        </p>        
        </div>
        """,
        unsafe_allow_html=True
        )
    
    with cp22:
        minpol5, minpol6, minpol7 = st.tabs(['Age Distribution', 'State Distribution', 'Employment Category',])
        with minpol5:
            dd2.age_hist()
        with minpol6:
            dd2.state_bar()
        with minpol7:
            dd2.emp_bar()
    
with pol22:
    cp23, _, cp24 = st.columns([0.4,0.1,1])
    
    with cp23:
        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        This section shows the distribution of loans based on the identification attributes provided by 
        the applicants. As shown, most of the applicants only provided 1 identification attribute, dominantly
        ID card.
        
        </p>        
        </div>
        """,
        unsafe_allow_html=True
        )
    with cp24:
        minpol8, minpol9 = st.tabs(['Number of IDs Provided', 'ID Type Distribution'])
        with minpol8:
            dd2.id_count_bar()
        with minpol9:  
            dd2.id_bar()

with pol23:
    cp25, _, cp26, _ = st.columns([0.4,0.1,1, 0.2])
    
    with cp25:
        st.markdown(
        """
        <br>
        <div style = 'text-align: justify; font-size: 16px; line-height: 1.5;'>
        <p>
        This section shows the distribution of loans based on the credit score category.
        <br><br>
        The majority of applicants were first-time loaners without any credit history. This became a major concern
        in determining the creditworthiness of the applicants as current dataset heavily relies on applicants' 
        credit history.
        <br><br>
        Among experienced applicants, up to 99.5% of issued loans went to those with fewer than 5 overdue accounts, 
        highlighting a clear trend in disbursement and defaults.
        </p>        
        </div>
        """,
        unsafe_allow_html=True
        )
    
    with cp26:
        minpol10, minpol11,minpol12 = st.tabs(['Credit Score Category', 'Borrower Type', 'Overdue Accounts'])
        with minpol10:
            dd2.creditscore_bar()
        with minpol11:
            dd2.accountsnum_bar()
        with minpol12:
            dd2.overdue_hist()