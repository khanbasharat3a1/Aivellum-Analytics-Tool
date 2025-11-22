# Aivellum Income Stream Tracker v3.0

A comprehensive Flask-based income tracking platform for monitoring all revenue streams including app sales, promotions, services, and more.

## 🎆 Major Improvements in v3.0

### ✅ FIXED Issues
- **Date Filtering**: Start and end date filters now work properly
- **Trends Ordering**: Monthly/weekly trends display in correct chronological order
- **Dynamic Inputs**: Platform and user type dropdowns with "Other" option and custom text input

### 🚀 New Features
- **Comprehensive Income Tracking**: Track all income sources (apps, promotions, consulting, etc.)
- **Income Categories**: Organize revenue by type (App Sales, Digital Products, Services, etc.)
- **Enhanced Analytics**: Better insights for diverse income streams
- **Improved UX**: More intuitive interface for income management

## 🎯 Core Features

- 💰 Multi-source income tracking and analytics
- 🌍 Geographic income analysis
- 📈 Income forecasting and trends
- 💱 Multi-currency support (80+ currencies)
- 🔍 Advanced filtering (FIXED date ranges)
- 📤 Data export (CSV/Excel)
- ➕ Add income entries with dynamic inputs
- 🚀 Optimized performance with caching

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your income data:**
   - Place your Excel file as `Aivellum_Sales.xlsx` in the root directory
   - Required columns: Date, Time, Country, Platform, Total Amount, List Price, etc.
   - Supports all income types: app sales, promotions, services, consulting

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the platform:**
   - 💰 Income Dashboard: http://localhost:5000
   - ➕ Add Income Entry: http://localhost:5000/add-entry
   - ❤️ Health Check: http://localhost:5000/health

## Configuration

Set environment variables:
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Your secret key for production
- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (default: False)

## 🔌 API Endpoints

- `GET /api/kpis` - Income performance indicators
- `GET /api/revenue-trends` - Income trends over time (FIXED ordering)
- `GET /api/geographic` - Geographic income analysis
- `GET /api/platforms` - Income source performance
- `GET /api/insights` - AI-generated income insights
- `GET /api/forecast` - Income forecasting
- `GET /api/platform-options` - Dynamic platform/user options
- `POST /api/add-entry` - Add new income entry (enhanced)

## 📁 Data Requirements

Your Excel file should contain these columns:
- **Date, Time** - Transaction timestamp
- **Country** - Income source country
- **Platform** - Income source (Play Store, Gumroad, Direct, etc.)
- **Total Amount payed buy user** - Gross income amount
- **List Price** - Base price/rate
- **Net amount with deductions** - Final amount after fees
- **Purchase ID** - Transaction/reference ID
- **Income Category** - Type of income (optional)
- **For (Users)** - Target audience (optional)

### 💰 Supported Income Types
- **App Sales**: Play Store, App Store, direct sales
- **Digital Products**: Gumroad, Stripe, PayPal
- **Promotions**: Affiliate marketing, sponsorships
- **Services**: Consulting, development, design
- **Subscriptions**: Monthly, annual, lifetime
- **Other**: Any custom income source

## ⚡ Performance Optimizations

- ✅ LRU caching for currency conversions
- ✅ Vectorized pandas operations
- ✅ FIXED date filtering with proper boolean masks
- ✅ Error handling decorators
- ✅ Efficient datetime parsing
- ✅ Memory-efficient data processing
- ✅ Optimized trend calculations with chronological sorting

## 📅 Version History

- **v3.0**: 🎆 **MAJOR UPGRADE** - Comprehensive income tracker
  - ✅ FIXED date filtering (start/end dates work properly)
  - ✅ FIXED trends chronological ordering
  - ✅ Dynamic platform/user inputs with "Other" option
  - ✅ Income categories and enhanced tracking
  - ✅ Better UX and comprehensive analytics
- **v2.3**: Country column fix, performance optimizations
- **v2.2**: Enhanced error handling, better date parsing
- **v2.1**: Multi-currency support, geographic analysis
- **v2.0**: Complete rewrite with Flask

## 🎯 What's New in v3.0

### 🔧 Fixed Issues
1. **Date Filtering**: Previously broken start/end date filters now work correctly
2. **Trends Display**: Monthly trends now show in proper chronological order (Oct before Nov)
3. **Form Inputs**: Platform and user dropdowns now support custom "Other" entries

### 🎆 New Features
1. **Income Categories**: Organize revenue by type (apps, promotions, services)
2. **Dynamic Inputs**: Smart dropdowns that expand when "Other" is selected
3. **Enhanced Analytics**: Better insights for diverse income streams
4. **Improved Interface**: More intuitive design for income management

## 📞 Support

For issues or questions:
1. Check the logs in the `logs/` directory
2. Verify your Excel file format matches requirements
3. Ensure all required columns are present
4. Test with the health check endpoint: `/health`

## 📝 Notes

- All major filtering and display issues from v2.x have been resolved
- The platform now supports comprehensive income tracking beyond just app sales
- Dynamic form inputs make it easy to add new income sources
- Chronological ordering ensures trends are displayed correctly