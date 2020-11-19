import logging
import json
import azure.functions as func
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.resource import ResourceManagementClient

def main(msg: func.QueueMessage, outputblob: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    json_content = json.loads(msg.get_body().decode('utf-8'))
 
    country = json_content['country'] if 'country' in json_content else "US"
    state = json_content['state'] if 'state' in json_content else "Florida"
    shelter_date = json_content['shelter_date'] if 'shelter_date' in json_content else "2020-03-27"
    shelter_end_date = json_content['shelter_end_date'] if 'shelter_end_date' in json_content else "2022-08-01"
    shelter_release_start_date = json_content['shelter_release_start_date'] if 'shelter_release_start_date' in json_content else "2020-05-04"
    shelter_release_end_date = json_content['shelter_release_end_date'] if 'shelter_release_end_date' in json_content else "2020-06-29"
    county = json_content['county'] if 'county' in json_content else "['Hillsborough', 'Pasco', 'Pinellas', 'Polk']"
    sim_length = json_content['sim_length'] if 'sim_length' in json_content else "60"
    nDraws = json_content['nDraws'] if 'nDraws' in json_content else "50000"
    social_distancing = json_content['social_distancing'] if 'social_distancing' in json_content else "True"
    social_distancing_end_date = json_content['social_distancing_end_date'] if 'social_distancing_end_date' in json_content else "2020-06-15"
    quarantine_percent = json_content['quarantine_percent'] if 'quarantine_percent' in json_content else "0"
    quarantine_start_date = json_content['quarantine_start_date'] if 'quarantine_start_date' in json_content else "2020-08-01"
    hashVal = json_content['hash'] if 'hash' in json_content else "default"
    max_jobs = json_content['max_jobs'] if 'max_jobs' in json_content else "3"
    webhook_token = json_content['webhook_token'] if 'webhook_token' in json_content else ""
    webhook_url = json_content['webhook_url'] if 'webhook_url' in json_content else ""
    progress_delay = json_content['progress_delay'] if 'progress_delay' in json_content else "10"
    data_hash = json_content['data_hash'] if 'data_hash' in json_content else ""
    capacity_provider = json_content['capacity_provider'] if 'capacity_provider' in json_content else "FARGATE"

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "seircastRG" 
    CONTAINER_GROUP = "seircast-cg"
    CONTAINER_NAME = "seircast-model"  # must match the regex '[a-z0-9]([-a-z0-9]*[a-z0-9])?'
    WORKSPACE_ID = os.environ.get("WORKSPACE_ID", None) # Log analytics workspace ID
    WORKPSACE_KEY = os.environ.get("WORKSPACE_KEY", None)
    CONTAINER_IMAGE = os.environ.get("CONTAINER_IMAGE", None)

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    """
    # TODO https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd#defaultazurecredential-object-has-no-attribute-signed-session
    # This is necessary to authenticate and provide the credential to the ContainerInstanceManagementClient
    containerinstance_client = ContainerInstanceManagementClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create container group
    container_group = containerinstance_client.container_groups.create_or_update(
        GROUP_NAME,
        CONTAINER_GROUP,
        {
          "location": "eastus",
          "identity": {
            "type": "SystemAssigned"
          },
          "containers": [
            {
              "name": CONTAINER_NAME,
              "command": [],
              "environment_variables": [
                {
                    'name': 'country',
                    'value': country
                },
                {
                    'name': 'state',
                    'value': state
                },
                {
                    'name': 'shelter_date',
                    'value': shelter_date
                },
                {
                    'name': 'shelter_end_date',
                    'value': shelter_end_date
                },
                {
                    'name': 'shelter_release_start_date',
                    'value': shelter_release_start_date
                },
                {
                    'name': 'shelter_release_end_date',
                    'value': shelter_release_end_date
                },
                {
                    'name': 'county',
                    'value': county
                },
                {
                    'name': 'sim_length',
                    'value': sim_length
                },
                {
                    'name': 'nDraws',
                    'value': nDraws
                },
                {
                    'name': 'social_distancing',
                    'value': social_distancing
                },
                {
                    'name': 'social_distancing_end_date',
                    'value': social_distancing_end_date
                },
                {
                    'name': 'quarantine_percent',
                    'value': quarantine_percent
                },
                {
                    'name': 'quarantine_start_date',
                    'value': quarantine_start_date
                },
                {
                    'name': 'hash',
                    'value': hashVal
                },
                {
                    'name': 'max_jobs',
                    'value': max_jobs
                },
                {
                    'name': 'webhook_token',
                    'value': webhook_token
                },
                {
                    'name': 'webhook_url',
                    'value': webhook_url
                },
                {
                    'name': 'progress_delay',
                    'value': progress_delay
                },
                {
                    'name': 'data_hash',
                    'value': data_hash
                }
              ],
              "image": CONTAINER_IMAGE,
              "resources": {
                "requests": {
                  "cpu": "4",
                  "memory_in_gb": "8"
                }
              }
            }
          ],
          "diagnostics": {
            "log_analytics": {
              "workspace_id": WORKSPACE_ID,
              "workspace_key": WORKPSACE_KEY
            }
          },
          "os_type": "Linux",
          "restart_policy": "Never"
        }
    )
    print("Create container group:\n{}".format(container_group))

    print("Container exec:\n{}".format(result))
    """
    outputblob.set(msg.get_body().decode('utf-8'))