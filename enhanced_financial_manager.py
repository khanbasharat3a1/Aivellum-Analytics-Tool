"""
Enhanced Financial Management Module for Aivellum
Handles Income, Expenses, and Planned Activities with advanced analytics
"""

import csv
import os
from datetime import datetime

class EnhancedFinancialManager:
    def __init__(self, base_path='Aivellum_Financials_OCT'):
        self.base_path = base_path
        self.files = {
            'income': f'{base_path}_income.csv',
            'expenses': f'{base_path}_expenses.csv',
            'planned': f'{base_path}_planned.csv'
        }
        
        # Define expense categories
        self.expense_categories = {
            'Salaries': 'Team and freelancer payments',
            'Tools': 'Software, hardware, and development tools',
            'Outsourcing': 'External services and contractors',
            'Business': 'Legal, infrastructure, and operational costs',
            'Marketing': 'Advertising, promotion, and content creation'
        }
        
        # Define income categories
        self.income_categories = {
            'Digital Products': 'Course sales, templates, digital downloads',
            'App Revenue': 'Play Store, App Store earnings',
            'Services': 'Consulting, custom development, freelance work',
            'Other': 'Miscellaneous income sources'
        }
        
        self.init_files()
    
    def init_files(self):
        """Initialize CSV files with real user data"""
        # Income file
        if not os.path.exists(self.files['income']):
            with open(self.files['income'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Income Source', 'Amount', 'Date', 'Category', 'Notes'])
                # Real income data - November 2025
                writer.writerow(['Gumroad', '2070', '2025-11-03', 'Digital Products', 'Sales revenue'])
                writer.writerow(['Gumroad', '2080', '2025-11-10', 'Digital Products', 'Sales revenue'])
                writer.writerow(['Play Console', '9060', '2025-11-17', 'App Revenue', 'App store revenue'])
                writer.writerow(['Runnable', '2925', '2025-11-18', 'Services', 'Platform commission'])
                writer.writerow(['Runnable', '2948', '2025-11-26', 'Services', 'Platform commission'])
        
        # Expenses file
        if not os.path.exists(self.files['expenses']):
            with open(self.files['expenses'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Description', 'Amount', 'Date', 'Category', 'Type', 'Notes'])
                # Real expense data - November 2025
                writer.writerow(['Cursor Pro', '2088.64', '2025-11-07', 'Tools', 'Software', 'Development tool'])
                writer.writerow(['Editor', '500', '2025-11-11', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Editor', '500', '2025-11-25', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Basharat', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
                writer.writerow(['Abdaal', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
                writer.writerow(['Editor', '500', '2025-11-30', 'Salaries', 'Freelancer', 'Editor salary'])
                writer.writerow(['Saleem', '4000', '2025-11-30', 'Salaries', 'Employee', 'Team salary'])
        
        # Planned activities file
        if not os.path.exists(self.files['planned']):
            with open(self.files['planned'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Activity', 'Estimated Cost', 'Priority', 'Status', 'Target Date', 'Notes'])
                # Real planned activities - December 2025
                writer.writerow(['Zoho Workplace (for 5 accounts)', '750', 'Medium', 'Pending', '2025-12-15', 'Business email solution'])
                writer.writerow(['Domain', '1000', 'High', 'Pending', '2025-12-10', 'Domain registration'])
                writer.writerow(['Cursor pro', '2000', 'High', 'Pending', '2025-12-05', 'Development tool'])
                writer.writerow(['Editors salary', '5000', 'High', 'Pending', '2025-12-31', 'Monthly editor payments'])
                writer.writerow(['Openai API Credits', '750', 'Medium', 'Pending', '2025-12-20', 'AI service credits'])
                writer.writerow(['Ads', '1000', 'Medium', 'Pending', '2025-12-25', 'Marketing campaigns'])
        
        print(f"✅ Financial data files initialized with real user data")
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
    
    def get_monthly_trends(self):
        """Get enhanced monthly financial trends with proper formatting"""
        data = self.load_data()
        
        # Group by month
        monthly_data = {}
        
        # Process income by month
        for row in data['income']:
            try:
                date_str = row['Date']
                month = date_str[:7]  # YYYY-MM format
                amount = float(row['Amount'])
                
                if month not in monthly_data:
                    monthly_data[month] = {'income': 0, 'expenses': 0}
                monthly_data[month]['income'] += amount
            except (ValueError, KeyError) as e:
                print(f"Error processing income date {row.get('Date', 'N/A')}: {e}")
                continue
        
        # Process expenses by month
        for row in data['expenses']:
            try:
                date_str = row['Date']
                month = date_str[:7]  # YYYY-MM format
                amount = float(row['Amount'])
                
                if month not in monthly_data:
                    monthly_data[month] = {'income': 0, 'expenses': 0}
                monthly_data[month]['expenses'] += amount
            except (ValueError, KeyError) as e:
                print(f"Error processing expense date {row.get('Date', 'N/A')}: {e}")
                continue
        
        # Convert to chart format
        trends = []
        for month in sorted(monthly_data.keys()):
            data_point = monthly_data[month]
            income = data_point['income']
            expenses = data_point['expenses']
            net_flow = income - expenses
            
            # Format month for display
            try:
                month_obj = datetime.strptime(month, '%Y-%m')
                month_name = month_obj.strftime('%b %Y')
            except:
                month_name = month
            
            trends.append({
                'month': month,
                'month_name': month_name,
                'income': float(income),
                'expenses': float(expenses),
                'net_flow': float(net_flow)
            })
        
        return trends
    
    def get_expense_breakdown(self):
        """Get detailed expense breakdown by category with enhanced analysis"""
        data = self.load_data()
        breakdown = {}
        total_expenses = 0
        
        # Initialize all categories
        for category in self.expense_categories.keys():
            breakdown[category] = {
                'total': 0,
                'count': 0,
                'percentage': 0,
                'items': [],
                'avg_amount': 0
            }
        
        # Process expenses
        for row in data['expenses']:
            try:
                category = row.get('Category', 'Other')
                amount = float(row['Amount'])
                total_expenses += amount
                
                if category not in breakdown:
                    breakdown[category] = {
                        'total': 0,
                        'count': 0,
                        'percentage': 0,
                        'items': [],
                        'avg_amount': 0
                    }
                
                breakdown[category]['total'] += amount
                breakdown[category]['count'] += 1
                breakdown[category]['items'].append({
                    'description': row.get('Description', 'N/A'),
                    'amount': amount,
                    'date': row.get('Date', 'N/A'),
                    'type': row.get('Type', 'Other'),
                    'notes': row.get('Notes', '')
                })
            except (ValueError, KeyError) as e:
                print(f"Error processing expense: {e}")
                continue
        
        # Calculate percentages and averages
        for category in breakdown:
            if breakdown[category]['count'] > 0:
                breakdown[category]['avg_amount'] = breakdown[category]['total'] / breakdown[category]['count']
            if total_expenses > 0:
                breakdown[category]['percentage'] = (breakdown[category]['total'] / total_expenses) * 100
        
        # Add summary
        breakdown['_summary'] = {
            'total_expenses': total_expenses,
            'categories_count': len([c for c in breakdown if breakdown[c]['count'] > 0]),
            'largest_category': max(breakdown.items(), key=lambda x: x[1]['total'] if x[0] != '_summary' else 0)[0] if breakdown else None
        }
        
        return breakdown
    
    def get_financial_insights(self):
        """Generate enhanced AI-powered financial insights and recommendations"""
        summary = self.get_financial_summary()
        breakdown = self.get_expense_breakdown()
        performance = self.get_performance_metrics()
        data = self.load_data()
        insights = []
        
        # Cash flow analysis with detailed recommendations
        cash_flow_ratio = summary['net_cash_flow'] / summary['total_income'] if summary['total_income'] > 0 else 0
        
        if summary['net_cash_flow'] > 0:
            if cash_flow_ratio > 0.3:
                insights.append({
                    'type': 'success',
                    'title': 'Excellent Cash Flow Management',
                    'message': f"Outstanding {cash_flow_ratio*100:.1f}% profit margin (₹{summary['net_cash_flow']:,.0f})",
                    'recommendation': 'Consider reinvesting 20-30% in growth initiatives or emergency fund',
                    'priority': 'high'
                })
            else:
                insights.append({
                    'type': 'success',
                    'title': 'Positive Cash Flow',
                    'message': f"Healthy {cash_flow_ratio*100:.1f}% profit margin (₹{summary['net_cash_flow']:,.0f})",
                    'recommendation': 'Build emergency fund covering 3-6 months of expenses',
                    'priority': 'medium'
                })
        else:
            insights.append({
                'type': 'danger',
                'title': 'Critical Cash Flow Deficit',
                'message': f"Urgent: ₹{abs(summary['net_cash_flow']):,.0f} deficit ({abs(cash_flow_ratio)*100:.1f}%)",
                'recommendation': 'Immediate action: reduce non-essential expenses, increase income sources',
                'priority': 'critical'
            })
        
        # Income diversity analysis
        diversity = performance['income_diversity']
        if diversity['index'] < 0.3:
            insights.append({
                'type': 'warning',
                'title': 'Income Concentration Risk',
                'message': f"Over-reliance on {diversity['primary_source']} ({(1-diversity['index'])*100:.0f}% concentration)",
                'recommendation': 'Diversify income streams to reduce dependency risk',
                'priority': 'high'
            })
        elif diversity['index'] > 0.7:
            insights.append({
                'type': 'info',
                'title': 'Well-Diversified Income',
                'message': f"Excellent income diversification across {len(diversity['sources'])} sources",
                'recommendation': 'Maintain current diversification strategy',
                'priority': 'low'
            })
        
        # Expense efficiency analysis
        efficiency = performance['expense_efficiency']
        if efficiency['ratio'] < 0.2:
            insights.append({
                'type': 'warning',
                'title': 'Low Investment in Growth',
                'message': f"Only {efficiency['ratio']*100:.1f}% spent on tools/marketing",
                'recommendation': 'Increase investment in growth-driving expenses (tools, marketing)',
                'priority': 'medium'
            })
        
        # Salary expense analysis
        salary_expenses = breakdown.get('Salaries', {}).get('total', 0)
        salary_ratio = salary_expenses / summary['total_income'] if summary['total_income'] > 0 else 0
        
        if salary_ratio > 0.6:
            insights.append({
                'type': 'warning',
                'title': 'High Salary Burden',
                'message': f"Salaries consume {salary_ratio*100:.1f}% of income (₹{salary_expenses:,.0f})",
                'recommendation': 'Consider productivity improvements or revenue optimization',
                'priority': 'high'
            })
        
        # Planned expenses analysis with priority insights
        high_priority_planned = sum(float(row['Estimated Cost']) for row in data['planned'] if row.get('Priority') == 'High')
        if high_priority_planned > summary['net_cash_flow']:
            insights.append({
                'type': 'warning',
                'title': 'High-Priority Expenses Exceed Cash Flow',
                'message': f"₹{high_priority_planned:,.0f} high-priority expenses vs ₹{summary['net_cash_flow']:,.0f} available",
                'recommendation': 'Secure additional funding or defer lower-priority items',
                'priority': 'high'
            })
        
        # Growth opportunity insights
        if summary['net_cash_flow'] > 10000 and efficiency['ratio'] < 0.3:
            insights.append({
                'type': 'info',
                'title': 'Growth Investment Opportunity',
                'message': f"₹{summary['net_cash_flow']:,.0f} available for strategic investments",
                'recommendation': 'Consider investing in marketing, tools, or team expansion',
                'priority': 'medium'
            })
        
        # Sort insights by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        insights.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        
        return insights
    
    def get_cash_flow_analysis(self):
        """Get detailed cash flow analysis with projections"""
        data = self.load_data()
        summary = self.get_financial_summary()
        
        # Weekly cash flow
        weekly_flow = {}
        
        # Process by week
        for row in data['income']:
            try:
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
                week = date_obj.strftime('%Y-W%U')
                amount = float(row['Amount'])
                
                if week not in weekly_flow:
                    weekly_flow[week] = {'income': 0, 'expenses': 0}
                weekly_flow[week]['income'] += amount
            except:
                continue
        
        for row in data['expenses']:
            try:
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
                week = date_obj.strftime('%Y-W%U')
                amount = float(row['Amount'])
                
                if week not in weekly_flow:
                    weekly_flow[week] = {'income': 0, 'expenses': 0}
                weekly_flow[week]['expenses'] += amount
            except:
                continue
        
        # Calculate projections
        avg_weekly_income = sum(w['income'] for w in weekly_flow.values()) / len(weekly_flow) if weekly_flow else 0
        avg_weekly_expenses = sum(w['expenses'] for w in weekly_flow.values()) / len(weekly_flow) if weekly_flow else 0
        
        return {
            'current_balance': summary['net_cash_flow'],
            'weekly_flow': weekly_flow,
            'projections': {
                'next_month_income': avg_weekly_income * 4,
                'next_month_expenses': avg_weekly_expenses * 4,
                'next_month_net': (avg_weekly_income - avg_weekly_expenses) * 4
            },
            'burn_rate': avg_weekly_expenses,
            'runway_weeks': summary['net_cash_flow'] / avg_weekly_expenses if avg_weekly_expenses > 0 else float('inf')
        }
    
    def export_data(self):
        """Export all financial data for download"""
        data = self.load_data()
        summary = self.get_financial_summary()
        
        export_summary = {
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_income': summary['total_income'],
            'total_expenses': summary['total_expenses'],
            'net_cash_flow': summary['net_cash_flow'],
            'data_counts': {
                'income_entries': len(data['income']),
                'expense_entries': len(data['expenses']),
                'planned_entries': len(data['planned'])
            }
        }
        
        return {
            'summary': export_summary,
            'income_data': data['income'],
            'expense_data': data['expenses'],
            'planned_data': data['planned']
        }
    
    def get_performance_metrics(self):
        """Get advanced performance metrics"""
        data = self.load_data()
        summary = self.get_financial_summary()
        
        # Income source diversity
        income_sources = {}
        for row in data['income']:
            source = row.get('Income Source', 'Unknown')
            amount = float(row['Amount'])
            income_sources[source] = income_sources.get(source, 0) + amount
        
        # Calculate diversity index (higher = more diverse)
        total_income = sum(income_sources.values())
        diversity_index = 0
        if total_income > 0:
            for amount in income_sources.values():
                ratio = amount / total_income
                diversity_index += ratio * ratio
            diversity_index = 1 - diversity_index  # Convert to diversity (0 = concentrated, 1 = diverse)
        
        # Expense efficiency
        expense_categories = summary.get('expenses_by_category', {})
        productive_expenses = expense_categories.get('Tools', 0) + expense_categories.get('Marketing', 0)
        total_expenses = summary['total_expenses']
        efficiency_ratio = productive_expenses / total_expenses if total_expenses > 0 else 0
        
        return {
            'income_diversity': {
                'index': diversity_index,
                'sources': income_sources,
                'primary_source': max(income_sources.items(), key=lambda x: x[1])[0] if income_sources else None
            },
            'expense_efficiency': {
                'ratio': efficiency_ratio,
                'productive_expenses': productive_expenses,
                'total_expenses': total_expenses
            },
            'cash_flow_health': {
                'ratio': summary['net_cash_flow'] / summary['total_income'] if summary['total_income'] > 0 else 0,
                'status': 'Healthy' if summary['net_cash_flow'] > 0 else 'Needs Attention'
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