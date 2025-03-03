import pyodbc
import pandas as pd
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from io import StringIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_blob_client(tenant_id, client_id, client_secret, storage_account_name):
    """Initialize authenticated blob service client"""
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        account_url = f"https://{storage_account_name}.blob.core.windows.net"
        return BlobServiceClient(account_url=account_url, credential=credential)
    except Exception as e:
        logger.error(f"Failed to create blob client: {str(e)}")
        raise

def export_to_blob(server, database, username, password, separator, escapechar, encoding, tenant_id, client_id, client_secret, storage_account_name, container_name):
    """Export database tables to Azure Blob Storage"""
    try:
        # Initialize blob service
        blob_service_client = get_blob_client(tenant_id, client_id, client_secret, storage_account_name)
        container_client = blob_service_client.get_container_client(container_name)

        # Connect to database
        # for linux
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
        # for windows 
        #conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get and process tables
        table_names = [row.table_name for row in cursor.tables(tableType='TABLE') if row.table_name not in ('trace_xe_action_map', 'trace_xe_event_map')]
        logger.info(f"Found {len(table_names)} tables to export")

        for table_name in table_names:
            try:
                # Query and convert to CSV
                query = f'SELECT * FROM [{table_name}]' 
                df = pd.read_sql(query, conn)
                
                # Create CSV in memory
                csv_buffer = StringIO()
                df.to_csv(
                    csv_buffer,
                    index=False,
                    sep=separator,
                    doublequote=False,
                    escapechar=escapechar,
                    encoding=encoding
                )

                # Upload to blob storage
                blob_name = f'{table_name}.csv'
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(
                    csv_buffer.getvalue().encode(encoding),
                    overwrite=True
                )
                logger.info(f"Successfully uploaded {blob_name}")

            except Exception as e:
                logger.error(f"Error processing table {table_name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise Exception(f"Failed to export tables:\n{str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
            logger.info("Database connection closed")