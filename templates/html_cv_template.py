CV_TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ cv.header.full_name }} - CV</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        h1 {
            font-size: 2.5rem;
        }
        h2 {
            font-size: 2rem;
        }
        h3{
            font-size: 1.5rem;
        }
        p {
            margin-bottom: 10px;
        }
        ul, ol {
            margin-bottom: 10px;
        }
        ul li, ol li{
            margin-bottom: 5px;
        }

        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        .header img {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin-bottom: 10px;
        }
        .section {
            margin-top: 30px;
        }
        .section-title {
            font-size: 2rem;
            color: #3498db;
            margin-bottom: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        .work-item, .project-item, .education-item, .award-item, .certificate-item, .publication-item {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
        .work-item h3, .project-item h3, .education-item h3, .award-item h3, .certificate-item h3, .publication-item h3{
            font-size: 1.2rem;
        }

        .work-item h4 {
            font-size: 1.1rem;
            color: #7f8c8d;
            margin-bottom: 5px;
        }

        .skill-item {
            margin-bottom: 10px;
        }
        .skill-item h3{
            font-size: 1.2rem;
        }

        .language-item{
            margin-bottom: 10px;
        }
        .language-item h3{
            font-size: 1.2rem;
        }

        .location {
            font-size: 0.9rem;
            color: #7f8c8d;
        }

        .profile {
            margin-right: 10px;
        }

        @media (max-width: 600px) {
            .container {
                padding: 10px;
            }
            .header img {
                width: 120px;
                height: 120px;
            }
            h1 {
                font-size: 2rem;
            }
            h2 {
                font-size: 1.5rem;
            }
            h3{
                font-size: 1.2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <img src="{{ cv.header.image_url }}" alt="{{ cv.header.full_name }}'s Photo">
            <h1>{{ cv.header.full_name }}</h1>
            <p class="location">{{ cv.header.location.city }}, {{ cv.header.location.region }}, {{ cv.header.location.countryCode }}</p>
            <p>{{ cv.header.professional_title }}</p>
            <p>Email: {{ cv.header.email_address }} | Phone: {{ cv.header.phone_number }}</p>
            <p>
                {% for profile in cv.header.profiles %}
                    <a href="{{ profile.url }}" target="_blank" class="profile">{{ profile.network }}: {{ profile.username }}</a>
                {% endfor %}
            </p>
            <p>
                <a href="{{ cv.header.github_url }}" target="_blank">GitHub</a> |
                <a href="{{ cv.header.linkedin_url }}" target="_blank">LinkedIn</a> |
                <a href="{{ cv.header.portfolio_url }}" target="_blank">Portfolio</a>
            </p>
        </header>

        <section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p>{{ cv.professional_summary.summary }}</p>
            <h3>Objective</h3>
            <p>{{ cv.professional_summary.objective }}</p>
            <h3>Highlights</h3>
            <ul>
                {% for highlight in cv.professional_summary.highlights %}
                    <li>{{ highlight }}</li>
                {% endfor %}
            </ul>
        </section>

        {% if cv.skills %}
        <section class="section">
            <h2 class="section-title">Skills</h2>
            {% for skill in cv.skills %}
                <div class="skill-item">
                    <h3>{{ skill.name }} {% if skill.level %}({{ skill.level }}){% endif %}</h3>
                    <p>{{ ', '.join(skill.keywords) }}</p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.work_experience %}
        <section class="section">
            <h2 class="section-title">Work Experience</h2>
            {% for work_item in cv.work_experience %}
                <div class="work-item">
                    <h3>{{ work_item.company_name }}</h3>
                    <p class="location">{{ work_item.company_location.city }}, {{ work_item.company_location.region }}, {{ work_item.company_location.countryCode }}</p>
                    <h4>{{ work_item.job_title }}</h4>
                    <p><a href="{{ work_item.company_website_url }}" target="_blank">{{ work_item.company_website_url }}</a></p>
                    <p>{{ work_item.start_date }} - {{ work_item.end_date }}</p>
                    <p>{{ work_item.summary }}</p>
                    <ul>
                        {% for highlight in work_item.highlights %}
                            <li>{{ highlight }}</li>
                        {% endfor %}
                    </ul>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.projects %}
        <section class="section">
            <h2 class="section-title">Projects</h2>
            {% for project_item in cv.projects %}
                <div class="project-item">
                    <h3>{{ project_item.name }}</h3>
                    <p>{{ project_item.start_date }} - {{ project_item.end_date }}</p>
                    <p>{{ project_item.description }}</p>
                    <ul>
                        {% for highlight in project_item.highlights %}
                            <li>{{ highlight }}</li>
                        {% endfor %}
                    </ul>
                    <p><a href="{{ project_item.url }}" target="_blank">Project Link</a></p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.education %}
        <section class="section">
            <h2 class="section-title">Education</h2>
            {% for education_item in cv.education %}
                <div class="education-item">
                    <h3>{{ education_item.institution }}</h3>
                    <p><a href="{{ education_item.url }}" target="_blank">{{ education_item.url }}</a></p>
                    <p>{{ education_item.area }} - {{ education_item.study_type }}</p>
                    <p>{{ education_item.start_date }} - {{ education_item.end_date }}</p>
                    <p>Score: {{ education_item.score }}</p>
                    <p>Courses: {{ ', '.join(education_item.courses) }}</p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.awards %}
        <section class="section">
            <h2 class="section-title">Awards</h2>
            {% for award_item in cv.awards %}
                <div class="award-item">
                    <h3>{{ award_item.title }}</h3>
                    <p>{{ award_item.date }}</p>
                    <p>Awarded by: {{ award_item.awarder_by }}</p>
                    <p>{{ award_item.summary }}</p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.certificates %}
        <section class="section">
            <h2 class="section-title">Certificates</h2>
            {% for certificate_item in cv.certificates %}
                <div class="certificate-item">
                    <h3>{{ certificate_item.name }}</h3>
                    <p>{{ certificate_item.date }}</p>
                    <p>Issuer: {{ certificate_item.issuer }}</p>
                    <p><a href="{{ certificate_item.url }}" target="_blank">Certificate Link</a></p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.publications %}
        <section class="section">
            <h2 class="section-title">Publications</h2>
            {% for publication_item in cv.publications %}
                <div class="publication-item">
                    <h3>{{ publication_item.name }}</h3>
                    <p>Publisher: {{ publication_item.publisher }}</p>
                    <p>Release Date: {{ publication_item.releaseDate }}</p>
                    <p><a href="{{ publication_item.url }}" target="_blank">Publication Link</a></p>
                    <p>{{ publication_item.summary }}</p>
                </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if cv.languages %}
        <section class="section">
            <h2 class="section-title">Languages</h2>
            {% for language_item in cv.languages %}
              <div class="language-item">
                <h3>{{ language_item.language }}</h3>
                <p>Fluency: {{ language_item.fluency }}</p>
              </div>
            {% endfor %}
        </section>
        {% endif %}
    </div>
</body>
</html>
"""
