import requests
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_to_bank_system(data, mock_mode=True):
    """Simulate bank system integration with detailed logging"""
    try:
        if mock_mode:
            # Simulate successful integration
            logging.info("Mock integration successful")
            return True

        # Real integration parameters
        api_url = "https://api.bank.com/loans"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY"
        }

        # Convert data types
        payload = {
            "applicant_name": str(data.get('name', '')),
            "annual_income": float(data['income'].replace(',', '')),
            "loan_amount": float(data['loan_amount'].replace(',', '')),
            "ssn": data.get('ssn', '')
        }

        response = requests.post(
            url=api_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10  # 10-second timeout
        )

        # Log full transaction details
        logging.info(f"Integration Request: {json.dumps(payload)}")
        logging.info(f"Bank Response: {response.status_code} - {response.text}")

        return response.status_code in [200, 201]

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection Error: {str(e)}")
        return False
    except ValueError as e:
        logging.error(f"Data Conversion Error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return False