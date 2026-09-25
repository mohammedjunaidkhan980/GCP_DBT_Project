-- stg_transactions.sql
-- Reads from raw BigQuery table loaded from GCS
-- Source: # here your GCP project id.raw.transactions

with source as (
    select * from `# here your GCP project id`.`raw`.`transactions`
),

renamed as (
    select
        cast(txn_id      as string)   as txn_id,
        cast(account_id  as string)   as account_id,
        cast(customer_id as string)   as customer_id,
        cast(amount      as float64)  as amount,
        cast(txn_type    as string)   as txn_type,
        cast(txn_date    as date)     as txn_date,
        cast(status      as string)   as status,
        cast(city        as string)   as city
    from source
    where txn_id is not null
)

select * from renamed
