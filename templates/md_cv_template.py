CV_TEMPLATE_MD = '''
{% set name = cv.header.full_name %}
{% set title = cv.header.professional_title %}
{% set location = cv.header.location.city + ", " + cv.header.location.region + ", " + cv.header.location.countryCode %}
{% set email = cv.header.email_address %}
{% set phone = cv.header.phone_number %}
{% set github = cv.header.github_url %}
{% set linkedin = cv.header.linkedin_url %}
{% set portfolio = cv.header.portfolio_url %}

# {{ name }}
## {{ title }}
**Location:** {{ location }} | **Email:** {{ email }} | **Phone:** {{ phone }}
**Links:** [GitHub]({{ github }}) | [LinkedIn]({{ linkedin }}) | [Portfolio]({{ portfolio }})

## Professional Summary
{{ cv.professional_summary.summary }}

### Objective
{{ cv.professional_summary.objective }}

### Highlights
{% for highlight in cv.professional_summary.highlights %}
* {{ highlight }}
{% endfor %}

{% if cv.skills %}
## Skills
{% for skill in cv.skills %}
### {{ skill.name }} {% if skill.level %}({{ skill.level.value }}){% endif %}
{{ ', '.join(skill.keywords) }}
{% endfor %}
{% endif %}

{% if cv.work_experience %}
## Work Experience
{% for work_item in cv.work_experience %}
### {{ work_item.company_name }}
ID: {{ work_item.id }}

**Location:** {{ work_item.company_location.city }}, {{ work_item.company_location.region }}, {{ work_item.company_location.countryCode }} | **Title:** {{ work_item.job_title }} | **Website:** [{{ work_item.company_website_url }}]({{ work_item.company_website_url }})
**Start Date:** {{ work_item.start_date }} | **End Date:** {{ work_item.end_date }}

{{ work_item.summary }}

{% for highlight in work_item.highlights %}
* {{ highlight }}
{% endfor %}
{% endfor %}
{% endif %}

{% if cv.projects %}
## Projects
{% for project_item in cv.projects %}
### {{ project_item.name }}
ID: {{ project_item.id }}

**Start Date:** {{ project_item.start_date }} | **End Date:** {{ project_item.end_date }}

{{ project_item.description }}

{% for highlight in project_item.highlights %}
* {{ highlight }}
{% endfor %}

[Project Link]({{ project_item.url }})
{% endfor %}
{% endif %}

{% if cv.education %}
## Education
{% for education_item in cv.education %}
### {{ education_item.institution }}
[Link]({{ education_item.url }}) | **Area:** {{ education_item.area }} | **Type:** {{ education_item.study_type.value }}
**Start Date:** {{ education_item.start_date }} | **End Date:** {{ education_item.end_date }} | **Score:** {{ education_item.score }}
**Courses:** {{ ', '.join(education_item.courses) }}
{% endfor %}
{% endif %}

{% if cv.awards %}
## Awards
{% for award_item in cv.awards %}
### {{ award_item.title }}
ID: {{ award_item.id }}

**Date:** {{ award_item.date }} | **Awarder:** {{ award_item.awarder_by }}
{{ award_item.summary }}
{% endfor %}
{% endif %}

{% if cv.certificates %}
## Certificates
{% for certificate_item in cv.certificates %}
### {{ certificate_item.name }}
**Date:** {{ certificate_item.date }} | **Issuer:** {{ certificate_item.issuer }}
[Certificate Link]({{ certificate_item.url }})
{% endfor %}
{% endif %}

{% if cv.publications %}
## Publications
{% for publication_item in cv.publications %}
### {{ publication_item.name }}
ID: {{ publication_item.id }}

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