*** Settings ***
Documentation  Resource file for common methods
Library     Collections
Library     ../Library/ParseDataLibrary.py
Library     ../Library/RESTRequestLibrary.py
Library     ../Library/DataBaseLibrary.py
Variables   Variables.py


*** Keywords ***
Setup connections
    [Documentation]  Setup steps for preparation database and REST API connections to work
    Make connection  ${CONNECTION_NAME}  ${APP_URL}
    Connect to the database  ${DB_FILE_NAME}


Check the balance changing
    [Documentation]  Verifying if the balance value changed after the service purchase.
    ...              *Args:\n
    ...              - start_balance: balance value before the service  purchase
    ...              - end_balance: balance value after the service  purchase
    ...              - service_cost: the cost of the purchased service
    [Arguments]  ${start_balance}  ${end_balance}  ${service_cost}
    ${estimated_balance} =  evaluate  ${start_balance}-${service_cost}
    should be equal as strings  ${estimated_balance}  ${end_balance}  The current client balance doesn't match estimated balance.

Close connections
    [Documentation]  Teardown steps
    Close database connection
    Delete all connections
