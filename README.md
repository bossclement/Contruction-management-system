# **Video Demo**
[Watch the video](https://youtu.be/QLT-AyDL5kM)


Team members:

- Tuyishime Clement, [Bosstclement@gmail.com](mailto:Bosstclement@gmail.com), (+250) 0791761076)

# **Construction Management System Documentation**

## **1\. Project Overview**

### **Project Name: Construction Management System**

### **Description:**

The **Construction Management System** is a web-based application designed to streamline the management of construction operations. The system allows administrators to manage workers, job applications, newsletters, payments, and messages, providing a centralized platform for construction companies to handle daily tasks efficiently.

## **2\. Learning Objectives**

Through the development of this project, the team aims to achieve the following objectives:

- **Learn how to modularize a Flask application using blueprints** to structure the application for better scalability and maintenance.
- **Enhance database management skills** by implementing SQLAlchemy ORM to manage worker, job, payment, and message data.
- **Implement session management and security mechanisms** for user authentication and authorization, ensuring data privacy and system security.
- **Create a user-friendly admin dashboard** that facilitates efficient operations management, including job assignment, application approval, and payment tracking.

## **3\. Technologies Used**

### **Backend:**

- **Flask (Python Framework)**: The core of the application, handling routing, templating, and backend logic.
- **SQLAlchemy (ORM)**: Used for database interaction, enabling easy and efficient queries to manage construction-related data.
- **SQLite/MySQL/PostgreSQL**: A relational database to store worker profiles, jobs, payments, messages, newsletters, and other system data.

### **Frontend:**

- **HTML, CSS, Bootstrap**: Used for creating responsive and modern web pages.
- **Jinja2**: The templating engine used with Flask to dynamically render HTML pages based on server-side data.

### **Version Control:**

- **Git & GitHub**: For collaborative development and version control, ensuring smooth team collaboration.

## **4\. Features and Functionalities**

### **4.1 User Authentication and Authorization**

- **Login Required**: Admin routes and sensitive operations are protected by user authentication, ensuring only authorized personnel can access the system. The application uses session management to keep users logged in for a specified duration.
- **Security Mechanism**: The application uses a secret key and session management for secure user interactions. Unauthorized access to admin routes is restricted.

### **4.2 Admin Dashboard**

The Admin Blueprint (admin) provides the following key features:

1. **Worker Management**: Admins can view the total number of workers and manage their job statuses.
2. **Job Management**: Admins can view all jobs, create new jobs, edit job details, and delete jobs.
3. **Job Applications**: Admins can view and approve or decline job applications submitted by workers.
4. **Payment Management**: Admins can track payment requests from workers and approve or reject them.
5. **Message Management**: Admins can view messages from users and delete or respond to them.
6. **Newsletter Management**: Admins can view and manage email newsletters, including deleting subscribers.

### **4.3 Client Dashboard**

The Client Blueprint (client) provides a user-friendly dashboard for workers. Workers can:

- View job postings.
- Apply for available jobs.
- Track the status of their job applications.
- Receive notifications about job approvals or rejections.

### **4.4 Newsletter Subscriptions**

Users can subscribe to the company’s newsletter, providing their email addresses. Admins manage these subscriptions through the newsletter interface on the admin dashboard.

### **4.5 Contact Messages**

Users can submit messages or inquiries through the contact page. These messages are stored in the database and are accessible by admins through the admin dashboard.

### **4.6 Session and Cookie Management**

- **Session Management**: Sessions are used to keep track of user login status, with a session lifetime of 60 minutes for security purposes.
- **Cookies**: Cookies are set to store user sessions, with configurations ensuring secure and efficient session handling.

## **5\. Application Structure and Requirements**

### **5.1 Application Structure**

The project follows the **Flask Blueprint** structure, enabling modular development:

- **Main App (app.py)**: This is the entry point of the application where blueprints (client, backend, admin) are registered.
- **Blueprints**:
  - **Admin Blueprint**: Handles all admin-related functionalities like job management, payments, etc.
  - **Client Blueprint**: Manages the worker’s dashboard and job applications.
  - **Backend Blueprint**: Handles database operations, user authentication, and business logic.

### **5.2 Requirements**

To run the project, the following dependencies are required:

- **Python 3.8+**
- **Flask 2.0+**
- **Flask-Session**
- **Flask-SQLAlchemy**

### **5.3 System Configuration**

- **Secret Key**: Used for session management, app.secret_key is set in the main app.
- **Session Lifetime**: Configured to 60 minutes using PERMANENT_SESSION_LIFETIME.
- **Cookie Domain**: Set to build.com for secure cookie handling across subdomains.

## **6\. Challenges Identified**

### **6.1 Security**

- Managing access control for admin functionalities is a key challenge. The system must ensure that sensitive routes are protected by proper user authentication and session handling.

### **6.2 Scalability of Database**

- Handling large datasets, such as worker profiles, job listings, and messages, requires careful query optimization to prevent performance bottlenecks.

### **6.3 UI/UX**

- Designing an intuitive and user-friendly interface for both admins and workers is crucial. This will require testing and user feedback to refine.

### **6.4 Time Management**

- Completing the project within the given 27-day timeline is challenging, requiring disciplined task allocation and tracking using project management tools like Trello or Kanban boards.
