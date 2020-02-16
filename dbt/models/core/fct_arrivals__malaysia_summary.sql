{{
    config(
        materialized="table",
        tags=["arrivals",]
    )
}}

with stg_airports as (

    select * from {{ ref('stg_airports') }}

),

stg_arrivals__malaysia as (

    select * from {{ ref('stg_arrivals__malaysia') }}

),

aggregate as (

    select
        arrival_date,
        arrival_iata,
        arrival_icao,
        arrival_airport_name,
        count(*) as flight_count
    from
        stg_arrivals__malaysia
    where
        is_code_share is null
    {{ group_by(4) }}
    order by 5 desc

),

final as (

    select
        a.airport_id,
        a."name",
        a.latitude,
        a.longitude,
        coalesce(b.flight_count, 0) as "flight_count"
    from
        stg_airports a
    left join
        aggregate b
    on
       a.iata = b.arrival_iata
    where country = 'Malaysia'

)

select * from final