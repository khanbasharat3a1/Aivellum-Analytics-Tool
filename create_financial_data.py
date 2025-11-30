#!/usr/bin/env python3
"""
Create sample financial data Excel file
"""

import pandas as pd
from datetime import datetime
import os

def create_financial_excel():
    """Create Excel file with sample financial data"""
    
    # Income data
    income_data = {
        'Income Source': ['Gumroad', 'Gumroad', 'Play Console', 'Runnable', 'Runnable'],
        'Amount': [2070, 2080, 9060, 2925, 2948],
        'Date': ['2025-11-03', '2025-11-10', '2025-11-17', '2025-11-18', '2025-11-26'],
        'Category': ['Digital Products', 'Digital Products', 'App Revenue', 'Services', 'Services'],
        'Notes': ['Course sales', 'Template sales', 'Monthly payout', 'Development work', 'Consulting']
    }
    
    # Expenses data
    expense_data = {
        'Description': ['Cursor Pro', 'Editor Payment', 'Editor Payment', 'Basharat Salary', 'Abdaal Salary', 'Editor Payment', 'Saleem Salary'],
        'Amount': [2088.64, 500, 500, 4000, 4000, 500, 4000],
        'Date': ['2025-11-07', '2025-11-11', '2025-11-25', '2025-11-30', '2025-11-30', '2025-11-30', '2025-11-30'],
        'Category': ['Tools', 'Outsourcing', 'Outsourcing', 'Salaries', 'Salaries', 'Outsourcing', 'Salaries'],
        'Type': ['Software', 'Service', 'Service', 'Employee', 'Employee', 'Service', 'Employee'],
        'Notes': ['Annual subscription', 'Content editing', 'Content editing', 'Monthly salary', 'Monthly salary', 'Content editing', 'Monthly salary']
    }
    
    # Planned activities data
    planned_data = {
        'Activity': ['Zoho Workplace (5 accounts)', 'Domain Renewal', 'Cursor Pro Renewal', 'Editors Monthly Salary', 'OpenAI API Credits', 'Marketing Ads'],
        'Estimated Cost': [750, 1000, 2000, 5000, 750, 1000],
        'Priority': ['High', 'High', 'Medium', 'High', 'Medium', 'Low'],
        'Status': ['Pending', 'Pending', 'Pending', 'Recurring', 'Pending', 'Planned'],
        'Target Date': ['2025-12-15', '2025-12-31', '2026-11-07', '2025-12-01', '2025-12-10', '2025-12-20'],
        'Notes': ['Email & collaboration', 'Annual renewal', 'Development tool', 'Content team', 'AI services', 'Promotion campaign']
    }
    
    # Create DataFrames
    income_df = pd.DataFrame(income_data)
    expense_df = pd.DataFrame(expense_data)
    planned_df = pd.DataFrame(planned_data)
    
    # Convert dates
    income_df['Date'] = pd.to_datetime(income_df['Date'])
    expense_df['Date'] = pd.to_datetime(expense_df['Date'])
    planned_df['Target Date'] = pd.to_datetime(planned_df['Target Date'])
    
    # Write to Excel
    filename = 'Aivellum_Financials_OCT.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        income_df.to_excel(writer, sheet_name='Income', index=False)
        expense_df.to_excel(writer, sheet_name='Expenses', index=False)
        planned_df.to_excel(writer, sheet_name='Planned', index=False)
    
    print(f"✅ Created {filename} with financial data")
    print(f"📊 Income entries: {len(income_df)}")
    print(f"💸 Expense entries: {len(expense_df)}")
    print(f"📅 Planned activities: {len(planned_df)}")
    
    return filename

if __name__ == "__main__":
    create_financial_excel()