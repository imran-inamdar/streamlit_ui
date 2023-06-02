import requests
import streamlit as st
import pandas as pd
import json
import datetime
# Databricks API endpoint and token
endpoint = "https://adb-4992821984904052.12.azuredatabricks.net/api/2.0/sql/statements/"
token = "dapi3076bec455ef0b68a5e1cc98ab2db680-2"

def run_query(start_date,end_date):
    #endpoint_url = f"{endpoint}?warehouse_id={warehouse_id}"
    headers = {"Authorization": f"Bearer {token}"}
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    sql_query = f"select Name, UId as UserId, Email, concat_ws(',', collect_set(ActionLists)) AS ActionsPerformed, LifetimePoints, bround(sum(EarnedPoints), 0) as EarnedPoints, bround(sum(RedeemedPoints), 0) as RedeemedPoints, bround(sum(RedemptionCredit), 0) as RedemptionCredit, bround(sum(ReturnedPoints), 0) as ReturnedPoints, bround(sum(DebitPoints), 0) as DebitPoints, bround(sum(ExpiredPoints), 0) as ExpiredPoints, CurrentBalance, OptInStatus, LastActivityDate, LastPurchaseDate from annexcloud_reports.pointreport_curated_layer_v1 where SiteId = 29235480 and opt_in_status != 0 and MultitemplateId = 0 and UId NOT LIKE 'delete_%' and TransactionDate between '{start_date_str}' and '{end_date_str}' group by UId, name, email, lifetimepoints, OptInStatus, LastPurchaseDate, LastActivityDate, CurrentBalance, UserCreateDate HAVING EarnedPoints >= 0 ORDER BY UserCreateDate DESC"
    #sql_query="select Name,UId as UserId,Email,concat_ws(',',collect_set(ActionLists)) AS ActionsPerformed,LifetimePoints,bround(sum(EarnedPoints),0) as EarnedPoints,bround(sum(RedeemedPoints),0) as RedeemedPoints,bround(sum(RedemptionCredit),0) as RedemptionCredit,bround(sum(ReturnedPoints),0) as ReturnedPoints,bround(sum(DebitPoints),0) as DebitPoints,bround(sum(ExpiredPoints),0) as ExpiredPoints,CurrentBalance,OptInStatus,LastActivityDate,LastPurchaseDate from annexcloud_reports.pointreport_curated_layer_v1 where SiteId = 29235480 and opt_in_status!=0 and MultitemplateId=0 and UId NOT LIKE 'delete_%' and TransactionDate between 'start_date' and 'end_date' group by UId,name,email,lifetimepoints,OptInStatus,LastPurchaseDate,LastActivityDate,CurrentBalance,UserCreateDate HAVING EarnedPoints >=0"
    data = {"statement": sql_query,"warehouse_id" : '6f7d1be4c302a5c3'}
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise ValueError("Query execution failed")
    return response.json()
def run_link(external_link):
    response1 = requests.get(external_link)
    if response1.status_code != 200:
        raise ValueError("Query execution failed")
    return response1.json()


def main():
    st.title("Databricks SQL Query Executor")
    start_date = st.sidebar.date_input('Start date', datetime.date(2022,9,13))
    end_date = st.sidebar.date_input('End date', datetime.date(2022,9,19))
    st.write("Selected Start Date",start_date)
    st.write("Selected End Date",end_date)
    # Text input for SQL query
    #sql_query = st.text_area("Enter your SQL query here:")

    # Submit button
    if st.button("Submit"):
        try:
            # Send API request with SQL query and warehouse ID
            response_json = run_query(start_date,end_date)
            #count=(((response_json['result']['external_links'][0]['byte_count'])/1024)/1024)
            #st.write("Byte Count",count)
            #external_link=response_json['result']['external_links'][0]['external_link']

            #response1_json=run_link(external_link)
            #result_df = pd.DataFrame(response1_json)
            #st.write(result_df)
            #names=[response_json['manifest']['schema']['columns'][0]['names'] for key in response_json]
            #[key]["name"] for key in response_json]
            #st.write(names)
            #names = [data[key]['name'] for key in data]
            #for name in names:
                #print(name)

            result_df = pd.DataFrame(response_json['result']['data_array'])
            count=response_json['result']['row_count']
            st.write("Total Row fetched",count)
            # Display the result DataFrame as a table
            st.table(result_df)
            # Display response JSON
            #st.json(response_json)
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
