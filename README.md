# Customer Feedback/Review App

## Introduction The Customer Feedback/Review App is a web application designed to gather and manage customer feedback and reviews for various products. It provides a platform for customers to share their opinions, ratings, and reviews, while also offering valuable insights to businesses for improving their products and services.

The app is built using Flask, a lightweight web framework in Python, and utilizes MySQL as the database management system for storing and retrieving data.

## Features 
- **User Registration and Authentication**: Users can create accounts and log in securely to access the app's features.
- **Product Listing**: Display a list of available products for customers to browse and leave feedback.
- **Feedback Submission**: Allow customers to submit feedback, ratings, and reviews for specific products.
- **Sorting and Filtering**: Enable users to sort and filter feedback based on various criteria such as product category, rating, or date.
- **Commenting and Interactions**: Users can engage in discussions by commenting on feedback and interacting with other users.
- **Reporting and Moderation**: Implement a reporting system for inappropriate or abusive content, and provide moderation capabilities for administrators.
- **Analytics and Insights**: Generate reports and analytics based on the collected feedback to gain insights into customer preferences and areas for improvement.

## Technologies Used 
- **Python**: The primary programming language used for building the app. 
- **Flask**: A lightweight web framework for developing web applications in Python.
- **MySQL**: A robust and widely-used relational database management system.
- **HTML/CSS**: Used for front-end development and styling the user interface.
- **JavaScript**: Enhances the interactivity and functionality of the app. -
- **Bootstrap**: A popular CSS framework for creating responsive and visually appealing web pages.
- **SQLAlchemy**: An Object-Relational Mapping (ORM) library for Python, providing an abstraction layer to interact with the MySQL database.

## Installation 
1. Clone the repository: `git clone [repository URL] `
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: - For Windows: `venv` - For Unix/Linux: `source venv/bin/activate`
4. Install the dependencies: `pip install -r requirements.txt`
5. Set up the database: - Create a MySQL database for the app. - Update the database connection details in the 'config.py' file.
6. Run database migrations: `flask db upgrade`
7. Start the server: `flask run`
8. The application should now be running on [http://localhost:5000](http://localhost:5000).

## Usage 
1. Open the web application in your preferred browser.
2. Sign up for a new account or log in with your existing credentials.
3. Browse the list of available products and select a product you want to provide feedback for.
4. Submit your feedback, ratings, and reviews for the selected product.
5. Explore the app's features, such as sorting and filtering feedback, commenting on other users' feedback, and reviewing analytics and insights.
6. As an administrator, you can moderate and manage user feedback and reports through the admin panel.

## Contributing 
Contributions to the Customer Feedback/Review App are welcome! If you would like to contribute, please follow these steps: 
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name'`
3. Make your changes and commit them: `git commit -m 'Add some feature` 
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request.

## License This project is licensed under the [MIT License](LICENSE).

## Contact For any inquiries or questions, please contact [yousri rachid] at [shixymanflowx@gmail.com].

We appreciate your interest in our Customer Feedback/Review App and look forward to your valuable feedback and contributions!