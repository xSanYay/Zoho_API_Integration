# Zoho API Integration

A **Zoho API Leave Monitoring** project — your helpline for navigating Zoho's tricky documentation.

## Overview

This repository helps integrate and monitor leaves using Zoho People API with clear instructions for API setup and usage.

---

## Getting Started

### **API Key Setup (Simplified for You!)**

1. **Determine Your Region**:
   - For **India**: Use `zoho.in` in API URLs.
   - For other regions: Use `zoho.com`.

2. **Access Zoho API Console**:
   - Go to [Zoho API Console](https://api-console.zoho.in/) for India, or adjust for your region.

3. **Create a Self-Client**:
   - Choose the **Self Client** option in the API Console.

4. **Generate Authorization Token**:
   - Select **scope** based on the application:
     - Example: `Zoho.People.leaves.ALL`, `Zoho.forms.ALL`, etc.
   - Set **duration** (10 minutes recommended for testing).
   - Add a brief description.
   - Copy the **Auth Token**, **Client ID**, and **Client Secret**.

---

### **Generate Access Token**

1. Open your terminal and run the following command:
   ```
   curl -X POST https://accounts.zoho.in/oauth/v2/token \
   -d "grant_type=authorization_code" \
   -d "client_id=YOUR_CLIENT_ID" \
   -d "client_secret=YOUR_CLIENT_SECRET" \
   -d "redirect_uri=http://localhost" \
   -d "code=YOUR_AUTH_TOKEN"

2. Access Token Notes: 
The access token is valid for 1 hour.
Save the refresh_token for re-generating the access token without re-authorization.

3. Refresh Access Token
Use the following command to refresh the access token when it expires:
```
curl --location --request POST 'https://accounts.zoho.in/oauth/v2/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'refresh_token=YOUR_REFRESH_TOKEN' \
--data-urlencode 'client_id=YOUR_CLIENT_ID

```
# The code in app.py is a leave management hrbot, does basic functions by calling zoho crm.
