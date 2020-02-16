{% macro rm_quotes(column_name) -%}

    {#-- Extra indentation so it appears inline when script is compiled. -#}
        trim(both '"' from {{column_name}}) as "{{ column_name }}"

{%- endmacro %}

