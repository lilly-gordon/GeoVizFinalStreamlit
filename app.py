import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap

st.title("CRC MSAVI2 2011 and 2016 Greenness Viewer")

# ---------------------------------------------------
# 1) Load MASVI2 TIFF (relative path is cloud safe)
# ---------------------------------------------------
# Paths to your local GeoTIFFs
tif_2011 = "data/msavi2_2011.tif"
tif_2016 = "data/msavi2_2016.tif"

img_2011 = Image.open(tif_2011)
arr_2011 = np.array(img_2011)

img_2016 = Image.open(tif_2016)
arr_2016 = np.array(img_2016)

# ---------------------------------------------------
# 2) Geospatial Bounds
# ---------------------------------------------------
left  = -109.639353
right = -109.628493
bottom = 38.262410
top    = 38.268114

bounds = [[bottom, left], [top, right]]

# ---------------------------------------------------
# 3) NDVI Breaks + Colors
# ---------------------------------------------------
ndvi_breaks = [-1.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]

msavi2_colors = [
    '#FFFFFF',
    '#CE7E45',
    '#FCD163',
    '#99B718',
    '#66A000',
    '#207401',
    '#056201',
    '#004C00',
    '#023B01',
    '#012E01'
]

# ---------------------------------------------------
# 4) Build Leafmap map
# ---------------------------------------------------
m = leafmap.Map(center=((top+bottom)/2, (left+right)/2), zoom=15)

# MSAVI2 colormap
colormap = msavi2_colors  

# Create the split map
m.split_map(
    left_layer=tif_2011,
    right_layer=tif_2016,
    left_label="MSAVI2 2011",
    right_label="MSAVI2 2016",
    colormap=colormap,
    vmin=-1,
    vmax=1
)


# ---------------------------------------------------
# 5) Add Legend
# ---------------------------------------------------
legend_dict = {
    "No vegetation (≤ 0.0)": "#FFFFFF",
    "0.0 – 0.1": "#CE7E45",
    "0.1 – 0.2": "#FCD163",
    "0.2 – 0.3": "#99B718",
    "0.3 – 0.4": "#66A000",
    "0.4 – 0.5": "#207401",
    "0.5 – 0.6": "#056201",
    "0.6 – 0.7": "#004C00",
    "0.7 – 0.8": "#023B01",
    "0.8 – 1.0": "#012E01",
}

m.add_legend(title="MSAVI2", legend_dict=legend_dict)

m

# ---------------------------------------------------
# 6) Display in Streamlit
# ---------------------------------------------------
m.to_streamlit(height=500)


# ---------------------------------------------------
# 7) Histograms
# ---------------------------------------------------
st.subheader("MSAVI2 Histograms: 2011 vs 2016")

# Create two side-by-side histogram plots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ----------------------------
# Histogram for 2011
# ----------------------------
axes[0].hist(arr_2011[np.isfinite(arr_2011)], bins=50, 
             color="#1f77b4", edgecolor="black")
axes[0].set_title("MSAVI2 Histogram - 2011", fontweight="bold")
axes[0].set_xlabel("MSAVI2")
axes[0].set_ylabel("Pixel Count")
axes[0].grid(alpha=0.3)

# ----------------------------
# Histogram for 2016
# ----------------------------
axes[1].hist(arr_2016[np.isfinite(arr_2016)], bins=50, 
             color="#d62728", edgecolor="black")
axes[1].set_title("MSAVI2 Histogram - 2016", fontweight="bold")
axes[1].set_xlabel("MSAVI2")
axes[1].set_ylabel("Pixel Count")
axes[1].grid(alpha=0.3)

plt.tight_layout()
st.pyplot(fig)
