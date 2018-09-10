*** Settings ***
Documentation    Test task implementation

Resource        ../Resources/api.robot
Resource        ../Resources/common.robot
Library         ../Library/DataBaseLibrary.py


*** Settings ***
Test Setup  common.Setup connections
Test Teardown  common.Close connections

*** Test Cases ***
Testing the purchasing service functionality
    ${client_id}  ${start_balance} =  Get id and balance of client with positive balance
    ${subscribed_services} =  api.Get the client subscribed services  ${client_id}
    ${available_services} =  api.Get service list
    ${service_id}  ${service_price} =  Get non purchased service id and price  ${subscribed_services}  ${available_services}
    api.Add service to client account  ${client_id}  ${service_id}
    api.Verify the service is purchased  ${client_id}  ${service_id}
    ${current_balance} =  Get the client balance  ${client_id}
    common.Check the balance changing  ${start_balance}  ${current_balance}  ${service_price}
