from typing import Any, Callable, Dict, List, Optional, TypeVar

from google.genai import errors
from jinja2 import Template
from loguru import logger

from ai.llm import get_cv_improvements
from models.comparison_cv_fields import (ComparisonAwardItem, ComparisonCV,
                                         ComparisonField,
                                         ComparisonProfessionalSummary,
                                         ComparisonProjectItem,
                                         ComparisonPublicationItem,
                                         ComparisonWorkItem)
from models.input_cv_fields import AwardItem as OriginalAwardItem
from models.input_cv_fields import CVBody
from models.input_cv_fields import ProjectItem as OriginalProjectItem
from models.input_cv_fields import PublicationItem as OriginalPublicationItem
from models.input_cv_fields import WorkItem as OriginalWorkItem
from models.job_description_fields import JobDescriptionFields
from models.revised_cv_fields import (LLMResponse, RevisedAwardItem,
                                      RevisedCVResponseSchema,
                                      RevisedProjectItem,
                                      RevisedPublicationItem, RevisedWorkItem)
from templates.md_cv_template_to_llm import CV_TEMPLATE_LLM_MD
from templates.md_job_description_template import JOB_DESCRIPTION_TEMPLATE_MD
from utils.exceptions import ClientInitializationError, ResponseParsingError


def _create_comparison_field[T](
    original_value: T, suggested_value: Optional[T]
) -> ComparisonField[T]:
    return ComparisonField[T](original=original_value, suggested=suggested_value)


def _create_comparison_work_item(
    original_item: OriginalWorkItem, revised_suggestion: Optional[RevisedWorkItem]
) -> ComparisonWorkItem:
    return ComparisonWorkItem(
        id=original_item.id,
        summary=_create_comparison_field(
            original_item.summary,
            revised_suggestion.revised_summary if revised_suggestion else None,
        ),
        highlights=_create_comparison_field(
            original_item.highlights,
            revised_suggestion.revised_highlights if revised_suggestion else None,
        ),
        original_data=original_item,
    )


def _create_comparison_project_item(
    original_item: OriginalProjectItem, revised_suggestion: Optional[RevisedProjectItem]
) -> ComparisonProjectItem:
    return ComparisonProjectItem(
        id=original_item.id,
        summary=_create_comparison_field(
            original_item.summary,
            revised_suggestion.revised_summary if revised_suggestion else None,
        ),
        highlights=_create_comparison_field(
            original_item.highlights,
            revised_suggestion.revised_highlights if revised_suggestion else None,
        ),
        original_data=original_item,
    )


def _create_comparison_award_item(
    original_item: OriginalAwardItem, revised_suggestion: Optional[RevisedAwardItem]
) -> ComparisonAwardItem:
    return ComparisonAwardItem(
        id=original_item.id,
        summary=_create_comparison_field(
            original_item.summary,
            revised_suggestion.revised_summary if revised_suggestion else None,
        ),
        original_data=original_item,
    )


def _create_comparison_publication_item(
    original_item: OriginalPublicationItem,
    revised_suggestion: Optional[RevisedPublicationItem],
) -> ComparisonPublicationItem:
    return ComparisonPublicationItem(
        id=original_item.id,
        summary=_create_comparison_field(
            original_item.summary,
            revised_suggestion.revised_summary if revised_suggestion else None,
        ),
        original_data=original_item,
    )


OriginalItemT = TypeVar("OriginalItemT", bound=Any)
RevisedAISuggestionT = TypeVar("RevisedAISuggestionT", bound=Any)
ComparisonOutputT = TypeVar("ComparisonOutputT")


def _process_comparable_list(
    original_items: Optional[List[OriginalItemT]],
    ai_suggestions_list: Optional[List[RevisedAISuggestionT]],
    creator_func: Callable[
        [OriginalItemT, Optional[RevisedAISuggestionT]], ComparisonOutputT
    ],
    item_type_name: str = "Item",
) -> List[ComparisonOutputT]:
    comparison_results: List[ComparisonOutputT] = []
    if not original_items:
        return comparison_results

    ai_suggestions_map: Dict[str, RevisedAISuggestionT] = {}
    if ai_suggestions_list:
        for suggestion in ai_suggestions_list:
            if hasattr(suggestion, "id"):
                ai_suggestions_map[suggestion.id] = suggestion
            else:
                logger.warning(
                    f"AI suggestion for {item_type_name} missing 'id' attribute."
                )

    for original_item in original_items:
        if not hasattr(original_item, "id"):
            logger.warning(
                f"Original {item_type_name} missing 'id' attribute, cannot compare: {original_item}"
            )
            comparison_results.append(creator_func(original_item, None))
            continue

        corresponding_ai_suggestion = ai_suggestions_map.get(original_item.id)
        comparison_item = creator_func(original_item, corresponding_ai_suggestion)
        comparison_results.append(comparison_item)
        if corresponding_ai_suggestion:
            logger.debug(
                f"Compared {item_type_name} ID '{original_item.id}' with AI suggestion."
            )
        else:
            logger.debug(
                f"Included original {item_type_name} ID '{original_item.id}' (no AI suggestion)."
            )

    if ai_suggestions_list:
        original_item_ids = {item.id for item in original_items if hasattr(item, "id")}
        for suggestion in ai_suggestions_list:
            if hasattr(suggestion, "id") and suggestion.id not in original_item_ids:
                logger.warning(
                    f"AI suggestion for {item_type_name} ID '{suggestion.id}' did not match any original item."
                )

    return comparison_results


def create_comparison_cv(
    original_cv: CVBody, ai_suggestions: RevisedCVResponseSchema
) -> ComparisonCV:
    logger.info("Starting to create comparison CV structure.")

    compared_prof_title = _create_comparison_field(
        original_cv.header.professional_title, ai_suggestions.revised_professional_title
    )

    original_ps = original_cv.professional_summary
    revised_ps_suggestion = ai_suggestions.revised_professional_summary

    compared_ps = ComparisonProfessionalSummary(
        summary=_create_comparison_field(
            original_ps.summary,
            revised_ps_suggestion.summary if revised_ps_suggestion else None,
        ),
        objective=_create_comparison_field(
            original_ps.objective,
            revised_ps_suggestion.objective if revised_ps_suggestion else None,
        ),
        highlights=_create_comparison_field(
            original_ps.highlights,
            revised_ps_suggestion.highlights if revised_ps_suggestion else None,
        ),
    )

    compared_work_experience = _process_comparable_list(
        original_cv.work_experience,
        ai_suggestions.revised_work_experience,
        _create_comparison_work_item,
        "WorkExperience",
    )
    compared_projects = _process_comparable_list(
        original_cv.projects,
        ai_suggestions.revised_projects,
        _create_comparison_project_item,
        "Project",
    )
    compared_awards = _process_comparable_list(
        original_cv.awards,
        ai_suggestions.revised_awards,
        _create_comparison_award_item,
        "Award",
    )
    compared_publications = _process_comparable_list(
        original_cv.publications,
        ai_suggestions.revised_publications,
        _create_comparison_publication_item,
        "Publication",
    )

    return ComparisonCV(
        original_header=original_cv.header,
        professional_title=compared_prof_title,
        professional_summary=compared_ps,
        original_skills=original_cv.skills,
        suggested_skills=ai_suggestions.revised_skills,
        work_experience=(
            compared_work_experience if compared_work_experience else []
        ),
        projects=compared_projects if compared_projects else [],
        awards=compared_awards if compared_awards else None,
        publications=(
            compared_publications if compared_publications else None
        ),
        education=original_cv.education,
        certificates=original_cv.certificates,
        languages=original_cv.languages,
        ai_general_explanations=ai_suggestions.explanations,
        ai_suggestions=ai_suggestions.suggestions,
    )


def tailor_cv(original_cv: CVBody, job_description: JobDescriptionFields):
    cv_template = Template(CV_TEMPLATE_LLM_MD)
    job_description_template = Template(JOB_DESCRIPTION_TEMPLATE_MD)

    cv = cv_template.render(cv=original_cv)
    job_description_string: str = job_description_template.render(
        job_description_data=job_description
    )
    try:
        llm_data: LLMResponse = get_cv_improvements(job_description_string, cv)
        if not llm_data.response.usage_metadata:
            logger.error("LLMResponse received, but 'response' attribute is missing/empty.")
            raise ResponseParsingError("Internal error: LLM response was not found.")
        ai_suggestions: RevisedCVResponseSchema = llm_data.response.parsed
        if not isinstance(ai_suggestions, RevisedCVResponseSchema):
            logger.error(f"LLM response was not parsed into RevisedCVResponseSchema. Type: {type(ai_suggestions)}")
            raise TypeError("LLM response not parsed into expected schema after API call.")
    except ResponseParsingError as e:
        logger.error(f"Failed to parse LLM response: {e}")
        ai_suggestions = RevisedCVResponseSchema(explanations='An error occurred. Please try again later.')
        return create_comparison_cv(original_cv, ai_suggestions)
    except ClientInitializationError as e:
        logger.error(f"AI client initialization failed: {e}")
        raise
    except errors.APIError as e:
        logger.error(f"Google API error during CV improvements: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during get_cv_improvements: {e}")
        raise

    return create_comparison_cv(original_cv, ai_suggestions)
