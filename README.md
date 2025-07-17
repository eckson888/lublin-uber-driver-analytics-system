# Welcome to Uber Driver Analytics System!
Uber Driver Analytics System is a web app that allows Uber Drivers to know and understand their data, driving behaviour and patterns which they show while working. Users can make a new account and if they downloaded their uber driver app data,
they can upload it on the webpage to verify their account. If the verification process is successful, users can check their own data visualised, or check general insights that use the data from all the drivers. System allows users to check current
trends in earnings, best places to earn and in the future - check which incoming days, hours or localisations are the most suitable for earning! Currently the system holds and analyses over 30.000 trip records collected from 6 seperate drivers.

**Caution!**: The data downloaded directly from Uber does NOT contain any private information such as names, addresses etc. It only contains trip
data such as the price, timestamps, surge prices and many many more misc data regarding the trip itself (Localisation data is not always present in the file. If it is, its only pickup and dropoff coordinates clamped to 2 digits eg. 51.25).

# Tech Stack:
  - **Python** for data operations, SQL integration and data security:
      - Flask for web application and security
      - Pandas for dataframe operations
      - NumPy for numerical operations
      - Plotly/Seaborn for graphs
  - **PostgreSQL** for data storage, selection and querying
      - SQLAlchemy module for python
  - **Tailwind** for easy CSS work.
  - (SOON) ML algorithms for timeserie and localization prediction, model evaluation with MLFlow.

# The login page
<img width="1867" height="926" alt="loginpage" src="https://github.com/user-attachments/assets/6d7dad47-ee18-4f5e-a5e1-3171ecb750da" />

# Main Page
<img width="1854" height="920" alt="main" src="https://github.com/user-attachments/assets/e88e59ad-bbdb-4b38-a426-42c48c550506" />

# General data visualisations - all interactive!
<img width="1720" height="875" alt="graph1" src="https://github.com/user-attachments/assets/7923e2f3-1605-4501-9840-71732a121fa7" />

<img width="1527" height="741" alt="heatmap" src="https://github.com/user-attachments/assets/0b194cde-0588-4871-a36c-36c8a7729826" />






