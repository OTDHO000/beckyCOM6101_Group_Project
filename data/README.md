## This repo is for storing data to be used in the store choicy project.

activate environment:
- windows: venv\Scripts\activate
- linux: . venv/Scripts/activate

Sample data for testing:

Number of samples for restaurant: 400 
Criteria: if address contain "KWAI CHUNG", to ensure all tested restaurants are in Kwai Chung

Azure resource group: store-choicy

Powershell command: start-AzVM -ResourceGroupName "store-choicy" -Name "store-choicy"

Create profile for AZ CLI first:

new-item -type file -path $profile -force
Directory: C:\Users\kwokt\OneDrive\文件\WindowsPowerShell

Start azure CLI: az login

Azure start VM: az vm start --name store-choicy --resource-group store-choicy

Deploy web app to azure:
https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli 

Azrue VM:
https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal?tabs=ubuntu 

Run program in VM:
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal?tabs=ubuntu

Github token:
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 (For cloning private repo to VM)

save in /home/p233340