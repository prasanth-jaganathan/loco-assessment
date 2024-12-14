from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import mysql.connector
import os

# Create a Flask application
app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# Initialize the database
def init_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
        conn.close()

        # Connect to the database and create the users table
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Error initializing database: {e}")

@app.route("/")
def home():
    # Render home page with links to /users and /add_user
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #e7eff6;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                box-sizing: border-box;
            }
            .container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
                width: 350px;
                box-sizing: border-box;
                text-align: center;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 25px;
                color: #3a3a3a;
            }
            a {
                display: block;
                font-size: 18px;
                color: #007BFF;
                text-decoration: none;
                margin-top: 15px;
                padding: 10px 0;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to User Management</h1>
            <a href="{{ url_for('get_users') }}">View Users</a>
            <a href="{{ url_for('add_user') }}">Add User</a>
                                  
        </div>
    </body>
    </html>
    """)

# Route to add a new user
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        data = request.form
        name = data.get("name")
        email = data.get("email")
        if not name or not email:
            return render_template_string(BASE_HTML, error="Name and email are required.")

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template_string(BASE_HTML, message="User added successfully", home_link=True)
        except mysql.connector.IntegrityError:
            return render_template_string(BASE_HTML, error="Email already exists", home_link=True)
        except mysql.connector.Error as e:
            return render_template_string(BASE_HTML, error=f"Database error: {e}", home_link=True)
    
    # Render the add user form
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add User</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #e7eff6;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                box-sizing: border-box;
            }
            .container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
                width: 350px;
                box-sizing: border-box;
                text-align: center;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 25px;
                color: #3a3a3a;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            button {
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Add a New User</h1>
            <form method="POST">
                <input type="text" name="name" placeholder="Enter Name" required><br>
                <input type="email" name="email" placeholder="Enter Email" required><br>
                <button type="submit">Add User</button>
            </form>
            <a href="{{ url_for('home') }}" style="display: inline-block; margin-top: 20px; padding: 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Back to Home</a>                                  
        </div>
    </body>
    </html>
    """)

# Route to list all users
# Route to list all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        # Generate the table HTML with user data
        users_table = """
        <table style="width:100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">ID</th>
                    <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">Name</th>
                    <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">Email</th>
                </tr>
            </thead>
            <tbody>
        """

        for user in users:
            users_table += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{user[0]}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{user[1]}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{user[2]}</td>
            </tr>
            """
        
        users_table += "</tbody></table>"

        # Return the table inside the HTML template
        return render_template_string(BASE_HTML, users_table=users_table, home_link=True)
    
    except mysql.connector.Error as e:
        return render_template_string(BASE_HTML, error=f"Database error: {e}", home_link=True)

@app.route("/healthz", methods=["GET"])
def health_check():
    try:
        # Try connecting to the database to ensure it's reachable
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except mysql.connector.Error as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# Base HTML template
BASE_HTML = """
<!-- Base HTML template -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e7eff6;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            box-sizing: border-box;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
            width: 350px;
            box-sizing: border-box;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 25px;
            color: #3a3a3a;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        table th, table td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        table th {
            background-color: #f4f4f4;
        }
        .message, .error {
            color: #4CAF50;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container" style="max-width: 90%; margin: 0 auto; padding: 20px;">
        <h1>User Management</h1>
       {% if message %}
            <p class="message" style="color: green; font-weight: bold;">{{ message }}</p>
        {% endif %}
        {% if error %}
            <p class="error" style="color: red; font-weight: bold;">{{ error }}</p>
        {% endif %}
        {% if users_table %}
            <h3>Users List:</h3>
            <div style="overflow-x:auto;">
                {{ users_table|safe }}
            </div>
        {% endif %}
        {% if home_link %}
            <a href="{{ url_for('home') }}" style="display: inline-block; margin-top: 20px; padding: 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Back to Home</a>
        {% endif %}
    </div>

</body>
</html>
"""

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)