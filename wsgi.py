from applicaiton import app as application

if __name__ == "__main__":
    application.run(debug=False, host="0.0.0.0", port=5000, ssl_context="adhoc")
