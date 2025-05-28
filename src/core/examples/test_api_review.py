if __name__ == "__main__":
    # with open("examples/job_description.txt", "r") as f:
    #     job_description = f.read()
    #
    # with open("examples/cv_4_llm.md", "r") as f:
    #     cv = f.read()
    #
    # response = get_cv_improvements(job_description, cv)
    # if not response.response:
    #     raise ValueError("Response is empty.")
    #
    # for k, v in response.response.parsed.model_dump().items():
    #     print(f"{k}: {v}\n")
    #
    # from examples.test_template import cv_dmytro
    #
    # template = Template(REVISED_CV_TEMPLATE_MD)
    # rendered_md = template.render(cv=cv_dmytro, ai_response=response.response.parsed)
    #
    # with open("examples/cv_revised.md", "w") as f:
    #     f.write(rendered_md)

    from src.core.services.cv_tailor_service import tailor_cv

    templ = """
    <!-- For Professional Title -->
    <div>
        <h3>Professional Title</h3>
        <div class="original">Original: {{ comparison_cv.professional_title.original }}</div>
        {% if comparison_cv.professional_title.suggested %}
            <div class="suggested">Suggested: {{ comparison_cv.professional_title.suggested }}</div>
            <!-- Add an input field pre-filled with suggested, or original if no suggestion -->
            <textarea name="professional_title_revised">{{ comparison_cv.professional_title.suggested or comparison_cv.professional_title.original }}</textarea>
        {% endif %}
    </div>

    <!-- For Skills -->
    <div>
        <h3>Skills</h3>
        <h4>Original Skills</h4>
        <ul>
            {% for skill in comparison_cv.original_skills %}
                <li>{{ skill.name }} ({{ skill.level.value }}): {{ skill.keywords|join(', ') }}</li>
            {% endfor %}
        </ul>
        {% if comparison_cv.suggested_skills %}
            <h4>Suggested Skills</h4>
            <ul>
                {% for skill in comparison_cv.suggested_skills %}
                     <li>{{ skill.name }} ({{ skill.level.value }}): {{ skill.keywords|join(', ') }}</li>
                {% endfor %}
            </ul>
            <!-- Here, editing skills might mean replacing the whole list, or editing items if you provide inputs for each suggested skill -->
        {% endif %}
    </div>

    <!-- For a Work Experience Item -->
    {% for work_item in comparison_cv.work_experience %}
        <div>
            <h4>{{ work_item.company_name }} - {{ work_item.job_title }}</h4>
            <p>Dates: {{ work_item.original_data.start_date }} - {{ work_item.original_data.end_date }}</p> <!-- From original_data -->
            <p>Location: {{ work_item.original_data.company_location.city }}</p> <!-- From original_data -->

            <h5>Summary</h5>
            <div class="original">Original: {{ work_item.summary.original }}</div>
            {% if work_item.summary.suggested %}
                <div class="suggested">Suggested: {{ work_item.summary.suggested }}</div>
            {% endif %}
            <textarea name="work_summary_{{ work_item.id }}">{{ work_item.summary.suggested or work_item.summary.original }}</textarea>

            <h5>Highlights</h5>
            Original:
            <ul>
                {% for hl in work_item.highlights.original %}<li>{{ hl }}</li>{% endfor %}
            </ul>
            {% if work_item.highlights.suggested %}
                Suggested:
                <ul>
                    {% for hl in work_item.highlights.suggested %}<li>{{ hl }}</li>{% endfor %}
                </ul>
            {% endif %}
            <!-- Textarea for highlights would be more complex, perhaps one per highlight or a combined one -->
        </div>
    {% endfor %}
        """
    from src.core.examples.test_template import cv_dmytro
    from src.core.models.job_description_fields import get_job_description_example

    job_description = get_job_description_example()
    comparison_cv = tailor_cv(original_cv=cv_dmytro, job_description=job_description)
    for k, v in comparison_cv.model_dump().items():
        print(f"{k}: {v}\n")

    import json

    json_object = comparison_cv.model_dump(mode="json")
    json_formatted_str = json.dumps(json_object, indent=4)

    print(json_formatted_str)
