# Import necessary libraries
import pandas as pd                    # For data manipulation
import matplotlib.pyplot as plt        # For plotting
import seaborn as sns                  # For advanced plotting styles
import numpy as np                     # For numerical operations
from sklearn.linear_model import LinearRegression        # Linear regression model
from sklearn.preprocessing import PolynomialFeatures      # For polynomial regression features
from sklearn.ensemble import RandomForestRegressor        # Random forest regression model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score  # Model evaluation metrics
import rasterio                        # For raster data processing
import geopandas as gpd                # For handling vector spatial data (shapefiles)
import matplotlib.colors as mcolors   # For colormap handling in plots
from rasterio.mask import mask         # To mask raster by vector geometries

# --- Time Series Analysis using Pandas, Seaborn, and Matplotlib ---

# Load NDVI data from CSV file
file_path = r"C:\Users\beat1234.stu\OneDrive - UBC\Desktop\MGEM WINTER TERM 2\FCOR 599\Satellite Dataset\ndvi_summary.csv"
ndvi_data = pd.read_csv(file_path)

# Convert 'Year' column to datetime format for proper time series plotting
ndvi_data['Year'] = pd.to_datetime(ndvi_data['Year'], format='%Y')

# Set Seaborn style for clean and modern plots
sns.set(style="whitegrid", palette="muted")

# Create a figure for NDVI trend visualization
plt.figure(figsize=(14,7))

# Plot NDVI trends over years for each site with markers and line styles
sns.lineplot(x=ndvi_data["Year"], y=ndvi_data["Mean_NDVI"], hue=ndvi_data["Site"], style=ndvi_data["Site"],
             markers=True, dashes=False, linewidth=2.5, markersize=8, marker='o')

# Customize axes labels and title with font size and color
plt.xlabel("Year", fontsize=14, fontweight='normal', color='black')
plt.ylabel("Mean NDVI", fontsize=14, fontweight='normal', color='black')
plt.title("NDVI Trends (2014-2024)", fontsize=16, fontweight='bold', color='black')

# Customize legend appearance and position outside plot area
plt.legend(title='Site', title_fontsize=12, fontsize=11, loc='upper left', bbox_to_anchor=(1, 1))

# Rotate x-axis labels for better readability and set label style
plt.xticks(rotation=45, fontsize=12, color='black')
plt.yticks(fontsize=12, color='black')

# Remove gridlines for a cleaner look
plt.grid(False)

# Adjust layout to avoid clipping of labels and legends
plt.tight_layout()

# Display the plot
plt.show()

# --- Regression Models for NDVI Prediction ---

# Filter dataset to the project site only
project_data = ndvi_data[ndvi_data['Site'] == 'Project']

# Prepare feature (Year) and target (Mean NDVI) variables for modeling
X = np.array(project_data["Year"].dt.year).reshape(-1, 1)  # Convert datetime to numeric year
y = np.array(project_data["Mean_NDVI"])

# Linear Regression Model
linear_model = LinearRegression()
linear_model.fit(X, y)

# Polynomial Regression Model (degree 2)
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)

# Random Forest Regression Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Define future years for prediction (2025 to 2030)
future_years = np.array(range(2025, 2031)).reshape(-1, 1)

# Generate predictions using all three models
linear_predictions = linear_model.predict(future_years)
future_years_poly = poly_features.transform(future_years)
poly_predictions = poly_model.predict(future_years_poly)
rf_predictions = rf_model.predict(future_years)

# Model evaluation on training data
y_pred_linear = linear_model.predict(X)
y_pred_poly = poly_model.predict(X_poly)
y_pred_rf = rf_model.predict(X)

# Print evaluation metrics for each model
print("Linear Regression - R²:", r2_score(y, y_pred_linear))
print("Linear Regression - MAE:", mean_absolute_error(y, y_pred_linear))
print("Linear Regression - RMSE:", np.sqrt(mean_squared_error(y, y_pred_linear)))

print("Polynomial Regression - R²:", r2_score(y, y_pred_poly))
print("Polynomial Regression - MAE:", mean_absolute_error(y, y_pred_poly))
print("Polynomial Regression - RMSE:", np.sqrt(mean_squared_error(y, y_pred_poly)))

print("Random Forest - R²:", r2_score(y, y_pred_rf))
print("Random Forest - MAE:", mean_absolute_error(y, y_pred_rf))
print("Random Forest - RMSE:", np.sqrt(mean_squared_error(y, y_pred_rf)))

# Print future NDVI predictions for each model
print("Predicted NDVI for 2025-2030 (Linear Regression):", linear_predictions)
print("Predicted NDVI for 2025-2030 (Polynomial Regression):", poly_predictions)
print("Predicted NDVI for 2025-2030 (Random Forest):", rf_predictions)

# --- Plot actual NDVI data and model predictions ---

plt.figure(figsize=(10, 6))

# Scatter plot of actual NDVI values
plt.scatter(X, y, color='black', label='Actual NDVI', marker='o')

# Plot predictions of each model on training data
plt.plot(X, y_pred_linear, color='blue', label='Linear Regression', linewidth=2)
plt.plot(X, y_pred_poly, color='green', label='Polynomial Regression (degree=2)', linewidth=2)
plt.plot(X, y_pred_rf, color='red', label='Random Forest', linewidth=2)

# Plot future predictions with dashed lines and markers
plt.plot(future_years, linear_predictions, color='blue', linestyle='--', label='Linear Regression (Future)', marker='x')
plt.plot(future_years, poly_predictions, color='green', linestyle='--', label='Polynomial Regression (Future)', marker='x')
plt.plot(future_years, rf_predictions, color='red', linestyle='--', label='Random Forest (Future)', marker='x')

# Add axis labels and title
plt.xlabel("Year")
plt.ylabel("Mean NDVI")
plt.title("NDVI Prediction with Linear, Polynomial, and Random Forest Regression")
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot
plt.show()

# --- Raster Data Processing and Visualization ---

# Define file paths for raster and shapefile data
carbon_stock_path = r"C:\Users\beat1234.stu\OneDrive - UBC\Desktop\MGEM WINTER TERM 2\FCOR 599\Satellite Dataset\MGEM_Data (1)\MGEM_Data\Chloris\area_1\stock_30m_2022.tif"
shapefile_path = r"C:\Users\beat1234.stu\OneDrive - UBC\Desktop\MGEM WINTER TERM 2\GEM 530\Term Project\Boundary.shp"

# Function to read a raster file and handle NoData values
def read_raster(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1).astype(float)  # Read first band as float
        no_data_value = src.nodata
        data[data == no_data_value] = np.nan  # Replace NoData with NaN
        transform = src.transform
        crs = src.crs
    return data, transform, crs

# Read carbon stock raster data
carbon_stock, carbon_transform, carbon_crs = read_raster(carbon_stock_path)

# Read shapefile using geopandas
shapefile = gpd.read_file(shapefile_path)

# Reproject shapefile to match raster CRS if needed
if shapefile.crs != carbon_crs:
    shapefile = shapefile.to_crs(crs=carbon_crs)

# Mask raster data with shapefile geometry to crop area of interest
with rasterio.open(carbon_stock_path) as src:
    geometry = [shapefile.geometry.unary_union]  # Combine geometries
    out_image, out_transform = mask(src, geometry, crop=True)
    out_image = out_image[0].astype(float)  # First band only
    out_image[out_image == src.nodata] = np.nan  # Mask NoData

# Define classification bins for carbon stock categories
bins = [0, 10, 30, 50, 80, np.nanmax(out_image)]
labels = [1, 2, 3, 4, 5]  # Category labels

# Categorize carbon stock values using bins
carbon_stock_categorized = np.digitize(out_image, bins, right=True)

# Mask areas with NaN to avoid plotting them
carbon_stock_categorized = np.ma.masked_where(np.isnan(out_image), carbon_stock_categorized)

# Define discrete color map for categories
cmap = mcolors.ListedColormap(["red", "darkorange", "yellow", "chartreuse", "darkgreen"])
bounds = [1, 2, 3, 4, 5, 6]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Plot categorized carbon stock raster
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(carbon_stock_categorized, cmap=cmap, norm=norm, interpolation="nearest")

# Add title and hide axes
ax.set_title("Categorized Carbon Stock (2022) - Project Site", fontsize=14, fontweight="bold")
ax.axis("off")

# Add colorbar with category labels
cbar = fig.colorbar(im, ax=ax, orientation="vertical", fraction=0.03, pad=0.04, ticks=[1, 2, 3, 4, 5])
cbar.set_label("Carbon Stock Category", fontsize=12, fontweight="bold")
cbar.set_ticks([1.5, 2.5, 3.5, 4.5, 5.5])
cbar.set_ticklabels(["Very Low", "Low", "Medium", "High", "Very High"])

# Show the plot
plt.show()
