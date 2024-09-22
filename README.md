# PersonalFinance-DjangoSite
A Comprehensive Personal Finance Website using Django, MySQL, and Bootstrap

<img width="908" alt="ww0" src="https://github.com/user-attachments/assets/7c469ebf-cb59-4b0b-9f78-336f53c95d2f">

Project Overview
The Personal Finance Tracker is a powerful and comprehensive web application designed to help users manage their finances efficiently. With features like an expense tracker, reminder notifications, note and bill storage, retirement planning, and integration with real-time CPI data and holiday news, this tool is ideal for individuals seeking control over their financial goals.

Key Features:
User Registration and Authentication

A login page that allows users to sign in with their credentials.
Registration option for new users.
<img width="925" alt="ww1" src="https://github.com/user-attachments/assets/387e8da6-5a1b-4d0d-9788-95d0292be3db">

Expense Tracker

Your Balance: Displays the current balance, which updates based on income and expenses.
Income and Expense tracking, showing amounts distinctly.
Add New Transaction: A form to enter transaction details, amount, and date. 
Export Data: Users can extract their income, expenses, and balance data in Excel and PDF formats.
 Email Summary: An email with the user's income, expenses, and balance can be shared to their registered email.
<img width="926" alt="ww2" src="https://github.com/user-attachments/assets/42d4dec8-5bbd-4969-b6cd-ba3538cd4273">

Add Note 📝

Users can store personal or financial notes related to their transactions or financial goals.
Notes can be tagged with categories.
Notes can be viewed, edited, or deleted from the Notes Section.
<img width="912" alt="wwnote" src="https://github.com/user-attachments/assets/e73a1ff7-48ad-4f7a-8c00-6ae5fc9bc339">


Add Bill 💼

Users can upload and store bills or receipts for purchases, utilities, or financial records.
The Add Bill feature allows users to upload PDF, image files, or scanned copies of their bills.
Stored bills can be accessed later for reference, and users can filter bills.
<img width="919" alt="wwbills" src="https://github.com/user-attachments/assets/19462779-1bd3-4fb8-8359-a29804a62ab6">


Reminder Feature

A Calendar allows users to set reminders for specific dates (e.g., "Pay insurance premium," "Sell HDFC mutual fund units").
Users receive an email reminder on the selected date.
<img width="929" alt="wwreminder" src="https://github.com/user-attachments/assets/0b83830b-8126-47af-b647-8ebcda767599">


API Integrations

 Data Integration: Fetches real-time CPI data using the API (API key: JIW8BTVT49VJ1VEO).
 Displays the latest public holiday deatails from India

Retirement Planning

Set Retirement Goals: Users can set financial goals for retirement (desired retirement age, income, and expenses).
<img width="919" alt="ww3" src="https://github.com/user-attachments/assets/ef7f367e-49af-4de2-a3a4-c9b809af17fd">


Technology Stack
Backend: Django (Python) + MySQL
Frontend: Bootstrap
Email Service: SMTP (for sending notifications and weekly summaries)
