from jinja2 import Template

from models.input_cv_fields import (
    AwardItem,
    CertificateItem,
    CVBody,
    CVHeader,
    EducationItem,
    LanguageItem,
    Location,
    ProfessionalSummary,
    Profile,
    ProjectItem,
    PublicationItem,
    SkillItem,
    WorkItem,
    StudyType,
)
from templates.html_cv_template import CV_TEMPLATE_HTML
from templates.md_cv_template import CV_TEMPLATE_MD

# ---

location_dmytro = Location(
    address="20 Shevchenko Avenue",
    postalCode="79000",
    city="Lviv",
    countryCode="UA",
    region="Lviv Region",
)

profiles_dmytro = [
    Profile(network="Kaggle", username="dmydata", url="https://www.kaggle.com/dmydata")
]

header_dmytro = CVHeader(
    full_name="Dmytro Kovalenko",
    professional_title="Data Scientist",
    image_url="https://example.com/dmytro_kovalenko.jpg",
    email_address="dmytro.kovalenko@email.com",
    phone_number="+380 67 987 6543",
    github_url="https://github.com/dmytrodata",
    linkedin_url="https://linkedin.com/in/dmytrokovalenko",
    portfolio_url="https://dmytrokovalenko.com",
    location=location_dmytro,
    profiles=profiles_dmytro,
)

summary_dmytro = ProfessionalSummary(
    summary="An analytical and innovative Data Scientist with 4 years of experience in developing and deploying machine learning models to solve complex business problems. Proficient in data analysis, statistical modeling, and creating compelling data visualizations.",
    objective="To apply my expertise in data-driven decision-making and advanced analytics to contribute to impactful projects.",
    highlights=[
        "Skilled in Python, R, and various machine learning frameworks.",
        "Experienced in predictive modeling and statistical analysis.",
        "Proficient in data visualization and reporting.",
        "Strong problem-solving and analytical skills.",
    ],
)

skills_dmytro = [
    SkillItem(
        name="Data Science",
        level="Advanced",
        keywords=[
            "Python",
            "R",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "TensorFlow",
            "Keras",
            "PyTorch",
            "SQL",
        ],
    ),
    SkillItem(
        name="Statistical Analysis",
        level="Advanced",
        keywords=[
            "Hypothesis Testing",
            "Regression Analysis",
            "Time Series Analysis",
            "A/B Testing",
        ],
    ),
    SkillItem(
        name="Data Visualization",
        level="Intermediate",
        keywords=["Matplotlib", "Seaborn", "Plotly", "Tableau"],
    ),
    SkillItem(
        name="Cloud & Big Data",
        level="Intermediate",
        keywords=["AWS Sagemaker", "Google Cloud Platform (GCP)", "Spark", "Hadoop"],
    ),
]

work_experience_dmytro = [
    WorkItem(
        company_name="Analytics Pro",
        company_location=Location(
            address="15 Innovation Street",
            postalCode="79000",
            city="Lviv",
            countryCode="UA",
            region="Lviv Region",
        ),
        job_title="Data Scientist",
        company_website_url="https://analyticspro.ua",
        start_date="2022-01-15",
        end_date="Present",
        summary="Developed and implemented predictive models for client projects across various industries, enhancing decision-making processes.",
        highlights=[
            "Built a customer churn prediction model using gradient boosting, leading to a 10% improvement in customer retention strategies.",
            "Performed extensive exploratory data analysis on large datasets to identify key trends and insights for strategic planning.",
            "Designed and conducted A/B tests for marketing campaigns, resulting in a 15% increase in conversion rates.",
            "Deployed machine learning models into production environments using AWS Sagemaker.",
        ],
    ),
    WorkItem(
        company_name="FinTech Insights",
        company_location=Location(
            address="30 Financial Boulevard",
            postalCode="01001",
            city="Kyiv",
            countryCode="UA",
            region="Kyiv City",
        ),
        job_title="Junior Data Analyst",
        company_website_url="https://fintechinsights.com",
        start_date="2020-09-01",
        end_date="2021-12-31",
        summary="Assisted senior data scientists in data cleaning, preprocessing, and generating reports for financial analytics.",
        highlights=[
            "Cleaned and preprocessed large financial datasets, ensuring data quality and consistency.",
            "Created automated dashboards and reports using SQL and Tableau for key performance indicators.",
            "Assisted in the development of risk assessment models by preparing and analyzing relevant data.",
        ],
    ),
]

projects_dmytro = [
    ProjectItem(
        name="Sentiment Analysis of Social Media Data",
        start_date="2024-03-01",
        end_date="2024-05-15",
        description="A personal project to analyze public sentiment from Twitter data using natural language processing (NLP) techniques.",
        highlights=[
            "Collected and preprocessed Twitter data using Tweepy.",
            "Trained a Recurrent Neural Network (RNN) model for sentiment classification (positive, negative, neutral).",
            "Visualized sentiment trends over time using Plotly.",
        ],
        url="https://github.com/dmytrodata/sentiment-analysis-twitter",
    )
]

education_dmytro = [
    EducationItem(
        institution="Taras Shevchenko National University of Kyiv",
        url="https://knu.ua",
        area="Applied Statistics",
        study_type=StudyType.BACHELORS,
        start_date="2016-09-01",
        end_date="2020-06-30",
        score="3.8/4.0",
        courses=[
            "Probability Theory",
            "Statistical Inference",
            "Regression Modeling",
            "Data Mining",
        ],
    )
]

awards_dmytro = [
    AwardItem(
        title="Dean's List for Academic Excellence",
        date="2019-05-20",
        awarder_by="Taras Shevchenko National University of Kyiv",
        summary="Recognized for outstanding academic achievement in the Department of Statistics.",
    )
]

publications_dmytro = [
    PublicationItem(
        name="Predictive Modeling for Customer Lifetime Value in E-commerce",
        publisher="Journal of Data Science and Analytics",
        releaseDate="2023-11-01",
        url="https://journalofdata.com/predictive-modeling",
        summary="A research paper exploring various machine learning techniques to predict customer lifetime value, demonstrating the impact of accurate predictions on marketing strategies.",
    )
]

languages_dmytro = [
    LanguageItem(language="Ukrainian", fluency="Native"),
    LanguageItem(language="English", fluency="Fluent"),
]

cv_dmytro = CVBody(
    header=header_dmytro,
    professional_summary=summary_dmytro,
    skills=skills_dmytro,
    work_experience=work_experience_dmytro,
    projects=projects_dmytro,
    education=education_dmytro,
    awards=awards_dmytro,
    publications=publications_dmytro,
    languages=languages_dmytro,
)


template = Template(CV_TEMPLATE_MD)
# 4. Render the template with the data.
rendered_md = template.render(cv=cv_dmytro)

with open("cv.md", "w") as f:
    f.write(rendered_md)
