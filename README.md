# SemanticRouter Application
This guide provides step-by-step instructions for setting up and launching the application. Access using the following URL: [https://semanticrouter-vsokiaomurxjrxzcasqff4.streamlit.app/](https://semanticrouter-vsokiaomurxjrxzcasqff4.streamlit.app/) or follow the sections below to get started.

## Project Setup

To set up the project, you will need to install several Python packages. You can do this using pip, Python's package installer. Execute the following commands in your terminal or command prompt to install the required packages.

**Install Required Packages:**
```
   pip install streamlit
   pip install -U semantic-router==0.0.34
   pip install unifyai
   pip install transformers
   pip install torch

```
Make sure that each command completes successfully before proceeding to the next step. If you encounter any issues during the installation process, check your Python and pip versions, and ensure your environment is configured correctly.

 **Launch the App :**


    
    streamlit run app.py

Once all necessary packages are installed, you can launch the application using Streamlit. To start the app, run the following command in your terminal where your app.py script is located.This command will start the Streamlit server and open the application in your default web browser. You can interact with the app directly from your browser.The route chosen will be printed in the terminal.

  
## Additional Information
Troubleshooting: If you encounter issues with package installations, verify that you have the correct permissions and that your Python environment is properly set up.
Requirements: This app requires a Python environment. If you don't have Python installed, download and install it from python.org.
