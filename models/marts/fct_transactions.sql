-- fct_transactions.sql
-- Final aggregated table for reporting and Looker Studio dashboard
-- Aggregates credit, debit and net balance per customer per month

with int_transactions as (
    select * from {{ ref('int_transactions') }}
),

final as (
    select
        customer_id,
        account_id,
        city,
        txn_year,
        txn_month,
        count(distinct txn_id)               as total_transactions,
        sum(credit_amount)                   as total_credits,
        sum(debit_amount)                    as total_debits,
        round(sum(credit_amount)
            - sum(debit_amount), 2)          as net_balance,
        round(avg(amount), 2)                as avg_txn_amount,
        min(txn_date)                        as first_txn_date,
        max(txn_date)                        as last_txn_date
    from int_transactions
    group by
        customer_id,
        account_id,
        city,
        txn_year,
        txn_month
)

select * from final
