# M-Pesa Integration Django Application

## Overview
This is a Django-based application that integrates with M-Pesa's API to facilitate mobile money transactions. The application allows users to make payments, check transaction statuses, and manage M-Pesa transactions securely.

## Features
- Lipa na M-Pesa Online Payment (STK Push)
- C2B (Customer to Business) Transactions
- B2C (Business to Customer) Payments
- Transaction Status Query
- Reversal of Transactions

## Technologies Used
- Django
- Django REST Framework
- MySQL
- Safaricom Daraja API (M-Pesa API)
- Python Requests Library

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- MySQL
- Django

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mpesa-integration.git
   cd mpesa-integration
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file and add the following:
     ```env
     MPESA_CONSUMER_KEY=your_consumer_key
     MPESA_CONSUMER_SECRET=your_consumer_secret
     MPESA_SHORTCODE=your_shortcode
     MPESA_PASSKEY=your_passkey
     CALLBACK_URL=https://yourdomain.com/callback/
     ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- **STK Push:** Send a request to initiate an M-Pesa STK push transaction.
- **C2B Payments:** Handle customer payments made to your business shortcode.
- **B2C Payments:** Disburse payments from your business to customers.
- **Transaction Status:** Check the status of a specific transaction.

## API Endpoints
| Endpoint              | Method | Description |
|----------------------|--------|-------------|
| /api/stk-push/       | POST   | Initiates STK Push transaction |
| /api/c2b-register/   | POST   | Registers C2B callback URL |
| /api/b2c-payment/    | POST   | Sends B2C payment request |
| /api/transaction-status/ | GET | Checks transaction status |

## Contribution
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit changes.
4. Push to your fork and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or support, reach out via:
- Email: your.email@example.com
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- GitHub: [YourUsername](https://github.com/yourusername)

