_IsThisWater_ is a web app that detects the existence of any surface water (rivers, lakes, oceans, etc.) within a square satellite image of the surface of the Earth.


## Background

One of the most important concerns with climate change is the increasing scarcity of freshwater sources. One of the ways that technology can be used to mitigate this problem is understanding where and how much water exists on the surface of the Earth. Convolutional neural networks have been used successfully in the past to identify and map surface water from Landsat images, as explained in studies like <a href="https://www.tandfonline.com/doi/pdf/10.1080/17538947.2015.1026420?needAccess=true&">this</a> and <a href="http://live.ece.utexas.edu/publications/2017/isikdogan2017surface.pdf">this</a>.

## How to use
1. Scroll/zoom to a location on the Earth using an interactive map from Mapbox.
GIF
2. Click Detect Water.
GIF
3. The neural network will classify the image as "Water" or "No Water" and return the result. 
