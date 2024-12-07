<p align="center">
<img alt="logo" src="assets/logo.png" width="250">
</p>
<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/license-MIT-MIT">
 <img alt="Issues" src=https://img.shields.io/github/issues/romisadeh/tube-tracker>
 <img alt="last commit" src=https://img.shields.io/github/last-commit/romisadeh/tube-tracker>
 <img alt="Static Badge" src="https://img.shields.io/badge/Power%20BI-included-blue?logo=Power%20BI&style=flat">

</p>
<h1 align="center">TubeTracker</h1>

<p align="center">
  TubeTracker is a project that extracts YouTube channel data from my account using the YouTube API to monitor changes in views, subscribers, and overall video performance.
  The script collects daily metrics for each channel over a two-week period and visualizes the results using Power BI.
</p>

<p align="center">
  <a href="https://app.powerbi.com/links/tJZEOR0q87?ctid=784e25d3-aacb-40f0-adae-a1537ab168e5&pbi_source=linkShare&bookmarkGuid=063f3df0-4e14-43aa-a164-613324bfcdbd"> Go to dashboard</a> 
  <a href="https://github.com/romisadeh/tube-tracker/blob/main/assets/youtube_data.pbix" download>Download Dashboard</a>
</p>




## Key Insights:
- **Daily New Views**: Track the change in views for each channel on a daily basis.
- **Daily New Subscribers**: Monitor subscriber growth, broken down by channel.
- **Total Views by Topics**: Analyze total views categorized by specific channel topics.
- **Comprehensive Data Table**: A detailed table of all metrics, offering an in-depth view for analysis.

This project enables a clear understanding of how each channel is performing over time, providing data-driven insights for further evaluation.

## TubeTracker BI dashboard:
The script create a [csv file](https://github.com/romisadeh/tube-tracker/blob/main/assets/youtube_api.csv) that later is entered to Power BI to create a visualized dashboard <br>
<img alt="youtube_data-1" src="assets/youtube_data1.png" width="750"> 
<br><br>
<img alt="youtube_data-2" src="assets/youtube_data-2.png" width="750">

## Requierments:
-googleapiclient.discovery  <br>
-google_auth_oauthlib.flow <br>
-pickle <br>
-google.auth.transport.requests <br>

## Quick start:
To run code user must first get youtube scope, client secret and client secret's JOIN file. <br>
Enter [Google For Developers](https://developers.google.com/youtube/v3) and create app. <br>
download JSON file and put the information into a text file name "youtube_data" in the correct order: <br>
1. scopes <br>
2. client secret <br>
<p align="left">
run the code to create a csv file with all the data <br>
