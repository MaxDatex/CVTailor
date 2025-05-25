from jinja2 import Template

from ai.llm import get_cv_improvements
from templates.md_revised_cv_template import REVISED_CV_TEMPLATE_MD

if __name__ == "__main__":
    with open("examples/job_description.txt", "r") as f:
        job_description = f.read()

    with open("examples/cv_4_llm.md", "r") as f:
        cv = f.read()

    response = get_cv_improvements(job_description, cv)
    if not response.response:
        raise ValueError("Response is empty.")

    for k, v in response.response.parsed.model_dump().items():
        print(f"{k}: {v}\n")

    from examples.test_template import cv_dmytro

    template = Template(REVISED_CV_TEMPLATE_MD)
    rendered_md = template.render(cv=cv_dmytro, ai_response=response.response.parsed)

    with open("examples/cv_revised.md", "w") as f:
        f.write(rendered_md)
