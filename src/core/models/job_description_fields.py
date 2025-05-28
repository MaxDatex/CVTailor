from typing import Optional

from pydantic import BaseModel, Field


class JobDescriptionContent(BaseModel):
    about_company: Optional[str] = Field(None, min_length=10, max_length=2000)
    about_role: Optional[str] = Field(None, min_length=10, max_length=2000)
    requirements: Optional[str] = Field(None, min_length=10, max_length=2000)
    nice_to_have: Optional[str] = Field(None, min_length=10, max_length=2000)
    responsibilities: Optional[str] = Field(None, min_length=10, max_length=2000)
    other: Optional[str] = Field(None, min_length=10, max_length=1000)

    model_config = {
        "validate_assignment": True,
    }


class JobDescriptionFields(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200)
    job_description: JobDescriptionContent


def get_job_description_example():
    mock_job_description_data = {
        "job_title": "Machine Learning Engineer",
        "job_description": {
            "about_company": "Data Science UA is a service company with strong data science and AI expertise. Our journey began in 2016 with the organization of the first Data Science UA conference, setting the foundation for our growth. Over the past 8 years, we have diligently fostered the largest Data Science Community in Eastern Europe.",
            "about_role": "We are looking for a Machine Learning Engineer to become a helping hand for our internal AI/ML R&D team. Do you want to work on some real projects for our clients and/or perform R&D on novel AI algorithms and platforms? Do you want to try different fields of AI/ML, starting with advanced analytics, ending ad-hoc neural networks optimizations for Edge AI platforms? Then apply and join our team!",
            "requirements": "— 1.5 years of experience as ML Engineer/Data Scientist or related (alternatively, participation in open-source ML projects or Kaggle competitions);\n— Expertise in CV or LLM/NLP-based projects;\n— Good knowledge of math, CS, and AI fundamentals;\n— Proficiency in Python;\n— Student/graduate in the field of computer science, mathematics, cybernetics, physics, etc.\n— Upper-Intermediate English.",
            "nice_to_have": "— Have your own pet projects;\n— Completed different Data Science — related courses.",
            "responsibilities": "— Participation in AI consulting projects for Clients from Ukraine and abroad;\n— Work on complex R&D projects;\n— Preparation of technical content (presentations, analytical articles).",
            "other": "We offer:\n— Free English classes with a native speaker and external courses compensation;\n— PE support by professional accountants;\n— Medical insurance;\n— Team-building events, conferences, meetups, and other activities;\n— There are many other benefits you’ll find out at the interview.",
        },
    }

    try:
        job_description_instance = JobDescriptionFields(**mock_job_description_data)
        return job_description_instance

    except Exception as e:
        print(f"Error validating mock data: {e}")
