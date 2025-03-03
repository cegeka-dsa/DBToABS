# File: /DBToABS/README.md

# Flask Database to Azure Blob Storage

This project is a Flask web application that allows users to export data from a database to Azure Blob Storage. Users can input their database and Azure Blob Storage details through a web form, and the application will handle the data export process.

## Project Structure

```
flask-db-to-abs
├── src
│   ├── app.py               # Entry point of the Flask application
│   ├── db_to_abs.py         # Core logic for exporting data to Azure Blob Storage
│   ├── templates
│   │   ├── base.html        # Base HTML template
│   │   └── index.html       # Main HTML template for user input
│   ├── static
│   │   └── styles
│   │       └── main.css     # CSS styles for the web application
│   └── config.py            # Configuration settings for the Flask application
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables
├── .gitignore                # Files to ignore in Git
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd flask-db-to-abs
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Create a `.env` file in the root directory and add your database and Azure credentials.

5. **Run the Application**
   ```bash
   python src/app.py
   ```

6. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Hosting on Azure

1. **Create an Azure Web App**
   - Go to the Azure Portal and create a new Web App.

2. **Deploy the Application**
   - Use Azure CLI or Git to deploy your application to the Azure Web App.

3. **Configure Application Settings**
   - In the Azure Portal, set the environment variables in the Application Settings section.

4. **Access Your Web App**
   - Once deployed, you can access your web app through the URL provided by Azure.

## Usage

- Fill out the web form with your database and Azure Blob Storage details.
- Submit the form to export the data to Azure Blob Storage.

## License

This project is licensed under the MIT License.