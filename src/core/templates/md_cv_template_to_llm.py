CV_TEMPLATE_LLM_MD = """
{% set name = cv.header.full_name %}
{% set title = cv.header.professional_title %}

# {{ name }}
## {{ title }}

## Professional Summary
{{ cv.professional_summary.summary }}

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

{{ project_item.summary }}

{% for highlight in project_item.highlights %}
* {{ highlight }}
{% endfor %}
{% endfor %}
{% endif %}

{% if cv.education %}
## Education
{% for education_item in cv.education %}
### {{ education_item.institution }}
**Area:** {{ education_item.area }} | **Type:** {{ education_item.study_type.value }}
**Score:** {{ education_item.score }}
**Courses:** {{ ', '.join(education_item.courses) }}
{% endfor %}
{% endif %}

{% if cv.awards %}
## Awards
{% for award_item in cv.awards %}
### {{ award_item.title }}
ID: {{ award_item.id }}

**Awarder:** {{ award_item.awarder_by }}
{{ award_item.summary }}
{% endfor %}
{% endif %}

{% if cv.certificates %}
## Certificates
{% for certificate_item in cv.certificates %}
### {{ certificate_item.name }}
**Issuer:** {{ certificate_item.issuer }}
{% endfor %}
{% endif %}

{% if cv.publications %}
## Publications
{% for publication_item in cv.publications %}
### {{ publication_item.name }}
ID: {{ publication_item.id }}

**Publisher:** {{ publication_item.publisher }}
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

"""
