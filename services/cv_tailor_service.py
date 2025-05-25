from typing import Optional, List, Union, Dict, Type

from ai.llm import get_cv_improvements
from models.revised_cv_fields import LLMResponse, RevisedCVResponseSchema
from templates.md_cv_template_to_llm import CV_TEMPLATE_LLM_MD
from templates.md_job_description_template import JOB_DESCRIPTION_TEMPLATE_MD
from jinja2 import Template
from loguru import logger
from models.input_cv_fields import (
    CVBody,
    SkillItem,
    WorkItem,
    ProjectItem,
    AwardItem,
    PublicationItem,
)
from models.job_description_fields import JobDescriptionFields
from models.revised_cv_fields import (
    RevisedWorkItem,
    RevisedProjectItem,
    RevisedAwardItem,
    RevisedPublicationItem,
)
from models.comparison_cv_fields import (
    ComparisonField,
    ComparisonProfessionalSummary,
    ComparisonWorkItem,
    ComparisonProjectItem,
    ComparisonCV,
    ComparisonAwardItem,
    ComparisonPublicationItem,
)


def _get_comparison_item_data(
    original_item: Union[
        Type[WorkItem], Type[ProjectItem], Type[AwardItem], Type[PublicationItem]
    ],
    revised_item_suggestion: Union[
        Type[RevisedWorkItem],
        Type[RevisedProjectItem],
        Type[RevisedPublicationItem],
        Type[RevisedAwardItem],
    ],
) -> Dict:
    comparison_item_data: Dict = {
        "id": original_item.id,
        "original_data": original_item,
        "summary": ComparisonField[str](
            original=original_item.summary,
            suggested=(
                revised_item_suggestion.revised_summary
                if revised_item_suggestion
                else None
            ),
        ),
    }
    if original_item.highlights is not None and len(original_item.highlights) > 0:
        comparison_item_data["highlights"] = ComparisonField[List[str]](
            original=original_item.highlights,
            suggested=(
                revised_item_suggestion.revised_highlights
                if revised_item_suggestion
                else None
            ),
        )
    return comparison_item_data


def _get_compared_field(
    original_cv: Type[CVBody],
    ai_suggestions: Type[RevisedCVResponseSchema],
    cv_field: str,
    comparison_item: Union[
        Type[ComparisonWorkItem],
        Type[ComparisonProjectItem],
        Type[ComparisonAwardItem],
        Type[ComparisonPublicationItem],
    ],
) -> List[
    Union[
        Type[ComparisonWorkItem],
        Type[ComparisonProjectItem],
        Type[ComparisonAwardItem],
        Type[ComparisonPublicationItem],
    ]
]:

    comp_list: List = []
    original_cv_item = getattr(original_cv, cv_field)
    if original_cv_item:
        original_map = {item.id: item for item in (original_cv_item or [])}
        revised_cv_item = getattr(ai_suggestions, f"revised_{cv_field}")
        if revised_cv_item:
            for revised_item_suggestion in revised_cv_item:
                original_item = original_map.get(revised_item_suggestion.id)
                if original_item:
                    comparison_item_data = _get_comparison_item_data(
                        original_item, revised_item_suggestion
                    )

                    comp_list.append(comparison_item(**comparison_item_data))
                else:
                    logger.warning(
                        f"AI suggested revision for ID {cv_field} '{revised_item_suggestion.id}' not found in original CV."
                    )
            # Include original work items that AI didn't suggest changes for
            ai_revised_item_ids = {item.id for item in (revised_cv_item or [])}
            for original_item in original_cv_item:
                if original_item.id not in ai_revised_item_ids:
                    comparison_item_data = _get_comparison_item_data(
                        original_item, None
                    )
                    comp_list.append(comparison_item(**comparison_item_data))
                    logger.debug(
                        f"Added original {cv_field} ID (no AI suggestion): {original_item.id}"
                    )

    return comp_list


def create_comparison_cv(
    original_cv: CVBody, ai_suggestions: RevisedCVResponseSchema
) -> ComparisonCV:
    logger.info("Starting to create comparison CV structure.")

    compared_prof_title = ComparisonField[str](
        original=original_cv.header.professional_title,
        suggested=ai_suggestions.revised_professional_title,
    )

    original_ps = original_cv.professional_summary
    revised_ps = ai_suggestions.revised_professional_summary

    compared_ps = ComparisonProfessionalSummary(
        summary=ComparisonField[Optional[str]](
            original=original_ps.summary,
            suggested=revised_ps.summary if revised_ps else None,
        ),
        objective=ComparisonField[Optional[str]](
            original=original_ps.objective,
            suggested=revised_ps.objective if revised_ps else None,
        ),
        highlights=ComparisonField[Optional[List[str]]](
            original=original_ps.highlights,
            suggested=revised_ps.highlights if revised_ps else None,
        ),
    )

    original_skills_list: Optional[List[SkillItem]] = original_cv.skills
    suggested_skills_list: Optional[List[SkillItem]] = ai_suggestions.revised_skills

    compared_work_experience = _get_compared_field(
        original_cv, ai_suggestions, "work_experience", ComparisonWorkItem
    )
    compared_projects = _get_compared_field(
        original_cv, ai_suggestions, "projects", ComparisonProjectItem
    )
    compared_awards = _get_compared_field(
        original_cv, ai_suggestions, "awards", ComparisonAwardItem
    )
    compared_publications = _get_compared_field(
        original_cv, ai_suggestions, "publications", ComparisonPublicationItem
    )

    return ComparisonCV(
        original_header=original_cv.header,
        professional_title=compared_prof_title,
        professional_summary=compared_ps,
        original_skills=original_skills_list,
        suggested_skills=suggested_skills_list,
        work_experience=compared_work_experience,
        projects=compared_projects,
        education=original_cv.education,  # Pass through non-revised
        ai_general_explanations=ai_suggestions.explanations,
        awards=compared_awards,
        publications=compared_publications,
    )


def tailor_cv(original_cv: CVBody, job_description: JobDescriptionFields):
    cv_template = Template(CV_TEMPLATE_LLM_MD)
    job_description_template = Template(JOB_DESCRIPTION_TEMPLATE_MD)

    cv = cv_template.render(cv=original_cv)
    job_description = job_description_template.render(
        job_description_data=job_description
    )
    response: LLMResponse = get_cv_improvements(job_description, cv)
    ai_suggestions: RevisedCVResponseSchema = response.response.parsed
    return create_comparison_cv(original_cv, ai_suggestions)
