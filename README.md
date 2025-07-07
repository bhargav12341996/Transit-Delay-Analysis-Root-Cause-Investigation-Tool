# Transit-Delay-Analysis-Root-Cause-Investigation-Tool

📌 Objective:

This project aims to identify and analyze transit delays using bus GPS data, and correlate those delays with nearby road events (e.g., double parking, construction). The goal is to uncover root causes behind delays to support transit agencies and city planners in improving operational efficiency and rider experience.

🧩 Problem Statement:

Transit systems frequently suffer from unpredictable delays caused by urban traffic congestion, blocked lanes, or roadwork. While buses generate GPS logs, and cities record road incidents, these data sources are rarely connected. This project bridges that gap by:

* Detecting delays from irregular GPS time gaps

* Matching delays with nearby road events in time and space

* Highlighting potential causes using data-driven methods

🛠 What the Project Does:

* Loads and cleans GPS and road event data

* Detects delays based on time differences between GPS records

* Matches delays with road events within a 5-minute and 150-meter window

* Outputs a CSV file summarizing delays and potential causes



