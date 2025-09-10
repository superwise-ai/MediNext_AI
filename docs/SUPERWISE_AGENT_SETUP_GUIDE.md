# Superwise API Integration Guide

This guide explains how to set up and use the Superwise API integration in MediNext AI.

## 🔑 Prerequisites & Account Setup

### **Step 1: Create Superwise Account**

1. **Sign Up**: Visit [Superwise Platform](https://platform.superwise.ai/) and create a free account
2. **Verify Email**: Complete email verification process
3. **Access Dashboard**: Log in to your Superwise dashboard

**Note**: You'll also need an **OpenAI API key** for the model setup (Step 7). If you don't have one, create an account at [OpenAI Platform](https://platform.openai.com/) and generate an API key.

### **Step 2: Create Application**

1. **Navigate to Applications**: In your Superwise dashboard, go to "Applications" section
2. **Create New App**: Click "Create Application" or "New App"
3. **Select Framework**: Choose **"Superwise Framework"** (not Flowise Framework)
4. **Application Creation Dialog**: A dialog will open with the following fields:
   - **Application Name**: Enter `MediNext AI` (or your preferred name)
   - **Application Type**: Select **"Basic LLM Assistant"** (option 3)
     - Available options:
       - AI-Assistant Retrieval (option 1)
       - Advanced Agent (option 2)
       - **Basic LLM Assistant (option 3)** ← Select this one
5. **Complete Creation**: Click "Done" to create the application
6. **Application Dashboard**: After clicking "Done", you'll see the application dashboard with:
   - **Top Left**: Application name and **App ID** (copy this for your `.env` file)
   - **Top Right**: Two action buttons:
     - **"+Model"**: Add AI models to your application
     - **"Save&Publish"**: Save and publish your application
   - **Main Area**: 
     - **Chat Playground**: Interactive testing area for your application
   - **Left Sidebar**: Configuration sections:
     - **"Prompt"**: Configure prompts and instructions
     - **"Authentication"**: Set up API authentication
     - **"Guardrails"**: Configure safety and compliance rules

7. **Model Setup**: Configure the AI model for your application:
   - **Click "+Model" Button**: Located in the top right of the dashboard
   - **Model Provider Dialog**: A dialog will open with provider options:
     - OpenAI
     - Google AI
     - Anthropic
     - Other providers
   - **Select Provider**: Choose **"OpenAI"** as the model provider
   - **Prerequisites**: Ensure you have an OpenAI API key/token
   - **Model Selection**: Select **"gpt-4.1"** (recommended model)
   - **API Configuration**:
     - **API Token Box**: Enter your OpenAI API key/token
     - **Click "Save"**: Complete the model setup

8. **Prompt Configuration**: Set up the AI assistant's behavior and instructions:
   - **Navigate to Prompt Section**: Click on "Prompt" in the left sidebar
   - **Add System Prompt**: Copy and paste the following prompt into the prompt dialog box:

   ```
   You are a clinical decision-support assistant for healthcare professionals. I will provide you with de-identified and synthetic patient information or laboratory test results.

   Your task:

   Interpret the data in general, non-patient-specific, and educational terms.

   If the information is unclear, incomplete, or contradictory, clearly state:
   "The data provided is insufficient or inconsistent for reliable interpretation."

   For each condition or finding:

   Summarize the possible clinical significance

   Outline common causes or contributors

   After all conditions are described, provide one consolidated section of general next steps that a healthcare professional might consider (e.g., further diagnostic testing, specialist referral, lifestyle review).

   Do not provide a definitive diagnosis or specific treatment instructions. Instead, emphasize contextual interpretation and general medical reasoning.

   Always include a closing note:
   "This information is intended for clinical decision-support and contextual understanding by healthcare professionals. Final decisions must be made by licensed providers with access to the complete patient history and clinical context."
   ```

   - **Save Prompt**: Click "Save" to save the prompt configuration

9. **Publish Application**: Make your application available for use:
   - **Click "Save&Publish" Button**: Located in the top right of the dashboard
   - **Wait for Processing**: The system will process your configuration (may take a few minutes)
   - **Check Status**: Monitor the application status on the right side top near "Created at"
   - **Status Confirmation**: Once ready, you'll see status change to **"Available"**

✅ **Congratulations! Your Superwise application is now ready to use.**

10. **Get Credentials**: From the dashboard, you can find:
    - **App ID**: Located below the application name (top left) - **Copy this for your project**
    - **API URL**: Base URL for API calls (usually `https://api.superwise.ai/`)
    - **API Version**: Current API version (usually `v1`)

## 🔧 Configuration Setup

### **Step 11: Configure Project Environment Variables**

Now that your Superwise application is ready, you need to configure it in your MediNext AI project:

1. **Copy Template**: 
   
   **Linux/Mac:**
   ```bash
   cp .env.example .env
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   copy .env.example .env
   ```
   
   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit Configuration**:
   ```bash
   # Superwise API Settings
   SUPERWISE_API_URL=https://api.superwise.ai/
   SUPERWISE_API_VERSION=v1
   SUPERWISE_APP_ID=your_app_id_here
   
   # API Timeout Settings (in seconds)
   API_TIMEOUT=30
   
   # Retry Settings
   MAX_RETRIES=3
   RETRY_DELAY=1
   ```

3. **Replace App ID**: Update `SUPERWISE_APP_ID` with your actual App ID from Step 10 (the one you copied from the Superwise dashboard)

### **Step 12: Test Integration**

1. **Start Application**: Run the application using Docker or local Python
2. **Navigate to Patient Details**: Go to `/patient-details` page
3. **Test AI Analysis**: Click "Analyze with Superwise AI" button
4. **Verify Connection**: Check for successful API response or error messages

### **Troubleshooting**

**Common Issues:**
- **Wrong Framework Selected**: Ensure you selected "Superwise Framework" (not Flowise Framework) during app creation
- **Wrong Application Type**: Make sure you selected "Basic LLM Assistant" (option 3) in the application type dialog
- **Invalid App ID**: Double-check your App ID in Superwise dashboard
- **API URL Issues**: Ensure `SUPERWISE_API_URL` matches your Superwise region
- **Timeout Errors**: Increase `API_TIMEOUT` value if experiencing slow responses
- **Authentication Errors**: Verify your Superwise account is active and has proper permissions

**Need Help?**
- Review Superwise documentation: [Superwise Docs](https://docs.superwise.ai/)
- Contact Superwise support for API-related issues

## 🚀 Usage

### How it Works

1. **Patient Selection**: User selects a patient from the patient table
2. **Navigate to Details**: Click "Ask Superwise" button to go to patient details
3. **API Call**: Click "Ask Superwise" button on the details page
4. **Analysis**: The system calls the Superwise API with patient data
5. **Response**: Displays the AI analysis results

### API Payload Structure

The system sends only the essential medical fields to Superwise for clinical decision support:

```json
{
  "input": "Patient Information for Clinical Decision Support:\n\nPatient Birth Date: 1979-05-15\nGender: M\nMedical Conditions: Hypertension, Type 2 Diabetes\nHemoglobin Level: 14.2 g/dL\nCurrent Medications: Lisinopril 10mg daily, Metformin 500mg twice daily\nGlucose Level: 95 mg/dL\n\nPlease provide clinical interpretation and general next steps for healthcare professionals.",
  "chat_history": []
}
```

**Fields Sent to Superwise:**
- **Patient Birth Date**: Date of birth for age calculation
- **Gender**: Patient's gender (M/F)
- **Medical Conditions**: Current medical conditions
- **Hemoglobin Level**: Hemoglobin value in g/dL
- **Current Medications**: Current medication list
- **Glucose Level**: Glucose value in mg/dL

**Privacy Note**: The system only sends essential medical data required for clinical decision support. Personal identifiers (SSN, address, phone) are not transmitted to Superwise.

## 🔍 Error Handling

The system handles various error scenarios:

- **Configuration Error**: Missing API key or URL
- **Timeout**: API request takes too long
- **Network Error**: Connection issues
- **API Error**: Server returns error status
- **Unexpected Error**: Other unexpected issues

## 📝 Logging

All API calls are logged with:
- Request details
- Response status
- Error messages (if any)
- Patient ID for tracking

## 🛠️ Customization

### Modify API Endpoint

Edit `app/config/api_config.py` to change:
- API URL
- Headers
- Timeout settings
- Retry logic

### Custom Payload

Modify the `payload` structure in `call_superwise_api()` function to send different data to Superwise.

### Response Formatting

Update the response formatting in the button click handler to display different information from the API response.

## 🔒 Security Notes

- API keys are stored in environment variables
- Never hardcode API keys in source code
- Use HTTPS for all API communications
- Implement rate limiting if needed
- Monitor API usage and costs

## 🧪 Testing

### Test API Connection

```python
# Test the API configuration
from app.config.api_config import validate_api_config
print(validate_api_config())  # Should return True if configured correctly
```

### Mock API for Development

For development without real API calls, you can modify the `call_superwise_api()` function to return mock data:

```python
def call_superwise_api(patient_data):
    # Mock response for development
    return {
        "success": True,
        "data": {
            "risk_level": "Moderate",
            "confidence": "87%",
            "insights": "Patient shows moderate risk factors...",
            "recommendations": "Schedule follow-up appointment..."
        },
        "message": "Mock analysis completed"
    }
```
