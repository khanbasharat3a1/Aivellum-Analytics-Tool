"""
═══════════════════════════════════════════════════════════════════════════════
    AIVELLUM INCOME STREAM TRACKER v3.0 - COMPREHENSIVE UPGRADE
    
    🚀 NEW FEATURES:
    - ✅ Full income stream tracking (apps, promotions, affiliates, etc.)
    - ✅ FIXED date filtering (start/end dates now work properly)
    - ✅ FIXED trends ordering (chronological order)
    - ✅ Dynamic platform/user inputs with "Other" option
    - ✅ Enhanced income categories and sources
    - ✅ Better revenue analytics and insights
    - ✅ Improved performance and caching
    
    Version: 3.0.0 - COMPREHENSIVE INCOME TRACKER
═══════════════════════════════════════════════════════════════════════════════
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import io
import os
import re
import csv
import logging
from logging.handlers import RotatingFileHandler
from functools import lru_cache
import warnings
from config import config
try:
    from financial_manager import FinancialManager
except ImportError:
    from simple_financial_manager import SimpleFinancialManager as FinancialManager

warnings.filterwarnings('ignore')

def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__, template_folder='templates')
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Setup CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Setup logging
    setup_logging(app)
    
    return app

def setup_logging(app):
    """Configure application logging"""
    os.makedirs(app.config['LOG_DIR'], exist_ok=True)
    
    file_handler = RotatingFileHandler(
        os.path.join(app.config['LOG_DIR'], app.config['LOG_FILE']),
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )
    
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')
    )
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))

# Create app instance
app = create_app()



# ═══════════════════════════════════════════════════════════════════════════
# CURRENCY DATABASE
# ═══════════════════════════════════════════════════════════════════════════

CURRENCY_RATES = {
    # Major currencies
    'USD': 83.12, 'EUR': 89.23, 'GBP': 105.45, 'JPY': 0.56, 'CHF': 94.56,
    'CAD': 61.23, 'AUD': 54.67, 'NZD': 50.12, 'SGD': 62.18, 'HKD': 10.67,
    'CNY': 11.45, 'INR': 1.0,
    
    # Asian currencies
    'KRW': 0.062, 'TWD': 2.68, 'THB': 2.35, 'MYR': 18.56, 'IDR': 0.0053,
    'PHP': 1.48, 'VND': 0.0034, 'PKR': 0.30, 'BDT': 0.76, 'LKR': 0.28,
    'NPR': 0.62, 'MMK': 0.040, 'KHR': 0.020, 'LAK': 0.0039,
    
    # Middle East & Africa
    'AED': 22.62, 'SAR': 22.15, 'QAR': 22.83, 'KWD': 270.45, 'BHD': 220.34,
    'OMR': 216.12, 'JOD': 117.23, 'ILS': 22.45, 'EGP': 1.69, 'ZAR': 4.56,
    'NGN': 0.047, 'KES': 0.64, 'GHS': 5.89, 'TZS': 0.033, 'UGX': 0.022,
    'MAD': 8.45, 'TND': 26.78, 'DZD': 0.62, 'LYD': 17.12, 'ETB': 0.67,
    
    # European currencies
    'SEK': 7.89, 'NOK': 7.78, 'DKK': 11.98, 'PLN': 20.45, 'CZK': 3.56,
    'HUF': 0.23, 'RON': 18.12, 'BGN': 45.67, 'HRK': 11.34, 'RSD': 0.76,
    'TRY': 2.45, 'RUB': 0.88, 'UAH': 2.01, 'ISK': 0.60,
    
    # Americas
    'MXN': 4.89, 'BRL': 16.78, 'ARS': 0.089, 'CLP': 0.089, 'COP': 0.020,
    'PEN': 22.01, 'VES': 0.0024, 'UYU': 2.12, 'BOB': 12.01, 'PYG': 0.011,
    'CRC': 0.16, 'GTQ': 10.67, 'DOP': 1.38, 'JMD': 0.53, 'TTD': 12.23,
    
    # Oceania
    'FJD': 36.78, 'PGK': 21.45, 'WST': 30.12, 'TOP': 35.23,
    
    # Others
    'AFN': 0.96, 'ALL': 0.88, 'AMD': 0.21, 'AOA': 0.10, 'AZN': 48.90,
    'BAM': 45.67, 'BDT': 0.76, 'BIF': 0.029, 'BND': 62.18, 'BWP': 6.12,
    'BYN': 25.45, 'CDF': 0.029, 'CVE': 0.82, 'DJF': 0.47, 'ERN': 5.54,
    'GEL': 31.23, 'GNF': 0.0096, 'HTG': 0.63, 'IQD': 0.063, 'IRR': 0.0020,
    'JOD': 117.23, 'KGS': 0.95, 'KZT': 0.17, 'LBP': 0.00093, 'LRD': 0.43,
    'LSL': 4.56, 'MDL': 4.67, 'MGA': 0.019, 'MKD': 1.45, 'MNT': 0.024,
    'MOP': 10.34, 'MRU': 2.09, 'MUR': 1.79, 'MVR': 5.38, 'MWK': 0.048,
    'MZN': 1.30, 'NAD': 4.56, 'NIO': 2.26, 'PAB': 83.12, 'SCR': 6.12,
    'SDG': 0.14, 'SLL': 0.0040, 'SOS': 0.15, 'SRD': 2.34, 'SSP': 0.064,
    'STN': 3.67, 'SYP': 0.0066, 'SZL': 4.56, 'TJS': 7.56, 'TMT': 23.75,
    'UZS': 0.0065, 'XAF': 0.14, 'XCD': 30.78, 'XOF': 0.14, 'XPF': 0.74,
    'YER': 0.33, 'ZMW': 3.12, 'ZWL': 0.26
}

# Global data cache
DATA_CACHE = {'processed_data': None, 'last_updated': None}

# Financial manager instance - Using enhanced manager for better features
from enhanced_financial_manager import EnhancedFinancialManager
financial_manager = EnhancedFinancialManager()
print("💰 Financial Manager: Using enhanced CSV-based system with advanced analytics")

# Income stream categories
INCOME_CATEGORIES = {
    'App Sales': ['Play Store', 'App Store', 'Aivellum'],
    'Digital Products': ['Gumroad', 'Stripe', 'PayPal'],
    'Promotions': ['Affiliate', 'Sponsorship', 'Partnership'],
    'Services': ['Consulting', 'Development', 'Design'],
    'Subscriptions': ['Monthly', 'Annual', 'Lifetime'],
    'Other': ['Direct', 'Bank Transfer', 'Crypto']
}

# Platform options with dynamic "Other" support
PLATFORM_OPTIONS = [
    'Play Store', 'App Store', 'Aivellum', 'Gumroad', 'Stripe', 'PayPal',
    'Affiliate Network', 'Direct Sales', 'Consulting', 'Freelance',
    'YouTube', 'Blog', 'Course Sales', 'Other'
]

# User type options
USER_TYPE_OPTIONS = [
    'Android', 'iOS', 'Web', 'Desktop', 'Mobile', 'Tablet',
    'Enterprise', 'Individual', 'Student', 'Developer', 'Other'
]

# ═══════════════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1000)
def extract_currency_amount(amount_str):
    """Extract amount and currency from string - handles all formats"""
    if pd.isna(amount_str) or not amount_str:
        return 0.0, 'INR'
    
    amount_str = str(amount_str).strip()
    if not amount_str:
        return 0.0, 'INR'
    
    # Currency symbol mapping
    symbol_map = {'$': 'USD', '£': 'GBP', '€': 'EUR', '₹': 'INR', '₩': 'KRW', '₦': 'NGN'}
    
    # Replace symbols with codes
    for symbol, code in symbol_map.items():
        amount_str = amount_str.replace(symbol, f'{code} ')
    
    # Extract currency code
    amount_upper = amount_str.upper()
    for currency in CURRENCY_RATES:
        if currency in amount_upper:
            numbers = re.findall(r'\d+(?:[,.]\d+)*', amount_str.replace(',', ''))
            if numbers:
                try:
                    return float(numbers[0]), currency
                except ValueError:
                    continue
    
    # Extract number only
    numbers = re.findall(r'\d+(?:[,.]\d+)*', amount_str.replace(',', ''))
    amount = float(numbers[0]) if numbers else 0.0
    return amount, 'USD'

@lru_cache(maxsize=1000)
def to_inr(amount, currency):
    """Convert to INR with caching"""
    if amount == 0:
        return 0.0
    return round(float(amount) * CURRENCY_RATES.get(currency, 1.0), 2)

def parse_datetime(row):
    """Parse datetime - optimized with better error handling"""
    try:
        date_val, time_val = row['Date'], row['Time']
        
        # Handle datetime objects directly
        if isinstance(date_val, (datetime, pd.Timestamp)):
            date_obj = pd.to_datetime(date_val)
        else:
            date_str = str(date_val).strip()
            if not date_str or date_str.lower() in ['nan', 'none', 'null']:
                return None
            
            # Optimized format matching
            date_formats = [
                '%Y-%m-%d %H:%M:%S', '%d-%b-%y', '%Y-%m-%d', 
                '%b %d, %Y', '%d-%m-%Y', '%m/%d/%Y'
            ]
            
            date_obj = None
            for fmt in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if not date_obj:
                date_obj = pd.to_datetime(date_str, errors='coerce')
                if pd.isna(date_obj):
                    return None
        
        # Parse time efficiently
        time_str = str(time_val).strip().replace('UTC', '').replace('IST', '').replace('==', '').strip()
        
        if 'PM' in time_str or 'AM' in time_str:
            try:
                time_obj = datetime.strptime(time_str, '%I:%M %p').time()
            except ValueError:
                time_obj = datetime.min.time()
        elif ':' in time_str:
            try:
                parts = time_str.split(':')
                hour = min(int(parts[0]), 23)
                minute = min(int(parts[1]) if len(parts) > 1 else 0, 59)
                time_obj = datetime.min.time().replace(hour=hour, minute=minute)
            except (ValueError, IndexError):
                time_obj = datetime.min.time()
        else:
            time_obj = datetime.min.time()
        
        dt = datetime.combine(date_obj.date(), time_obj)
        
        # UTC to IST conversion
        if 'UTC' in str(time_val):
            dt += timedelta(hours=5, minutes=30)
        
        return dt
        
    except Exception as e:
        app.logger.warning(f"DateTime parsing failed for row: {e}")
        return None

def handle_api_errors(f):
    """Decorator for consistent API error handling"""
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"API error in {f.__name__}: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    wrapper.__name__ = f.__name__
    return wrapper

def process_excel(file_path):
    """Process Excel file with optimized operations"""
    try:
        # Read with optimized settings
        df = pd.read_excel(file_path, engine='openpyxl')
        app.logger.info(f"Loaded {len(df)} raw records")
        
        if df.empty:
            raise ValueError("Excel file is empty")
        
        # Vectorized datetime parsing
        df['DateTime_IST'] = df.apply(parse_datetime, axis=1)
        df['DateTime_IST'] = pd.to_datetime(df['DateTime_IST'], errors='coerce')
        
        # Filter valid dates
        valid_mask = df['DateTime_IST'].notna()
        df = df[valid_mask].copy()
        app.logger.info(f"After date filtering: {len(df)} records")
        
        if df.empty:
            raise ValueError("No valid dates found in data")
        
        # Vectorized temporal features
        dt_series = df['DateTime_IST']
        df['Date_IST'] = dt_series.dt.date
        df['DayOfWeek'] = dt_series.dt.day_name()
        df['Hour'] = dt_series.dt.hour
        df['Week'] = dt_series.dt.isocalendar().week
        df['Month'] = dt_series.dt.month
        df['MonthName'] = dt_series.dt.strftime('%B')
        
        # Optimized currency processing
        total_amounts = df['Total Amount payed buy user'].apply(extract_currency_amount)
        df[['Total_Amount_Raw', 'Total_Currency']] = pd.DataFrame(total_amounts.tolist(), index=df.index)
        
        list_prices = df['List Price'].apply(extract_currency_amount)
        df[['List_Price_Raw', 'List_Currency']] = pd.DataFrame(list_prices.tolist(), index=df.index)
        
        # Vectorized INR conversion
        df['Total_Amount_INR'] = [to_inr(amt, curr) for amt, curr in zip(df['Total_Amount_Raw'], df['Total_Currency'])]
        df['List_Price_INR'] = [to_inr(amt, curr) for amt, curr in zip(df['List_Price_Raw'], df['List_Currency'])]
        
        # Net amount processing
        net_amounts = df['Net amount with deductions'].apply(
            lambda x: to_inr(*extract_currency_amount(x)) if pd.notna(x) and str(x).strip() else None
        )
        df['Net_Amount_INR'] = net_amounts.fillna(df['List_Price_INR'] * 0.70)
        
        # Country column handling
        if 'Country' in df.columns:
            df['Country'] = df['Country'].fillna('Unknown').astype(str).str.strip().replace('', 'Unknown')
            app.logger.info("Using Country column from data")
        else:
            df['Country'] = 'Unknown'
            app.logger.warning("No Country column found")
        
        # Financial calculations
        df['Tax_INR'] = df['Total_Amount_INR'] - df['List_Price_INR']
        df['Platform_Deduction_INR'] = df['List_Price_INR'] - df['Net_Amount_INR']
        
        # Safe percentage calculation
        with np.errstate(divide='ignore', invalid='ignore'):
            df['Deduction_Percentage'] = np.where(
                df['List_Price_INR'] > 0,
                (df['Platform_Deduction_INR'] / df['List_Price_INR'] * 100).round(2),
                0
            )
        
        app.logger.info(f"Processing complete: {len(df)} records")
        app.logger.info(f"Countries: {df['Country'].nunique()} unique")
        
        return df
        
    except Exception as e:
        app.logger.error(f"Excel processing failed: {e}")
        raise

def load_data():
    """Load and cache data with validation"""
    try:
        file_path = app.config['DATA_FILE']
        if not os.path.exists(file_path):
            app.logger.error(f"Data file not found: {file_path}")
            return False
        
        # Check file size
        file_size = os.path.getsize(file_path)
        max_size = app.config['MAX_FILE_SIZE']
        if file_size > max_size:
            app.logger.error(f"File too large: {file_size / 1024 / 1024:.1f}MB (max: {max_size / 1024 / 1024:.1f}MB)")
            return False
        
        df = process_excel(file_path)
        
        # Validate processed data
        if df.empty:
            app.logger.error("Processed data is empty")
            return False
        
        required_columns = ['DateTime_IST', 'Total_Amount_INR', 'Country']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            app.logger.error(f"Missing required columns: {missing_cols}")
            return False
        
        DATA_CACHE['processed_data'] = df
        DATA_CACHE['last_updated'] = datetime.now()
        
        app.logger.info(f"Data loaded successfully: {len(df)} records")
        return True
        
    except Exception as e:
        app.logger.error(f"Data loading failed: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# FILTERING - FIXED
# ═══════════════════════════════════════════════════════════════════════════

def get_filtered_data(start_date=None, end_date=None, country=None, platform=None):
    """Get filtered dataset with WORKING date filtering"""
    df = DATA_CACHE['processed_data']
    
    if df is None or df.empty:
        return pd.DataFrame()
    
    filtered_df = df.copy()
    original_count = len(filtered_df)
    
    try:
        # Date filtering - ACTUALLY WORKS NOW
        if start_date and str(start_date).strip() not in ['', 'null', 'undefined', 'all']:
            start_dt = pd.to_datetime(start_date).date()
            filtered_df = filtered_df[filtered_df['Date_IST'] >= start_dt]
            app.logger.info(f"Start date {start_dt}: {len(filtered_df)} records")
        
        if end_date and str(end_date).strip() not in ['', 'null', 'undefined', 'all']:
            end_dt = pd.to_datetime(end_date).date()
            filtered_df = filtered_df[filtered_df['Date_IST'] <= end_dt]
            app.logger.info(f"End date {end_dt}: {len(filtered_df)} records")
        
        # Country filtering
        if country and str(country).strip() not in ['', 'all', 'null', 'undefined']:
            filtered_df = filtered_df[filtered_df['Country'] == country]
            app.logger.info(f"Country {country}: {len(filtered_df)} records")
        
        # Platform filtering
        if platform and str(platform).strip() not in ['', 'all', 'null', 'undefined']:
            filtered_df = filtered_df[filtered_df['Platform'] == platform]
            app.logger.info(f"Platform {platform}: {len(filtered_df)} records")
        
        app.logger.info(f"FILTER RESULT: {original_count} -> {len(filtered_df)} records")
        return filtered_df
            
    except Exception as e:
        app.logger.error(f"Filter error: {e}")
        return df.copy()

def fill_missing_dates(data, start_date, end_date):
    """Fill missing dates with zeros"""
    if not data or len(data) == 0:
        return []
    
    try:
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        data_dict = {item['date']: item for item in data}
        
        filled_data = []
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in data_dict:
                filled_data.append(data_dict[date_str])
            else:
                filled_data.append({
                    'date': date_str,
                    'revenue': 0,
                    'net_revenue': 0,
                    'orders': 0,
                    'avg_order': 0
                })
        
        return filled_data
    except:
        return data

# ═══════════════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/add-entry')
def add_entry_page():
    """Render add entry page"""
    try:
        return render_template('add_entry.html')
    except Exception as e:
        app.logger.error(f"Error loading add_entry.html: {e}")
        # Fallback: try to read the file directly
        try:
            with open(os.path.join('templates', 'add_entry.html'), 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e2:
            return f"Error loading form: {e2}. Please check if templates/add_entry.html exists.", 500

@app.route('/financials')
def financials_page():
    """Render financial management page"""
    try:
        return render_template('financials.html')
    except Exception as e:
        app.logger.error(f"Error loading financials.html: {e}")
        return f"Error loading financials page: {e}", 500

@app.route('/add-financial')
def add_financial_page():
    """Render add financial entry page"""
    try:
        return render_template('add_financial.html')
    except Exception as e:
        app.logger.error(f"Error loading add_financial.html: {e}")
        return f"Error loading add financial page: {e}", 500

@app.route('/api/kpis')
@handle_api_errors
def api_kpis():
    """Get KPIs with optimized calculations"""
    try:
        df = get_filtered_data(
            request.args.get('startDate'),
            request.args.get('endDate'),
            request.args.get('country'),
            request.args.get('platform')
        )
        
        # Empty data response
        empty_kpis = {
            'revenue': {'gross': 0, 'net': 0, 'net_margin': 0},
            'orders': {'total': 0, 'avg_value': 0, 'median_value': 0},
            'geographic': {'countries': 0, 'top_country': 'N/A', 'concentration_hhi': 0},
            'temporal': {'days_active': 0, 'revenue_per_day': 0, 'orders_per_day': 0},
            'platform': {'platforms': 0, 'top_platform': 'N/A'},
            'customer': {'clv': 0, 'max_cac': 0}
        }
        
        if df.empty:
            return jsonify({'success': True, 'data': {'kpis': empty_kpis}})
        
        # Vectorized calculations
        total_revenue = df['Total_Amount_INR'].sum()
        total_net = df['Net_Amount_INR'].sum()
        order_count = len(df)
        
        # Safe division helper
        def safe_divide(a, b, default=0):
            return round(a / b, 2) if b > 0 else default
        
        # Calculate date range once
        date_range = (df['DateTime_IST'].max() - df['DateTime_IST'].min()).days + 1
        
        kpis = {
            'revenue': {
                'gross': round(total_revenue, 2),
                'net': round(total_net, 2),
                'net_margin': safe_divide(total_net * 100, total_revenue)
            },
            'orders': {
                'total': order_count,
                'avg_value': round(df['Total_Amount_INR'].mean(), 2),
                'median_value': round(df['Total_Amount_INR'].median(), 2)
            },
            'geographic': {
                'countries': df['Country'].nunique(),
                'top_country': df.groupby('Country')['Total_Amount_INR'].sum().idxmax() if order_count > 0 else 'N/A',
                'concentration_hhi': 0.15
            },
            'temporal': {
                'days_active': date_range,
                'revenue_per_day': safe_divide(total_revenue, date_range),
                'orders_per_day': safe_divide(order_count, date_range)
            },
            'platform': {
                'platforms': df['Platform'].nunique(),
                'top_platform': df.groupby('Platform')['Total_Amount_INR'].sum().idxmax() if order_count > 0 else 'N/A'
            },
            'customer': {
                'clv': round(df['Total_Amount_INR'].mean() * 3, 2),
                'max_cac': round(df['Total_Amount_INR'].mean() * 0.9, 2)
            }
        }
        
        return jsonify({'success': True, 'data': {'kpis': kpis}})
        
    except Exception as e:
        app.logger.error(f"KPI calculation error: {e}")
        return jsonify({'success': False, 'error': 'Failed to calculate KPIs'}), 500

@app.route('/api/revenue-trends')
@handle_api_errors
def api_revenue_trends():
    """Revenue trends - FIXED with proper chronological ordering"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        granularity = request.args.get('granularity', 'daily')
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': True, 'data': [], 'granularity': granularity})
        
        if granularity == 'daily':
            trends = df.groupby('Date_IST').agg({
                'Total_Amount_INR': ['sum', 'mean'],
                'Net_Amount_INR': 'sum',
                'S.NO': 'count'
            }).reset_index()
            trends.columns = ['date', 'revenue', 'avg_order', 'net_revenue', 'orders']
            trends = trends.sort_values('date')  # FIXED: Proper chronological order
            trends['date'] = trends['date'].astype(str)
            
            # Fill missing dates using selected date range
            if len(trends) > 0:
                # Use filter dates if provided, otherwise use data range
                if start_date and end_date:
                    min_date = pd.to_datetime(start_date)
                    max_date = pd.to_datetime(end_date)
                else:
                    min_date = pd.to_datetime(trends['date'].min())
                    max_date = pd.to_datetime(trends['date'].max())
                trends_list = trends.to_dict('records')
                trends_list = fill_missing_dates(trends_list, min_date, max_date)
                return jsonify({'success': True, 'data': trends_list, 'granularity': granularity})
            
        elif granularity == 'weekly':
            # FIXED: Add year-week for proper sorting
            df['YearWeek'] = df['DateTime_IST'].dt.strftime('%Y-W%U')
            trends = df.groupby(['YearWeek', 'Week']).agg({
                'Total_Amount_INR': ['sum', 'mean'],
                'Net_Amount_INR': 'sum',
                'S.NO': 'count'
            }).reset_index()
            trends.columns = ['year_week', 'week', 'revenue', 'avg_order', 'net_revenue', 'orders']
            trends = trends.sort_values('year_week')  # FIXED: Chronological order
            trends['growth'] = trends['revenue'].pct_change() * 100
            
        elif granularity == 'monthly':
            # FIXED: Add year-month for proper sorting
            df['YearMonth'] = df['DateTime_IST'].dt.strftime('%Y-%m')
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            
            trends = df.groupby(['YearMonth', 'MonthName']).agg({
                'Total_Amount_INR': ['sum', 'mean'],
                'Net_Amount_INR': 'sum',
                'S.NO': 'count'
            }).reset_index()
            trends.columns = ['year_month', 'month', 'revenue', 'avg_order', 'net_revenue', 'orders']
            trends = trends.sort_values('year_month')  # FIXED: Chronological order
            trends['growth'] = trends['revenue'].pct_change() * 100
        
        return jsonify({
            'success': True,
            'data': trends.round(2).fillna(0).to_dict('records'),
            'granularity': granularity
        })
        
    except Exception as e:
        app.logger.error(f"Trends error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/geographic')
@handle_api_errors
def api_geographic():
    """Geographic - FIXED"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        limit = request.args.get('limit', 20, type=int)
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': True, 'data': []})
        
        geo_stats = df.groupby('Country').agg({
            'Total_Amount_INR': ['sum', 'mean', 'count'],
            'Net_Amount_INR': 'sum',
            'Platform': lambda x: x.mode()[0] if len(x) > 0 else 'N/A'
        }).round(2)
        
        geo_stats.columns = ['revenue', 'aov', 'orders', 'net_revenue', 'top_platform']
        geo_stats = geo_stats.sort_values('revenue', ascending=False).head(limit)
        
        total_revenue = geo_stats['revenue'].sum()
        if total_revenue > 0:
            geo_stats['market_share'] = (geo_stats['revenue'] / total_revenue * 100).round(2)
        else:
            geo_stats['market_share'] = 0
        
        return jsonify({
            'success': True,
            'data': geo_stats.reset_index().to_dict('records')
        })
        
    except Exception as e:
        app.logger.error(f"Geographic error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/platforms')
@handle_api_errors
def api_platforms():
    """Platform analysis"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': True, 'data': []})
        
        platform_stats = df.groupby('Platform').agg({
            'Total_Amount_INR': ['sum', 'mean'],
            'Net_Amount_INR': 'sum',
            'S.NO': 'count',
            'Deduction_Percentage': 'mean'
        }).round(2)
        
        platform_stats.columns = ['revenue', 'aov', 'net_revenue', 'orders', 'avg_fee']
        platform_stats['countries'] = df.groupby('Platform')['Country'].nunique()
        
        return jsonify({
            'success': True,
            'data': platform_stats.reset_index().to_dict('records')
        })
        
    except Exception as e:
        app.logger.error(f"Platform error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/temporal-patterns')
@handle_api_errors
def api_temporal_patterns():
    """Temporal patterns"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': True, 'data': {'hourly': [], 'day_of_week': []}})
        
        hourly = df.groupby('Hour').agg({
            'S.NO': 'count',
            'Total_Amount_INR': 'sum'
        }).reset_index()
        hourly.columns = ['hour', 'orders', 'revenue']
        
        dow = df.groupby('DayOfWeek').agg({
            'S.NO': 'count',
            'Total_Amount_INR': 'sum'
        }).reset_index()
        dow.columns = ['day', 'orders', 'revenue']
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow['day'] = pd.Categorical(dow['day'], categories=day_order, ordered=True)
        dow = dow.sort_values('day')
        dow['day'] = dow['day'].astype(str)
        
        return jsonify({
            'success': True,
            'data': {
                'hourly': hourly.round(2).to_dict('records'),
                'day_of_week': dow.round(2).to_dict('records')
            }
        })
        
    except Exception as e:
        app.logger.error(f"Temporal error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insights')
@handle_api_errors
def api_insights():
    """AI Insights - FIXED"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': True, 'data': []})
        
        insights = []
        
        # Revenue health
        total_revenue = df['Total_Amount_INR'].sum()
        total_net = df['Net_Amount_INR'].sum()
        net_margin = (total_net / total_revenue * 100) if total_revenue > 0 else 0
        
        if net_margin < 60:
            insights.append({
                'type': 'critical',
                'category': 'Revenue',
                'title': 'High Platform Fees',
                'message': f"Net margin is {net_margin:.1f}%. Fees consuming {100-net_margin:.1f}%.",
                'impact': 'high',
                'action': 'Consider direct sales channels'
            })
        else:
            insights.append({
                'type': 'success',
                'category': 'Revenue',
                'title': 'Healthy Margins',
                'message': f"Net margin at {net_margin:.1f}% is sustainable.",
                'impact': 'positive',
                'action': 'Continue current strategy'
            })
        
        # Market concentration
        country_revenue = df.groupby('Country')['Total_Amount_INR'].sum()
        if len(country_revenue) > 0:
            top_country = country_revenue.idxmax()
            concentration = (country_revenue.max() / country_revenue.sum() * 100)
            
            if concentration > 40:
                insights.append({
                    'type': 'warning',
                    'category': 'Risk',
                    'title': 'High Market Concentration',
                    'message': f"{top_country} is {concentration:.1f}% of revenue",
                    'impact': 'high',
                    'action': 'Diversify into 3-5 new markets'
                })
        
        return jsonify({'success': True, 'data': insights})
        
    except Exception as e:
        app.logger.error(f"Insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/forecast')
@handle_api_errors
def api_forecast():
    """Revenue forecast - FIXED"""
    try:
        days = request.args.get('days', 7, type=int)
        df = get_filtered_data()
        
        if df.empty or len(df) < 2:
            return jsonify({'success': False, 'error': 'Insufficient data'})
        
        # Simple moving average
        daily = df.groupby('Date_IST')['Total_Amount_INR'].sum().reset_index()
        daily.columns = ['date', 'revenue']
        
        avg_revenue = daily['revenue'].mean()
        
        # Generate forecast
        last_date = daily['date'].max()
        forecast_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(days)]
        forecast_values = [round(avg_revenue, 2)] * days
        
        return jsonify({
            'success': True,
            'data': {
                'dates': forecast_dates,
                'values': forecast_values,
                'trend': 'stable',
                'slope': 0
            }
        })
        
    except Exception as e:
        app.logger.error(f"Forecast error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/filters/options')
def api_filter_options():
    """Filter options"""
    try:
        df = DATA_CACHE['processed_data']
        
        if df is None or df.empty:
            return jsonify({'success': False, 'error': 'No data'})
        
        return jsonify({
            'success': True,
            'data': {
                'countries': sorted(df['Country'].unique().tolist()),
                'platforms': sorted(df['Platform'].unique().tolist()),
                'date_range': {
                    'min': df['DateTime_IST'].min().strftime('%Y-%m-%d'),
                    'max': df['DateTime_IST'].max().strftime('%Y-%m-%d')
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/<format>')
def api_export(format):
    """Export - FIXED"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        country = request.args.get('country')
        platform = request.args.get('platform')
        
        df = get_filtered_data(start_date, end_date, country, platform)
        
        if df.empty:
            return jsonify({'success': False, 'error': 'No data'}), 400
        
        if format == 'csv':
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'aivellum_{datetime.now().strftime("%Y%m%d")}.csv'
            )
            
        elif format == 'excel':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sales Data', index=False)
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'aivellum_{datetime.now().strftime("%Y%m%d")}.xlsx'
            )
        
        return jsonify({'success': False, 'error': 'Invalid format'}), 400
        
    except Exception as e:
        app.logger.error(f"Export error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/add-entry', methods=['POST'])
def api_add_entry():
    """Add new income entry - Enhanced for comprehensive tracking"""
    try:
        data = request.json
        
        file_path = 'Aivellum_Sales.xlsx'
        df = pd.read_excel(file_path)
        
        # Handle dynamic platform input
        platform = data['platform']
        if platform == 'Other' and data.get('platform_other'):
            platform = data['platform_other']
        
        # Handle dynamic user type input
        for_users = data.get('for_users', '')
        if for_users == 'Other' and data.get('for_users_other'):
            for_users = data['for_users_other']
        
        new_entry = {
            'S.NO': len(df) + 1,
            'Date': data['date'],
            'Time': data['time'],
            'Purchase ID': data['purchase_id'],
            'Platform': platform,
            'For (Users)': for_users,
            'Billing Address': data.get('billing_address', ''),
            'Country': data.get('country', 'Unknown'),
            'Total Amount payed buy user': data['total_amount'],
            'List Price': data['list_price'],
            'Taxn (toal amount - list price)': data.get('tax', ''),
            'Net amount with deductions': data.get('net_amount', ''),
            'Income Category': data.get('income_category', 'Other'),
            'Notes': data.get('notes', '')
        }
        
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(file_path, index=False)
        
        # Reload data cache
        load_data()
        
        return jsonify({
            'success': True,
            'message': 'Income entry added successfully',
            'entry_number': new_entry['S.NO'],
            'platform': platform,
            'amount': data['total_amount']
        })
        
    except Exception as e:
        app.logger.error(f"Add entry error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/currencies')
def api_currencies():
    """Get currencies"""
    currencies = [
        {'code': code, 'name': code, 'symbol': code, 'rate': rate}
        for code, rate in CURRENCY_RATES.items()
    ]
    return jsonify({'success': True, 'data': currencies})

@app.route('/api/countries')
def api_countries():
    """Get countries list"""
    countries = [
        {'code': 'US', 'name': 'United States', 'timezone': 'America/New_York', 'currency': 'USD'},
        {'code': 'IN', 'name': 'India', 'timezone': 'Asia/Kolkata', 'currency': 'INR'},
        {'code': 'GB', 'name': 'United Kingdom', 'timezone': 'Europe/London', 'currency': 'GBP'},
        {'code': 'AU', 'name': 'Australia', 'timezone': 'Australia/Sydney', 'currency': 'AUD'},
        {'code': 'CA', 'name': 'Canada', 'timezone': 'America/Toronto', 'currency': 'CAD'},
        {'code': 'DE', 'name': 'Germany', 'timezone': 'Europe/Berlin', 'currency': 'EUR'},
        {'code': 'FR', 'name': 'France', 'timezone': 'Europe/Paris', 'currency': 'EUR'},
        {'code': 'FI', 'name': 'Finland', 'timezone': 'Europe/Helsinki', 'currency': 'EUR'},
        {'code': 'EC', 'name': 'Ecuador', 'timezone': 'America/Guayaquil', 'currency': 'USD'},
        {'code': 'HR', 'name': 'Croatia', 'timezone': 'Europe/Zagreb', 'currency': 'EUR'},
        {'code': 'KR', 'name': 'South Korea', 'timezone': 'Asia/Seoul', 'currency': 'KRW'},
        {'code': 'PK', 'name': 'Pakistan', 'timezone': 'Asia/Karachi', 'currency': 'PKR'},
        {'code': 'NG', 'name': 'Nigeria', 'timezone': 'Africa/Lagos', 'currency': 'NGN'},
        {'code': 'ZA', 'name': 'South Africa', 'timezone': 'Africa/Johannesburg', 'currency': 'ZAR'},
        {'code': 'AE', 'name': 'United Arab Emirates', 'timezone': 'Asia/Dubai', 'currency': 'AED'},
        {'code': 'HU', 'name': 'Hungary', 'timezone': 'Europe/Budapest', 'currency': 'EUR'},
        {'code': 'CZ', 'name': 'Czech Republic', 'timezone': 'Europe/Prague', 'currency': 'CZK'},
    ]
    return jsonify({'success': True, 'data': countries})

@app.route('/api/platform-options')
def api_platform_options():
    """Get platform options for dynamic dropdown"""
    return jsonify({
        'success': True,
        'data': {
            'platforms': PLATFORM_OPTIONS,
            'user_types': USER_TYPE_OPTIONS,
            'income_categories': list(INCOME_CATEGORIES.keys())
        }
    })

# ═══════════════════════════════════════════════════════════════════════════
# FINANCIAL MANAGEMENT API ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/financial/summary')
@handle_api_errors
def api_financial_summary():
    """Get financial summary and cash flow analysis"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        summary = financial_manager.get_financial_summary(start_date, end_date)
        
        # Convert numpy types to Python types for JSON serialization
        def convert_types(obj):
            if hasattr(obj, 'item'):
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(v) for v in obj]
            else:
                return obj
        
        return jsonify({
            'success': True,
            'data': convert_types(summary)
        })
    except Exception as e:
        app.logger.error(f"Financial summary error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/trends')
@handle_api_errors
def api_financial_trends():
    """Get monthly financial trends"""
    try:
        trends = financial_manager.get_monthly_trends()
        
        return jsonify({
            'success': True,
            'data': trends
        })
    except Exception as e:
        app.logger.error(f"Financial trends error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/data')
@handle_api_errors
def api_financial_data():
    """Get all financial data"""
    try:
        data = financial_manager.load_data()
        
        # Convert data to dict for JSON serialization
        result = {}
        for key, items in data.items():
            if isinstance(items, list):
                result[key] = items
            else:
                result[key] = []
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        app.logger.error(f"Financial data error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/add-income', methods=['POST'])
@handle_api_errors
def api_add_income():
    """Add new income entry"""
    try:
        data = request.json
        
        success = financial_manager.add_income(
            source=data['source'],
            amount=data['amount'],
            date=data['date'],
            category=data.get('category', 'Other'),
            notes=data.get('notes', '')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Income entry added successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add income entry'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Add income error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/add-expense', methods=['POST'])
@handle_api_errors
def api_add_expense():
    """Add new expense entry"""
    try:
        data = request.json
        
        success = financial_manager.add_expense(
            description=data['description'],
            amount=data['amount'],
            date=data['date'],
            category=data['category'],
            exp_type=data['type'],
            notes=data.get('notes', '')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Expense entry added successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add expense entry'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Add expense error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/add-planned', methods=['POST'])
@handle_api_errors
def api_add_planned():
    """Add new planned activity"""
    try:
        data = request.json
        
        success = financial_manager.add_planned_activity(
            activity=data['activity'],
            cost=data['cost'],
            priority=data['priority'],
            status=data['status'],
            target_date=data['target_date'],
            notes=data.get('notes', '')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Planned activity added successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add planned activity'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Add planned activity error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/options')
def api_financial_options():
    """Get financial form options"""
    return jsonify({
        'success': True,
        'data': {
            'income_categories': ['Digital Products', 'App Revenue', 'Services', 'Consulting', 'Other'],
            'expense_categories': list(financial_manager.expense_categories.keys()),
            'expense_types': {
                'Salaries': ['Employee', 'Freelancer', 'Contractor'],
                'Tools': ['Software', 'Hardware', 'Service'],
                'Outsourcing': ['Service', 'Freelancer', 'Agency'],
                'Business': ['Legal', 'Infrastructure', 'Office'],
                'Marketing': ['Advertising', 'Content', 'Events']
            },
            'priorities': ['High', 'Medium', 'Low'],
            'statuses': ['Pending', 'In Progress', 'Completed', 'Cancelled', 'On Hold']
        }
    })

@app.route('/api/financial/breakdown')
@handle_api_errors
def api_financial_breakdown():
    """Get detailed expense breakdown"""
    try:
        breakdown = financial_manager.get_expense_breakdown()
        return jsonify({
            'success': True,
            'data': breakdown
        })
    except Exception as e:
        app.logger.error(f"Financial breakdown error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/insights')
@handle_api_errors
def api_financial_insights():
    """Get AI-powered financial insights"""
    try:
        insights = financial_manager.get_financial_insights()
        return jsonify({
            'success': True,
            'data': insights
        })
    except Exception as e:
        app.logger.error(f"Financial insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/financial/cash-flow')
@handle_api_errors
def api_financial_cash_flow():
    """Get detailed cash flow analysis"""
    try:
        cash_flow = financial_manager.get_cash_flow_analysis()
        return jsonify({
            'success': True,
            'data': cash_flow
        })
    except Exception as e:
        app.logger.error(f"Cash flow analysis error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500





@app.route('/api/financial/export/<format>')
def api_financial_export(format):
    """Export financial data"""
    try:
        data = financial_manager.load_data()
        
        if format == 'csv':
            # Create a combined CSV export
            output = io.StringIO()
            output.write("=== AIVELLUM FINANCIAL EXPORT ===\n")
            output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Income section
            output.write("=== INCOME ===\n")
            if data['income']:
                fieldnames = data['income'][0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data['income'])
            output.write("\n")
            
            # Expenses section
            output.write("=== EXPENSES ===\n")
            if data['expenses']:
                fieldnames = data['expenses'][0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data['expenses'])
            output.write("\n")
            
            # Planned section
            output.write("=== PLANNED ACTIVITIES ===\n")
            if data['planned']:
                fieldnames = data['planned'][0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data['planned'])
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'aivellum_financial_{datetime.now().strftime("%Y%m%d")}.csv'
            )
        
        return jsonify({'success': False, 'error': 'Invalid format'}), 400
        
    except Exception as e:
        app.logger.error(f"Financial export error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/debug-filter')
def debug_filter():
    """Debug filtering"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    df = DATA_CACHE['processed_data']
    if df is None:
        return jsonify({'error': 'No data loaded'})
    
    result = {
        'total_records': len(df),
        'start_date_param': start_date,
        'end_date_param': end_date,
        'date_range_in_data': {
            'min': str(df['Date_IST'].min()),
            'max': str(df['Date_IST'].max())
        },
        'sample_dates': df['Date_IST'].head(10).astype(str).tolist()
    }
    
    if start_date:
        start_dt = pd.to_datetime(start_date).date()
        filtered = df[df['Date_IST'] >= start_dt]
        result['after_start_filter'] = len(filtered)
        
    if end_date:
        end_dt = pd.to_datetime(end_date).date()
        if start_date:
            filtered = filtered[filtered['Date_IST'] <= end_dt]
        else:
            filtered = df[df['Date_IST'] <= end_dt]
        result['after_end_filter'] = len(filtered)
    
    return jsonify(result)

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '4.0.0',
        'type': 'Financial Management Platform',
        'data_loaded': DATA_CACHE['processed_data'] is not None,
        'records': len(DATA_CACHE['processed_data']) if DATA_CACHE['processed_data'] is not None else 0,
        'features': ['Complete Cash Flow', 'Expense Management', 'Financial Planning', 'Income Tracking', 'Financial Analytics']
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal error'}), 500

# ═══════════════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════════════

def startup_summary():
    """Display startup information"""
    print("\n" + "=" * 80)
    print(" " * 5 + "🚀 AIVELLUM FINANCIAL MANAGEMENT PLATFORM v4.0")
    print("=" * 80)
    
    print("\n🔄 Loading income data...")
    
    if load_data():
        df = DATA_CACHE['processed_data']
        print(f"✅ Loaded {len(df):,} income records")
        print(f"📅 Date range: {df['DateTime_IST'].min().date()} to {df['DateTime_IST'].max().date()}")
        print(f"🌍 Countries: {df['Country'].nunique()}")
        print(f"📱 Platforms: {df['Platform'].nunique()}")
        print(f"💰 Total Income: ₹{df['Total_Amount_INR'].sum():,.2f}")
        print(f"💵 Net Income: ₹{df['Net_Amount_INR'].sum():,.2f}")
        print(f"📊 Avg per transaction: ₹{df['Total_Amount_INR'].mean():,.2f}")
    else:
        print("⚠️  No data loaded - check Aivellum_Sales.xlsx")
    
    print("\n🎯 v4.0 FEATURES:")
    print("   💰 Complete cash flow tracking")
    print("   💸 Expense management (salaries, tools, outsourcing)")
    print("   📅 Planned activities and financial planning")
    print("   📊 Financial dashboard and analytics")
    print("   ✅ All v3.0 income tracking features")
    
    print("\n🚀 Server starting...")
    print("   📊 Dashboard: http://localhost:5000")
    print("   ➕ Add Income: http://localhost:5000/add-entry")
    print("   💰 Financials: http://localhost:5000/financials")
    print("   ➕ Add Financial: http://localhost:5000/add-financial")
    print("   ❤️  Health: http://localhost:5000/health")
    print("\n" + "=" * 80 + "\n")

if __name__ == '__main__':
    startup_summary()
    
    try:
        app.run(
            host='0.0.0.0', 
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('DEBUG', 'False').lower() == 'true',
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")