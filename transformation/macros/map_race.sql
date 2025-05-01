{% macro map_race(code) %}
    case upper({{ code }})
        when 'A' then 'Other Asian'
        when 'B' then 'Black'
        when 'C' then 'Chinese'
        when 'D' then 'Cambodian'
        when 'F' then 'Filipino'
        when 'G' then 'Guamanian'
        when 'H' then 'Hispanic/Latin/Mexican'
        when 'I' then 'American Indian/Alaskan Native'
        when 'J' then 'Japanese'
        when 'K' then 'Korean'
        when 'L' then 'Laotian'
        when 'O' then 'Other'
        when 'P' then 'Pacific Islander'
        when 'S' then 'Samoan'
        when 'U' then 'Hawaiian'
        when 'V' then 'Vietnamese'
        when 'W' then 'White'
        when 'X' then 'Unknown'
        when 'Z' then 'Asian Indian'
    end
{% endmacro %}