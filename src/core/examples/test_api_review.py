if __name__ == "__main__":
    # from src.core.services.functional.cv_tailor_service_functional import tailor_cv
    from src.core.examples.test_template import cv_dmytro
    from src.core.models.job_description_fields import get_job_description_example
    from src.core.services.cv_tailor_service import CVTailorService
    import json
    import asyncio


    async def endpoint():
        command = input("Command: ")
        while command != "exit":
            job_description = get_job_description_example()
            tailor_cv_service = CVTailorService()
            comparison_cv = await tailor_cv_service.tailor_cv(original_cv=cv_dmytro, job_description=job_description)
            for k, v in comparison_cv.model_dump().items():
                print(f"{k}: {v}\n")

            json_object = comparison_cv.model_dump(mode="json")
            json_formatted_str = json.dumps(json_object, indent=4)

            print(json_formatted_str)
            command = input("Command: ")


    print("Program started.")
    asyncio.run(endpoint())
    print("Program finished.")
