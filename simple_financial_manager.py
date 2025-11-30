"""
Simple Financial Management Module for Aivellum
Handles Income, Expenses, and Planned Activities using CSV files
"""

import csv
import os
from datetime import datetime

class SimpleFinancialManager:
    def __init__(self, base_path='Aivellum_Financials_OCT'):
        self.base_path = base_path
        self.files = {
            'income': f'{base_path}_income.csv',
            'expenses': f'{base_path}_expenses.csv',
            'planned': f'{base_path}_planned.csv'
        }
        self.init_files()
    
    def init_files(self):
        """Initialize CSV files with enhanced sample data"""
        # Income file with more realistic data
        if not os.path.exists(self.files['income']):
            with open(self.files['income'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Income Source', 'Amount', 'Date', 'Category', 'Notes'])
                # Real income data
                writer.writerow(['Gumroad', '2070', '2025-11-03', 'Digital Products', 'Sales revenue'])
                writer.writerow(['Gumroad', '2080', '2025-11-10', 'Digital Products', 'Sales revenue'])
                writer.writerow(['Play Console', '9060', '2025-11-17', 'App Revenue', 'App store revenue'])
                writer.writerow(['Runnable', '2925', '2025-11-18', 'Services', 'Platform commission'])
                writer.writerow(['Runnable', '2948', '2025-11-26', 'Services', 'Platform commission'])
        
        # Enhanced expenses with more categories
        if not os.path.exists(self.files['expenses']):
            with open(self.files['expenses'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Description', 'Amount', 'Date', 'Category', 'Type', 'Notes'])
                # Real expense data
                writer.writerow(['Cursor Pro', '2088.64', '2025-11-07', 'Tools', 'Software', 'Development tool'])
                writer.writerow(['Editor', '500', '2025-11-11', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Editor', '500', '2025-11-25', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Basharat', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
                writer.writerow(['Abdaal', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
                writer.writerow(['Editor', '500', '2025-11-30', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Saleem', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
        
        # Enhanced planned activities with priorities
        if not os.path.exists(self.files['planned']):
            with open(self.files['planned'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Activity', 'Estimated Cost', 'Priority', 'Status', 'Target Date', 'Notes'])
                # Real planned activities
                writer.writerow(['Zoho Workplace (for 5 accounts)', '750', 'Medium', 'Pending', '2025-12-15', 'Business email solution'])
                writer.writerow(['Domain', '1000', 'High', 'Pending', '2025-12-10', 'Domain registration'])
                writer.writerow(['Cursor pro', '2000', 'High', 'Pending', '2025-12-05', 'Development tool'])
                writer.writerow(['Editors salary', '5000', 'High', 'Pending', '2025-12-31', 'Monthly editor payments'])
                writer.writerow(['Openai API Credits', '750', 'Medium', 'Pending', '2025-12-20', 'AI service credits'])
                writer.writerow(['Ads', '1000', 'Medium', 'Pending', '2025-12-25', 'Marketing campaigns'])
        
        print(f"✅ Financial data files initialized with enhanced sample data")
        print(f"💰 Income entries: {self._count_entries('income')}")
        print(f"💸 Expense entries: {self._count_entries('expenses')}")
        print(f"📅 Planned activities: {self._count_entries('planned')}")
    
    def _count_entries(self, file_type):
        """Count entries in a CSV file"""
        try:
            with open(self.files[file_type], 'r', encoding='utf-8') as f:
                return len(list(csv.reader(f))) - 1  # Subtract header
        except:
            return 0
    
    def load_data(self):
        """Load all financial data from CSV files"""
        data = {'income': [], 'expenses': [], 'planned': []}
        
        # Load income
        try:
            with open(self.files['income'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data['income'] = list(reader)
        except Exception as e:
            print(f"Error loading income: {e}")
        
        # Load expenses
        try:
            with open(self.files['expenses'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data['expenses'] = list(reader)
        except Exception as e:
            print(f"Error loading expenses: {e}")
        
        # Load planned
        try:
            with open(self.files['planned'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data['planned'] = list(reader)
        except Exception as e:
            print(f"Error loading planned: {e}")
        
        return data
    
    def get_financial_summary(self, start_date=None, end_date=None):
        """Get financial summary with cash flow analysis"""
        data = self.load_data()
        
        # Calculate totals
        total_income = float(sum(float(row['Amount']) for row in data['income']))
        total_expenses = float(sum(float(row['Amount']) for row in data['expenses']))
        net_cash_flow = float(total_income - total_expenses)
        
        # Category breakdowns
        income_by_category = {}
        for row in data['income']:
            category = row['Category']
            amount = float(row['Amount'])
            income_by_category[category] = float(income_by_category.get(category, 0) + amount)
        
        expenses_by_category = {}
        for row in data['expenses']:
            category = row['Category']
            amount = float(row['Amount'])
            expenses_by_category[category] = float(expenses_by_category.get(category, 0) + amount)
        
        # Planned expenses
        planned_total = float(sum(float(row['Estimated Cost']) for row in data['planned']))
        
        # Calculate additional metrics
        expense_breakdown = self.get_expense_breakdown()
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_cash_flow': net_cash_flow,
            'income_by_category': income_by_category,
            'expenses_by_category': expenses_by_category,
            'planned_expenses': planned_total,
            'projected_cash_flow': float(net_cash_flow - planned_total),
            'expense_breakdown': expense_breakdown,
            'metrics': {
                'income_count': len(data['income']),
                'expense_count': len(data['expenses']),
                'planned_count': len(data['planned']),
                'avg_income': float(total_income / len(data['income'])) if data['income'] else 0,
                'avg_expense': float(total_expenses / len(data['expenses'])) if data['expenses'] else 0,
                'cash_flow_ratio': float(net_cash_flow / total_income * 100) if total_income > 0 else 0
            }
        }
    
    def add_income(self, source, amount, date, category='Other', notes=''):
        """Add new income entry"""
        try:
            with open(self.files['income'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([source, str(amount), date, category, notes])
            return True
        except Exception as e:
            print(f"Error adding income: {e}")
            return False
    
    def add_expense(self, description, amount, date, category, exp_type, notes=''):
        """Add new expense entry"""
        try:
            with open(self.files['expenses'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([description, str(amount), date, category, exp_type, notes])
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def add_planned_activity(self, activity, cost, priority, status, target_date, notes=''):
        """Add new planned activity"""
        try:
            with open(self.files['planned'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([activity, str(cost), priority, status, target_date, notes])
            return True
        except Exception as e:
            print(f"Error adding planned activity: {e}")
            return False
    
    def get_monthly_trends(self):
        """Get enhanced monthly financial trends"""
        data = self.load_data()
        trends = []
        
        # Group by month
        monthly_income = {}
        monthly_expenses = {}
        
        # Process income by month
        for row in data['income']:
            try:
                date_str = row['Date']
                month = date_str[:7]  # YYYY-MM format
                amount = float(row['Amount'])
                monthly_income[month] = monthly_income.get(month, 0) + amount
            except (ValueError, KeyError):
                continue
        
        # Process expenses by month
        for row in data['expenses']:
            try:
                date_str = row['Date']
                month = date_str[:7]  # YYYY-MM format
                amount = float(row['Amount'])
                monthly_expenses[month] = monthly_expenses.get(month, 0) + amount
            except (ValueError, KeyError):
                continue
        
        # Combine data for trends
        all_months = set(list(monthly_income.keys()) + list(monthly_expenses.keys()))
        
        for month in sorted(all_months):
            income = monthly_income.get(month, 0)
            expenses = monthly_expenses.get(month, 0)
            
            trends.extend([
                {
                    'Month': month,
                    'Amount': float(income),
                    'Type': 'Income'
                },
                {
                    'Month': month,
                    'Amount': float(-expenses),
                    'Type': 'Expenses'
                },
                {
                    'Month': month,
                    'Amount': float(income - expenses),
                    'Type': 'Net Flow'
                }
            ])
        
        return trends
    
    def get_expense_breakdown(self):
        """Get detailed expense breakdown by category"""
        data = self.load_data()
        breakdown = {}
        
        for row in data['expenses']:
            try:
                category = row['Category']
                amount = float(row['Amount'])
                if category not in breakdown:
                    breakdown[category] = {
                        'total': 0,
                        'count': 0,
                        'items': []
                    }
                breakdown[category]['total'] += amount
                breakdown[category]['count'] += 1
                breakdown[category]['items'].append({
                    'description': row['Description'],
                    'amount': amount,
                    'date': row['Date'],
                    'type': row.get('Type', 'Other')
                })
            except (ValueError, KeyError):
                continue
        
        return breakdown
    
    def get_financial_insights(self):
        """Generate financial insights and recommendations"""
        summary = self.get_financial_summary()
        breakdown = self.get_expense_breakdown()
        insights = []
        
        # Cash flow analysis
        if summary['net_cash_flow'] > 0:
            insights.append({
                'type': 'success',
                'title': 'Positive Cash Flow',
                'message': f"You have a healthy cash flow of ₹{summary['net_cash_flow']:,.2f}",
                'recommendation': 'Consider investing surplus in growth opportunities'
            })
        else:
            insights.append({
                'type': 'warning',
                'title': 'Negative Cash Flow',
                'message': f"Cash flow deficit of ₹{abs(summary['net_cash_flow']):,.2f}",
                'recommendation': 'Review expenses and increase income sources'
            })
        
        # Expense analysis
        if breakdown:
            largest_category = max(breakdown.items(), key=lambda x: x[1]['total'])
            category_name, category_data = largest_category
            percentage = (category_data['total'] / summary['total_expenses']) * 100
            
            if percentage > 50:
                insights.append({
                    'type': 'info',
                    'title': f'{category_name} Dominates Expenses',
                    'message': f"{category_name} accounts for {percentage:.1f}% of total expenses",
                    'recommendation': f'Monitor {category_name} spending closely'
                })
        
        # Planned expenses warning
        if summary['projected_cash_flow'] < 0:
            insights.append({
                'type': 'warning',
                'title': 'Planned Expenses Risk',
                'message': f"Planned expenses may cause ₹{abs(summary['projected_cash_flow']):,.2f} deficit",
                'recommendation': 'Prioritize planned expenses or increase income'
            })
        
        return insights