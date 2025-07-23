# NDVI Time Series & Carbon Stock Analysis

This project performs **time-series analysis, regression modeling, and raster-based carbon stock classification** using satellite-derived NDVI and biomass data for a forest carbon assessment project.

---

## **Features**

1. **NDVI Time Series Analysis**
   - Visualizes NDVI trends from 2014–2024 by site.
   - Uses **Seaborn** and **Matplotlib** for clean time series plots.

2. **Regression Models for NDVI Prediction**
   - Implements:
     - Linear Regression
     - Polynomial Regression (degree 2)
     - Random Forest Regression
   - Evaluates models with:
     - R²
     - MAE
     - RMSE
   - Predicts future NDVI (2025–2030) for project site.

3. **Raster Data Processing & Carbon Stock Classification**
   - Reads raster (GeoTIFF) carbon stock data.
   - Clips raster to project boundary using shapefile.
   - Classifies carbon stock into **5 discrete categories**:
     - Very Low
     - Low
     - Medium
     - High
     - Very High
   - Visualizes categorized carbon stock with custom colormap.

---

## **Requirements**

Install the following Python libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn rasterio geopandas
```

---

## **Input Data**

### 1. NDVI Data (CSV)
- File: `ndvi_summary.csv`
- Columns:
  - `Year` (YYYY)
  - `Site` (e.g., Project, Control)
  - `Mean_NDVI` (float)

### 2. Carbon Stock Data (Raster)
- File: `stock_30m_2022.tif`
- Format: GeoTIFF (biomass or carbon stock in Mg/ha)

### 3. Project Boundary (Shapefile)
- File: `Boundary.shp`
- Used to clip raster to project area.

---

## **Workflow**

1. **NDVI Time Series Plot**
   - Converts year to datetime.
   - Plots trends for each site using Seaborn.

2. **Regression Modeling**
   - Filters data for project site.
   - Trains Linear, Polynomial, and Random Forest regressors.
   - Predicts NDVI for 2025–2030.
   - Plots actual vs predicted NDVI.

3. **Carbon Stock Classification**
   - Reads raster and shapefile.
   - Clips raster to project boundary.
   - Categorizes carbon stock into bins.
   - Visualizes with color-coded categories.

---

## **Outputs**

- **NDVI Trend Plot (2014–2024)**
- **Regression Predictions (2025–2030)**
- **Carbon Stock Classified Map (2022)**

---

## **Usage**

1. Update file paths in the script:
```python
file_path = r"C:\path\to\ndvi_summary.csv"
carbon_stock_path = r"C:\path\to\stock_30m_2022.tif"
shapefile_path = r"C:\path\to\Boundary.shp"
```

2. Run the script:
```bash
python analysis.py
```

---

## **Example Output**

## **Screenshots**

### NDVI Trend Plot
![NDVI Trend](https://github.com/Bee-pixel-bo/carbon-stock-forecasting/blob/main/Screenshot%202025-07-23%20101702.png)

### Regression Model Predictions
![Regression Predictions](https://github.com/Bee-pixel-bo/carbon-stock-forecasting/blob/main/Screenshot%202025-07-23%20101639.png)

### Carbon Stock Categorization
![Carbon Stock Map](https://github.com/Bee-pixel-bo/carbon-stock-forecasting/blob/main/Screenshot%202025-07-23%20101722.png)

---

## **Author**

Beatrice Somuah – MGEM Program, UBC
