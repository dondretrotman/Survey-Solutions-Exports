# Survey-Solutions-Exports
Script to export Survey Solutions Data to Excel

## Title: LFS data downloader
**Description:** This uses the Survey Solutions API to generate a Data package, download and extract it  
**Version:** 5.4  
**Date:** 2024-08-11  
**Author:** Dondre Trotman  

**Notes:**  
This script assumes that you have 7zip installed and set as a path (so that it can be called without stating the path). 

It also assumes that you have the SSAW, pandas and openpyxl modules installed. Run the following in a command prompt if they are not: `pip install SSAW pandas openpyxl`. 

The pydantic module should be version 1.9.0 (`pip install --force-reinstall "pydantic==1.9.0"`).   

It also requires a directory named "Weekly Updates" to export the completed files to.

It requires a json config file in the same directory named api.json that contains values for:
- url - The URL to your Survey solutions instance
- api_user - username for the survey solutions api account
- api_password - Password for the api username
- workspace - name of the workspace (usually "default")
- homedir - The full path to the working directory
- questionnaire_identity - The id and version of the survey solution identity. You can get this by going to Survey Setup->Questionnaires->Click on the questionnaire->Details, and copy everything after "Questionnaires/Details/" in the address bar. Remove any dashes.
In the format:  
```json
{
    "url": "SURVEY SOLUTIONS URL",
    "api_user": "API USER",
    "api_password": "API PASSWORD",
    "workspace": "WORKSPACE NAME",
    "homedir": "\\path\\to\\working\\directory\\"
    "questionnaire_identity": "61578538f9ecb1e6a12ac516d8474172$29"
}
```

## Changelog: 
1.0 - Initial release. Grabs the data and extracts it  
2.0 - Prints all output to file as well as the screen, including 7zip  
3.0 - Modified for LFS  
4.0 - Made it export a finished, dated txt file with all data  
4.1 - Changed questionnaire status to "ALL", Changed filename variables to accommodate different questionnaire statuses  
5.0 - Exports to MSExcel worksheet  
5.1 - Changed it to work locally on the server  
5.2 - Changed to Version 18 of the questionnaire  
5.3 - Moved all survey specific variables to the config file (making 5.2 a non-issue)  
5.4 - Fixed bug preventing the script from running twice in the same day  
