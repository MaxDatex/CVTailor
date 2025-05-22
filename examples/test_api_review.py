from ai.llm import get_cv_improvements
import json
from jinja2 import Template
from templates.md_revised_cv_template import REVISED_CV_TEMPLATE_MD


with open('job_description.txt', 'r') as f:
    job_description = f.read()

with open('cv.md', 'r') as f:
    cv = f.read()

response = get_cv_improvements(job_description, cv)

json_data = json.loads(response.text)

print(json.dumps(json_data, indent=4))

from examples.test_template import cv_dmytro
template = Template(REVISED_CV_TEMPLATE_MD)
rendered_md = template.render(cv=cv_dmytro, ai_response=response.parsed)

with open("cv_revised.md", "w") as f:
    f.write(rendered_md)