# Aivellum Analytics Platform v2.3

A Flask-based sales analytics dashboard with real-time data processing and visualization.

## Features

- 📊 Real-time sales analytics and KPIs
- 🌍 Geographic revenue analysis
- 📈 Revenue forecasting
- 💱 Multi-currency support (80+ currencies)
- 🔍 Advanced filtering and date range selection
- 📤 Data export (CSV/Excel)
- ➕ Add new sales entries
- 🚀 Optimized performance with caching

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your data:**
   - Place your Excel file as `Aivellum_Sales.xlsx` in the root directory
   - Ensure it has columns: Date, Time, Country, Total Amount, List Price, etc.

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the dashboard:**
   - Dashboard: http://localhost:5000
   - Add Entry: http://localhost:5000/add-entry
   - Health Check: http://localhost:5000/health

## Configuration

Set environment variables:
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Your secret key for production
- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (default: False)

## API Endpoints

- `GET /api/kpis` - Key performance indicators
- `GET /api/revenue-trends` - Revenue trends over time
- `GET /api/geographic` - Geographic analysis
- `GET /api/platforms` - Platform performance
- `GET /api/insights` - AI-generated insights
- `GET /api/forecast` - Revenue forecasting
- `POST /api/add-entry` - Add new sales entry

## Data Requirements

Your Excel file should contain these columns:
- Date, Time
- Country
- Total Amount payed buy user
- List Price
- Net amount with deductions
- Platform
- Purchase ID

## Performance Optimizations

- ✅ LRU caching for currency conversions
- ✅ Vectorized pandas operations
- ✅ Optimized filtering with boolean masks
- ✅ Error handling decorators
- ✅ Efficient datetime parsing
- ✅ Memory-efficient data processing

## Version History

- **v2.3**: Country column fix, performance optimizations
- **v2.2**: Enhanced error handling, better date parsing
- **v2.1**: Multi-currency support, geographic analysis
- **v2.0**: Complete rewrite with Flask

## Support

For issues or questions, check the logs in the `logs/` directory.