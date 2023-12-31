<a name="ENACOM Project"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Paniceres/PI_Data_Analytics">
    <img src="/src/ENACOM_logo.png" alt="Logo" width="500" height="225">
  </a>

<h3 align="center">ENACOM Data Analytics Project</h3>

  <p align="center">
    Data Analysis for Network Optimization
    <br />
    <a href="https://github.com/Paniceres/PI_Data_Analytics"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://enacom-data-analytics-paniceres.streamlit.app/">View Deploy</a>
    ·
    <a href="https://github.com/Paniceres/PI_Data_Analytics/issues">Report Bug</a>
    ·
    <a href="https://github.com/Paniceres/PI_Data_Analytics/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#methodology">Methodology</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

ENACOM, a leading telecommunications company, seeks to improve its network optimization. This project aims to enhance the network performance by developing an effective data analysis and machine learning solution. The goal is to provide more efficient network routing, improve network performance, and ultimately increase the company's revenue.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
* [![NumPy][NumPy-logo]][NumPy-url]
* [![Pandas][Pandas-logo]][Pandas-url]
* [![Python][Python-logo]][Python-url]
* [![Matplotlib][Matplotlib-logo]][Matplotlib-url]
* [![Seaborn][Seaborn-logo]][Seaborn-url]
* [![Streamlit][Streamlit-logo]][Streamlit-url]
* [![PyArrow][PyArrow-logo]][PyArrow-url]
* [![Manjaro][Manjaro-logo]][Manjaro-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip install requirements.txt

### Installation

This is an example of how to list things you need to use the software and how to install them.
* pip
  ```sh
  pip install requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Paniceres/PI_Data_Analytics.git
   ```
2. Execute main.py
   ```sh
   streamlit run 'PI_Data_Analytics/deploy/main.py'
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<a href="https://enacom-data-analytics-paniceres.streamlit.app/">View Deploy</a>

<img src="/src/usage.png" alt="Streamlit localhost" width="1000" height="520">


<img src="/src/caution.png" alt="Caution" width="341" height="415">
No encontré forma de ocultar los nombres de los modulos, solo usar la casilla interactiva de abajo.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- METHODOLOGY -->
# Methodology

The methodology employed in this project involved the following key steps:
**Data context and criterion; Extract, Transform and Load; Data Anlalysis; Deploy**

Over 30 available datasets were analyzed, and a set of criteria was imposed to optimize efforts. The selected 12 datasets were processed through ETL processes, resulting in the creation of tables containing ratios and growth rates.
Data Analysis

A comprehensive dataset, **df_kpi**, was generated from the processed data, serving as the basis for all visualizations and analyses. The economic landscape of modern Argentina was explored by understanding various correlations among technologies, growth rates, penetration totals (access rates, service availability), and speed (service quality).
Deployment Challenges

The deployment phase presented several technical challenges, particularly during the creation of the multi-app interactive dashboard. One significant challenge involved standardizing the project's directory structure to streamline data processing. Ensuring the interactivity of the dashboard required considerable effort and attention to detail.

## Key Technical Challenges Faced During Deployment:

 ### Data Processing Optimization: 
  Efficient processing of multiple datasets was crucial.
  
 ### Visualization Interactivity: 
  Making the dashboard interactive and responsive to user inputs was a priority. This required implementing interactive widgets and ensuring seamless communication between different components of the dashboard.
  
 ### Data Integration: 
  Integrating diverse datasets and ensuring consistency across different data sources was a challenge. Data cleaning and transformation procedures were meticulously applied to harmonize the data and prevent inconsistencies.
  
 ### User Experience Design: 
  Designing an intuitive and user-friendly interface was critical for ensuring a positive user experience. User interface elements were carefully chosen, and user feedback was incorporated to refine the design and enhance usability.

## Resulting Visualizations and Analyses

The project culminated in a multi-app interactive dashboard that enables users to explore and analyze the economic landscape of modern Argentina. The dashboard provides insights into various aspects of the country's economy, including growth rates, penetration totals, service availability, and speed.
Conclusion

The methodology employed in this project effectively enabled the creation of a comprehensive and interactive dashboard that offers valuable insights into the landscape of modern Argentina. By understanding the correlations among different metrics and visualizing them on a single platform, users can make informed decisions and optimize their strategies accordingly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONCLUSION -->
# Conclusion

Upon analyzing the net income trends in dollars, with its relative **stability around $500,000 USD**, we decided to interpret correlation patterns with other non-economic variables. We observed how **Fiber Optics stands out as the central focus of the proposal**, being the most cost-effective to install, increasing average speed, and enhancing connectivity rates for every province where it is implemented.

It is crucial to understand that Fiber Optics has an inverse correlation with ADSL, a technology that needs to be reduced. ADSL not only lacks technical features that favor accessibility or service quality but is also susceptible to theft due to its high copper content.

Wireless technology emerges as the one suggesting the highest connectivity, excelling in both rural and densely populated areas, owing to its wireless nature.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Paniceres Lucio - panicereslucio@gmail.com

Project Link: [https://github.com/Paniceres/PI_Data_Analytics](https://github.com/Paniceres/PI_Data_Analytics)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Deploy]: https://enacom-data-analytics-paniceres.streamlit.app/
[contributors-shield]: https://img.shields.io/github/contributors/Paniceres/PI_Data_Analytics.svg?style=for-the-badge
[contributors-url]: https://github.com/Paniceres/PI_Data_Analytics/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Paniceres/PI_Data_Analytics.svg?style=for-the-badge
[forks-url]: https://github.com/Paniceres/PI_Data_Analytics/network/members
[stars-shield]: https://img.shields.io/github/stars/Paniceres/PI_Data_Analytics.svg?style=for-the-badge
[stars-url]: https://github.com/Paniceres/PI_Data_Analitycs/stargazers
[issues-shield]: https://img.shields.io/github/issues/Paniceres/PI_Data_Analytics.svg?style=for-the-badge
[issues-url]: https://github.com/Paniceres/PI_Data_Analytics/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/paniceres-lucio/

[NumPy-logo]: https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
[Pandas-logo]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Python-logo]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Matplotlib-logo]: https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=python&logoColor=white
[Matplotlib-url]: https://matplotlib.org/
[Seaborn-logo]: https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=python&logoColor=white
[Seaborn-url]: https://seaborn.pydata.org/
[Streamlit-logo]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[PyArrow-logo]: https://img.shields.io/badge/PyArrow-F63E02?style=for-the-badge&logo=apache-arrow&logoColor=white
[PyArrow-url]: https://arrow.apache.org/pyarrow/
[Manjaro-logo]: https://img.shields.io/badge/Manjaro-35BF5C?style=for-the-badge&logo=manjaro&logoColor=white
[Manjaro-url]: https://manjaro.org/
