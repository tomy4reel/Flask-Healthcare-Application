from flask import Flask, render_template, request, redirect, send_file
import pymongo
import csv
import io

app = Flask(__name__)

# MongoDB connection setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["income_expense_db"]
collection = db["user_data"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form and insert into MongoDB
        user_data = {
            "age": request.form['age'],
            "gender": request.form['gender'],
            "total_income": request.form['total_income'],
            "expenses": {
                "utilities": request.form.get('utilities', 0),
                "entertainment": request.form.get('entertainment', 0),
                "school_fees": request.form.get('school_fees', 0),
                "shopping": request.form.get('shopping', 0),
                "healthcare": request.form.get('healthcare', 0)
            }
        }
        collection.insert_one(user_data)
        return redirect('/')
    return render_template('index.html')

@app.route('/export_csv', methods=['GET'])
def export_csv():
    # Create an in-memory CSV file
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['age', 'gender', 'total_income', 'expense_category', 'amount'])
    writer.writeheader()

    # Loop through each document in the MongoDB collection
    for user in collection.find():
        age = user['age']
        gender = user['gender']
        total_income = user['total_income']
        expenses = user['expenses']

        # Write each expense as a separate row
        for category, amount in expenses.items():
            writer.writerow({
                'age': age,
                'gender': gender,
                'total_income': total_income,
                'expense_category': category,
                'amount': amount
            })

    # Reset the buffer position to the beginning of the file
    output.seek(0)

    # Send the CSV file as a download response
    return send_file(output, mimetype='text/csv', attachment_filename='users.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
