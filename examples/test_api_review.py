from jinja2 import Template

from ai.llm import _init_ai_resources, get_cv_improvements
from templates.md_revised_cv_template import REVISED_CV_TEMPLATE_MD

_init_ai_resources()
with open("job_description.txt", "r") as f:
    job_description = f.read()

with open("cv.md", "r") as f:
    cv = f.read()

response = get_cv_improvements(job_description, cv)
if not response.response:
    raise ValueError("Response is empty.")

for k, v in response.response.parsed.__dict__.items():
    print(f"{k}: {v}\n")

from examples.test_template import cv_dmytro

template = Template(REVISED_CV_TEMPLATE_MD)
rendered_md = template.render(cv=cv_dmytro, ai_response=response.response.parsed)

with open("cv_revised.md", "w") as f:
    f.write(rendered_md)
