# Import necessary python modules
import requests 
import json
import time

# define Skytap user variables
skytap_user = "jon.pawlowski@gmail.com"
skytap_api_token = "76394842165c75c719dbe033b1cdfd635013ff92"

# define the requesite url, headers, and authorization for the Skytap API
copy_url = 'https://cloud.skytap.com/configurations.json'
auth = (skytap_user, skytap_api_token)                 # login and password/API Token
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}
copy_template_id = 1224389

print("Cloning new environment from template...")

# Put together the json and send the request to clone the template
clone_env_json = { "template_id": copy_template_id}
api_response = requests.post(copy_url, headers=headers, auth=auth, json=clone_env_json)

# Put together the json and grab the cloned environment's ID
json_output = json.loads(api_response.text)
clone_env_id = json_output['id']

# Put together the api request to rename the cloned environment
rename_env_status = 422
new_env_name = "Copy of Pawlowski 3-Tier App"
rename_env_url = 'https://cloud.skytap.com/configurations/{}?name={}'.format(clone_env_id, new_env_name)

# Send the request until it returns a status code. This is to make sure the environment isn't still being cloned.
while (rename_env_status != 200):
    api_response = requests.put(rename_env_url, headers=headers, auth=auth)
    rename_env_status = api_response.status_code

print("Environment successfully cloned and renamed to {}.".format(new_env_name))

# Put together json and api request for starting the cloned environment.
clone_env_start = { "runstate": "running" }
start_url = 'https://cloud.skytap.com/configurations/{}.json'.format(clone_env_id)

# Send the request until it returns a 200 status code. This is to make sure no operations are being run on the environment.
clone_env_status = 422
while (clone_env_status != 200):
    api_response = requests.put(start_url, headers=headers, auth=auth, json=clone_env_start)
    clone_env_status = api_response.status_code
    
print("Environment {} is starting...".format(new_env_name))

# Poll the api every 15 seconds to ensure the environment is running
print("Polling environment {} every 15 seconds to check if it has been started...".format(new_env_name))
get_env_url = 'https://cloud.skytap.com/configurations/{}.json'.format(clone_env_id)
clone_env_state = "busy"
while (clone_env_state != "running"):
    api_response = requests.get(get_env_url, headers=headers, auth=auth)
    json_output = json.loads(api_response.text)
    clone_env_state = json_output['runstate']
    time.sleep(15)
    
print("Environment {} started successfully.".format(new_env_name))

# Stop the environment after 5 minutes
print("Letting the environment {} run for 5 minutes...".format(new_env_name))
time.sleep(300)
clone_env_stop = { "runstate": "stopped" }
api_response = requests.put(start_url, headers=headers, auth=auth, json=clone_env_stop)

print("Environment {} is stopping...".format(new_env_name))

# Continuously check for environment state to be stopped
print("Polling environment {} every 15 seconds to check if it has been stopped...".format(new_env_name))
clone_env_state = "running"
while (clone_env_state != "stopped"):
    api_response = requests.get(get_env_url, headers=headers, auth=auth)
    json_output = json.loads(api_response.text)
    clone_env_state = json_output['runstate']
    time.sleep(15)

print("Environment {} stopped successfully.".format(new_env_name))

# Put together url and send api request to delete environment once it is stopped
delete_env_url = 'https://cloud.skytap.com/configurations/{}'.format(clone_env_id)
api_response = requests.delete(delete_env_url, headers=headers, auth=auth)
if (api_response.status_code == 200):
    print("Environment {} deleted successfully.".format(new_env_name))
else :
    print("Environment {} has already been deleted.".format(new_env_name))