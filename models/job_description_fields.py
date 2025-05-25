from typing import Optional

from pydantic import BaseModel, Field, field_validator


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


def get_job_desctiption_example():

    mock_job_description_data = {
        "job_title": "Senior Full Stack Engineer",
        "job_description": {
            "about_company": "Acme Innovations is a leading technology company specializing in scalable cloud solutions and AI-driven analytics. We are committed to fostering a culture of innovation, collaboration, and continuous learning. Our mission is to empower businesses with cutting-edge tools that transform data into actionable insights, driving growth and efficiency across various industries. We value diversity and inclusion, believing that a wide range of perspectives leads to the most creative and effective solutions. Join our dynamic team and contribute to building the future of technology.",
            "about_role": "We are seeking a highly motivated and experienced Senior Full Stack Engineer to join our growing product development team. In this role, you will be responsible for designing, developing, and maintaining robust and scalable web applications from front-end user interfaces to back-end services. You will work closely with product managers, UX/UI designers, and other engineers to deliver high-quality software solutions that meet user needs and business objectives. This position offers an exciting opportunity to work on challenging projects and make a significant impact on our core products.",
            "requirements": "Minimum 5 years of professional experience in full stack web development. Proficient in Python (Django/Flask) and JavaScript (React/Angular/Vue.js). Strong understanding of RESTful APIs, microservices architecture, and database design (SQL/NoSQL). Experience with cloud platforms (AWS, GCP, or Azure) and CI/CD pipelines. Solid grasp of data structures, algorithms, and software design principles. Excellent problem-solving skills and ability to work independently as well as collaboratively within a team. Bachelor's degree in Computer Science or a related field.",
            "nice_to_have": "Experience with containerization technologies (Docker, Kubernetes). Familiarity with GraphQL. Knowledge of machine learning fundamentals or data engineering concepts. Contributions to open-source projects. Master's degree in a relevant field. Prior experience in a fast-paced startup environment. Strong communication skills and ability to mentor junior developers.",
            "responsibilities": "Design, develop, and deploy full-stack web applications and services. Write clean, maintainable, and efficient code. Collaborate with cross-functional teams to define, design, and ship new features. Participate in code reviews to ensure code quality and adherence to best practices. Troubleshoot and debug production issues. Optimize applications for maximum speed and scalability. Stay up-to-date with emerging technologies and industry trends. Contribute to architectural discussions and technical decision-making.",
            "other": "This is a full-time position based in our dynamic San Francisco office, with flexible remote work options available. We offer competitive salary, comprehensive health benefits, generous paid time off, and opportunities for professional development and growth. Our team is passionate about building innovative products and making a difference. We believe in work-life balance and provide a supportive environment for our employees to thrive. Apply now to be part of our exciting journey!",
        },
    }

    try:
        job_description_instance = JobDescriptionFields(**mock_job_description_data)
        return job_description_instance

    except Exception as e:
        print(f"Error validating mock data: {e}")
