{% macro map_gender(code) %}
    case upper({{ code }})
        when 'M' then 'Male'
        when 'F' then 'Femal'
        when 'X' then 'Unknown'
        else 'Unknown'
    end
{% endmacro %}