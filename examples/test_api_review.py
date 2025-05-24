from jinja2 import Template

from ai.llm import get_cv_improvements
from templates.md_revised_cv_template import REVISED_CV_TEMPLATE_MD


with open("job_description.txt", "r") as f:
    job_description = f.read()

with open("cv.md", "r") as f:
    cv = f.read()

response = get_cv_improvements(job_description, cv)
if not response.success:
    raise Exception(response.error)

for k, v in response.response.parsed.__dict__.items():
    print(f"{k}: {v}\n")

from examples.test_template import cv_dmytro

template = Template(REVISED_CV_TEMPLATE_MD)
rendered_md = template.render(cv=cv_dmytro, ai_response=response.response.parsed)

with open("cv_revised.md", "w") as f:
    f.write(rendered_md)
