select 
    id,
    name as news_title,
    currency_code,
    country,
    impact as impact_level,
    previous,
    forecast,
    actual,
    previous_class,
    actual_class,
    revised_previous,
    all_day as is_all_day,
    starts_at as news_time,
    week,
    details_source,
    details_measures as details_description,
    details_frequency,
    details_why_care,
    details_expanded,
    details_notes as news_note
from 
    {{ source('babypips', 'babypips_calendar_news') }}