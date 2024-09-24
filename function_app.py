import azure.functions as func
import logging
import mysql.connector
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="mysqltestdb2.mysql.database.azure.com",
        user="azdbuser",
        password="Password@1",
        database="testdb",
        ssl_ca='c:/ssl/DigiCertGlobalRootCA.crt.pem',
        ssl_verify_cert=True,
        ssl_disabled=False 
    )


@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

# Insert user into the database
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM table1;")
        data = cursor.fetchall()
        # cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        # db.commit()
        cursor.close()
        db.close()
        return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")
       
        # return func.HttpResponse(f"User {name} added successfully.", status_code=200)
    except Exception as e:
        logging.error(e)
        # return func.HttpResponse("Failed to insert user.", status_code=500)
            
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )