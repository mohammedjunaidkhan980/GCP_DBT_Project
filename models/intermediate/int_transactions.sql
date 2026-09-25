-- int_transactions.sql
-- Applies business logic on top of staging layer
-- Filters only completed transactions and adds time dimensions

with stg_transactions as (
    select * from {{ ref('stg_transactions') }}
),

enriched as (
    select
        txn_id,
        account_id,
        customer_id,
        amount,
        txn_type,
        txn_date,
        status,
        city,
        extract(year  from txn_date)              as txn_year,
        extract(month from txn_date)              as txn_month,
        case
            when amount >= 3000  then 'high'
            when amount >= 1000  then 'medium'
            else                      'low'
        end                                       as amount_category,
        case
            when txn_type = 'credit' then amount
            else 0
        end                                       as credit_amount,
        case
            when txn_type = 'debit' then amount
            else 0
        end                                       as debit_amount
    from stg_transactions
    where status = 'completed'
)

select * from enriched
