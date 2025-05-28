if __name__ == "__main__":
    from src.core.services.cv_tailor_service import tailor_cv
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
