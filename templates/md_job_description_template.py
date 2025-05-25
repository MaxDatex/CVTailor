JOB_DESCRIPTION_TEMPLATE_MD = """
# {{ job_description_data.job_title }}

{% if job_description_data.job_description.about_company %}
## About the Company
{{ job_description_data.job_description.about_company }}
{% endif %}

{% if job_description_data.job_description.about_role %}
## About the Role
{{ job_description_data.job_description.about_role }}
{% endif %}

{% if job_description_data.job_description.responsibilities %}
## Responsibilities
{{ job_description_data.job_description.responsibilities }}
{% endif %}

{% if job_description_data.job_description.requirements %}
## Requirements
{{ job_description_data.job_description.requirements }}
{% endif %}

{% if job_description_data.job_description.nice_to_have %}
## Nice to Have
{{ job_description_data.job_description.nice_to_have }}
{% endif %}

{% if job_description_data.job_description.other %}
## Other Information
{{ job_description_data.job_description.other }}
{% endif %}

"""