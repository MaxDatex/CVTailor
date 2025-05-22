REVISED_CV_TEMPLATE_MD = '''
{% set name = cv.header.full_name %}
{% set title = cv.header.professional_title %}
{% set location = cv.header.location.city + ", " + cv.header.location.region + ", " + cv.header.location.countryCode %}
{% set email = cv.header.email_address %}
{% set phone = cv.header.phone_number %}
{% set github = cv.header.github_url %}
{% set linkedin = cv.header.linkedin_url %}
{% set portfolio = cv.header.portfolio_url %}

# {{ name }}
## {% if ai_response and ai_response.revised_professional_title %}{{ ai_response.revised_professional_title }}{% else %}{{ title }}{% endif %}
**Location:** {{ location }} | **Email:** {{ email }} | **Phone:** {{ phone }}
**Links:** [GitHub]({{ github }}) | [LinkedIn]({{ linkedin }}) | [Portfolio]({{ portfolio }})

## Professional Summary
{% if ai_response and ai_response.revised_professional_summary and ai_response.revised_professional_summary.summary %}
{{ ai_response.revised_professional_summary.summary }}
{% else %}
{{ cv.professional_summary.summary }}
{% endif %}

### Objective
{% if ai_response and ai_response.revised_professional_summary and ai_response.revised_professional_summary.objective %}
{{ ai_response.revised_professional_summary.objective }}
{% else %}
{{ cv.professional_summary.objective }}
{% endif %}

### Highlights
{% if ai_response and ai_response.revised_professional_summary and ai_response.revised_professional_summary.highlights %}
{% for highlight in ai_response.revised_professional_summary.highlights %}
* {{ highlight }}
{% endfor %}
{% else %}
{% for highlight in cv.professional_summary.highlights %}
* {{ highlight }}
{% endfor %}
{% endif %}

{% if cv.skills %}
## Skills
{% set skills_to_render = ai_response.revised_skills if ai_response and ai_response.revised_skills else cv.skills %}
{% for skill in skills_to_render %}
### {{ skill.name }} {% if skill.level %}({{ skill.level.value }}){% endif %}
{{ ', '.join(skill.keywords) }}
{% endfor %}
{% endif %}

{% if cv.work_experience %}
## Work Experience
{% for work_item in cv.work_experience %}
{% set revised_work_item = none %}
{% if ai_response and ai_response.revised_work_experience %}
    {% for r_item in ai_response.revised_work_experience %}
        {# Match by unique ID #}
        {% if r_item.id == work_item.id %}
            {% set revised_work_item = r_item %}
        {% endif %}
    {% endfor %}
{% endif %}
### {{ work_item.company_name }}
**Location:** {{ work_item.company_location.city }}, {{ work_item.company_location.region }}, {{ work_item.company_location.countryCode }} | **Title:** {{ work_item.job_title }} | **Website:** [{{ work_item.company_website_url }}]({{ work_item.company_website_url }})
**Start Date:** {{ work_item.start_date }} | **End Date:** {{ work_item.end_date }}

{% if revised_work_item and revised_work_item.revised_summary %}
{{ revised_work_item.revised_summary }}
{% else %}
{{ work_item.summary }}
{% endif %}

{% if revised_work_item and revised_work_item.revised_highlights %}
{% for highlight in revised_work_item.revised_highlights %}
* {{ highlight }}
{% endfor %}
{% else %}
{% for highlight in work_item.highlights %}
* {{ highlight }}
{% endfor %}
{% endif %}
{% endfor %}
{% endif %}

{% if cv.projects %}
## Projects
{% for project_item in cv.projects %}
{% set revised_project_item = none %}
{% if ai_response and ai_response.revised_projects %}
    {% for r_item in ai_response.revised_projects %}
        {# Assuming project_item also has an 'id' for matching #}
        {% if r_item.id == project_item.id %}
            {% set revised_project_item = r_item %}
        {% endif %}
    {% endfor %}
{% endif %}
### {{ project_item.name }}
**Start Date:** {{ project_item.start_date }} | **End Date:** {{ project_item.end_date }}

{% if revised_project_item and revised_project_item.revised_description %}
{{ revised_project_item.revised_description }}
{% else %}
{{ project_item.description }}
{% endif %}

{% if revised_project_item and revised_project_item.revised_highlights %}
{% for highlight in revised_project_item.revised_highlights %}
* {{ highlight }}
{% endfor %}
{% else %}
{% for highlight in project_item.highlights %}
* {{ highlight }}
{% endfor %}
{% endif %}

[Project Link]({{ project_item.url }})
{% endfor %}
{% endif %}

{% if cv.education %}
## Education
{% set education_to_render = ai_response.revised_education if ai_response and ai_response.revised_education else cv.education %}
{% for education_item in education_to_render %}
### {{ education_item.institution }}
[Link]({{ education_item.url }}) | **Area:** {{ education_item.area }} | **Type:** {{ education_item.study_type }}
**Start Date:** {{ education_item.start_date }} | **End Date:** {{ education_item.end_date }} | **Score:** {{ education_item.score }}
**Courses:** {{ ', '.join(education_item.courses) }}
{% endfor %}
{% endif %}

{% if cv.awards %}
## Awards
{% set awards_to_render = ai_response.revised_awards if ai_response and ai_response.revised_awards else cv.awards %}
{% for award_item in awards_to_render %}
### {{ award_item.title }}
**Date:** {{ award_item.date }} | **Awarder:** {{ award_item.awarder_by }}
{{ award_item.summary }}
{% endfor %}
{% endif %}

{% if cv.certificates %}
## Certificates
{% set certificates_to_render = ai_response.revised_certificates if ai_response and ai_response.revised_certificates else cv.certificates %}
{% for certificate_item in certificates_to_render %}
### {{ certificate_item.name }}
**Date:** {{ certificate_item.date }} | **Issuer:** {{ certificate_item.issuer }}
[Certificate Link]({{ certificate_item.url }})
{% endfor %}
{% endif %}

{% if cv.publications %}
## Publications
{% set publications_to_render = ai_response.revised_publications if ai_response and ai_response.revised_publications else cv.publications %}
{% for publication_item in publications_to_render %}
### {{ publication_item.name }}
**Publisher:** {{ publication_item.publisher }} | **Release Date:** {{ publication_item.releaseDate }}
[Publication Link]({{ publication_item.url }})
{{ publication_item.summary }}
{% endfor %}
{% endif %}

{% if cv.languages %}
## Languages
{% for language_item in cv.languages %}
### {{ language_item.language }}
**Fluency:** {{ language_item.fluency.value }}
{% endfor %}
{% endif %}

'''