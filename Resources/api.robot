*** Settings ***
Documentation  Resource file for working with API
Library     Collections
Library     ../Library/RESTRequestLibrary.py
Variables   Variables.py


*** Keywords ***
Create a session
    [Documentation]  Create a connection's preferences with particular server and default headers (optional).
    ${headers} =  create dictionary  Content-Type=application/json
    make connection  ${connection_name}  ${app_url}  ${headers}

Get the client subscribed services
    [Documentation]  GET-request implementation which returns a list of purchases services
    ...              *Args:\n
    ...              - connection_name: alias for the specific server/connection
    [Arguments]  ${client_id}
    ${data} =   create dictionary  client_id=${client_id}
    ${response} =  post request  ${connection_name}  ${purchased_services_url_tail}  ${data}
    should be equal as integers  ${response.status_code}  200  ${RESPONSE_ERROR_MSG} Status code: ${response.status_code}
    [Return]  ${response.json().get('items')}

Get service list
    [Documentation]  GET-request implementation which return a list of available services
    ${response} =  get request  ${connection_name}  ${all_servises_tail}
    should be equal as integers  ${response.status_code}  200  ${RESPONSE_ERROR_MSG} Status code: ${response.status_code}
    [Return]  ${response.json().get('items')}

Add service to client account
    [Documentation]  POST-request implementation which adds specific service to the client's purchased service list
    ...              *Args:\n
    ...              - client_id: the ID of the client for adding service to.
    ...              - service_id: the ID of the service which will be added.
    [Arguments]  ${client_id}  ${service_id}
    ${data} =  create dictionary  client_id=${client_id}  service_id=${service_id}
    ${response} =  post request  ${connection_name}  ${ADD_SERVICE_TAIL}  ${data}
    should be equal as integers  ${response.status_code}  202  ${RESPONSE_ERROR_MSG} Status code: ${response.status_code}

Verify the service is purchased
    [Documentation]  Verify if the specified service exists in the client's purcahsed service list
    ...              *Args:\n
    ...              - client_id: the ID of the client for adding service to.
    ...              - service_id: the ID of the service which will be added.
    [Arguments]  ${client_id}  ${service_id}
    ${data} =   create dictionary  client_id=${client_id}
    Wait until keyword succeeds  1 min  1 sec  Check if response contains service  ${connection_name}  ${PURCHASED_SERVICES_URL_TAIL}  ${data}  ${service_id}

Delete Sessions
    [Documentation]  Removes all connections settings
    Delete all connections
