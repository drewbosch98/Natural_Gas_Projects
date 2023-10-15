#MyApp

Created on 2023-10-09 18:18:14.102838
This is a natural gas fundamental dashboard, that is used to help develop views on the market.

  # About This Project
  This is a current working project of mine that utilizes open-source data to create a centralized natural gas fundamental dashboard.
  It aims to identify key factors influencing price volatility in the Western North America natural gas market and potentially the WECC power market.
  This is an interactive dashboard that allows users to explore data using their mouse.
  
  Currently:
  Natural Gas Infrastructure Map 
  * United States: United States: Hubs, Storage, Interstate and Intrastate Pipelines
  * Canada: Hubs, Storage (Interstate and Intrastate Pipelines data is unavailable)
      
  Storage Tracker:
  * United States: Tracks both Pacific and Mountain storage levels (weekly)
  * Canada: Tracks Western Canada storage levels (monthly)

  Upcoming: 
  * quantitative demand forecast model to help predict future demand for various west coast gas markets
  * quantitative storage model that will predict storage level when there is excess supply in the market
  * Weather Tracker integration to better understand key factors that are driving spot prices
  * WECC Demand model for various ISO and RTO 




## Running the App

Run `src/app.py` and navigate to http://127.0.0.1:8050/ in your browser.
