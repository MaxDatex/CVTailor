from typing import Any, Callable, Dict, List, Optional, TypeVar

from loguru import logger

from src.core.models.comparison_cv_fields import (
    ComparisonAwardItem,
    ComparisonCV,
    ComparisonField,
    ComparisonProfessionalSummary,
    ComparisonProjectItem,
    ComparisonPublicationItem,
    ComparisonWorkItem,
)
from src.core.models.input_cv_fields import AwardItem as OriginalAwardItem
from src.core.models.input_cv_fields import CVBody
from src.core.models.input_cv_fields import ProjectItem as OriginalProjectItem
from src.core.models.input_cv_fields import PublicationItem as OriginalPublicationItem
from src.core.models.input_cv_fields import WorkItem as OriginalWorkItem
from src.core.models.revised_cv_fields import (
    RevisedAwardItem,
    RevisedCVResponseSchema,
    RevisedProjectItem,
    RevisedPublicationItem,
    RevisedWorkItem,
)

OriginalItemT = TypeVar("OriginalItemT", bound=Any)
RevisedAISuggestionT = TypeVar("RevisedAISuggestionT", bound=Any)
ComparisonOutputT = TypeVar("ComparisonOutputT")


class ComparisonCVBuilder:
    @staticmethod
    def _create_comparison_field[T](
        original_value: T, suggested_value: Optional[T]
    ) -> ComparisonField[T]:
        return ComparisonField[T](original=original_value, suggested=suggested_value)

    @staticmethod
    def _create_comparison_work_item(
        original_item: OriginalWorkItem, revised_suggestion: Optional[RevisedWorkItem]
    ) -> ComparisonWorkItem:
        return ComparisonWorkItem(
            id=original_item.id,
            summary=ComparisonCVBuilder._create_comparison_field(
                original_item.summary,
                revised_suggestion.revised_summary if revised_suggestion else None,
            ),
            highlights=ComparisonCVBuilder._create_comparison_field(
                original_item.highlights,
                revised_suggestion.revised_highlights if revised_suggestion else None,
            ),
            original_data=original_item,
        )

    @staticmethod
    def _create_comparison_project_item(
        original_item: OriginalProjectItem,
        revised_suggestion: Optional[RevisedProjectItem],
    ) -> ComparisonProjectItem:
        return ComparisonProjectItem(
            id=original_item.id,
            summary=ComparisonCVBuilder._create_comparison_field(
                original_item.summary,
                revised_suggestion.revised_summary if revised_suggestion else None,
            ),
            highlights=ComparisonCVBuilder._create_comparison_field(
                original_item.highlights,
                revised_suggestion.revised_highlights if revised_suggestion else None,
            ),
            original_data=original_item,
        )

    @staticmethod
    def _create_comparison_award_item(
        original_item: OriginalAwardItem, revised_suggestion: Optional[RevisedAwardItem]
    ) -> ComparisonAwardItem:
        return ComparisonAwardItem(
            id=original_item.id,
            summary=ComparisonCVBuilder._create_comparison_field(
                original_item.summary,
                revised_suggestion.revised_summary if revised_suggestion else None,
            ),
            original_data=original_item,
        )

    @staticmethod
    def _create_comparison_publication_item(
        original_item: OriginalPublicationItem,
        revised_suggestion: Optional[RevisedPublicationItem],
    ) -> ComparisonPublicationItem:
        return ComparisonPublicationItem(
            id=original_item.id,
            summary=ComparisonCVBuilder._create_comparison_field(
                original_item.summary,
                revised_suggestion.revised_summary if revised_suggestion else None,
            ),
            original_data=original_item,
        )

    @staticmethod
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
            original_item_ids = {
                item.id for item in original_items if hasattr(item, "id")
            }
            for suggestion in ai_suggestions_list:
                if hasattr(suggestion, "id") and suggestion.id not in original_item_ids:
                    logger.warning(
                        f"AI suggestion for {item_type_name} ID '{suggestion.id}' did not match any original item."
                    )
        return comparison_results

    def create_comparison_cv(
        self, original_cv: CVBody, ai_suggestions: RevisedCVResponseSchema
    ) -> ComparisonCV:
        logger.info("Starting to create comparison CV structure.")

        compared_prof_title = ComparisonCVBuilder._create_comparison_field(
            original_cv.header.professional_title,
            ai_suggestions.revised_professional_title,
        )

        original_ps = original_cv.professional_summary
        revised_ps_suggestion = ai_suggestions.revised_professional_summary

        compared_ps = ComparisonProfessionalSummary(
            summary=ComparisonCVBuilder._create_comparison_field(
                original_ps.summary,
                revised_ps_suggestion.summary if revised_ps_suggestion else None,
            ),
            highlights=ComparisonCVBuilder._create_comparison_field(
                original_ps.highlights,
                revised_ps_suggestion.highlights if revised_ps_suggestion else None,
            ),
        )

        compared_work_experience = ComparisonCVBuilder._process_comparable_list(
            original_cv.work_experience,
            ai_suggestions.revised_work_experience,
            ComparisonCVBuilder._create_comparison_work_item,
            "WorkExperience",
        )
        compared_projects = ComparisonCVBuilder._process_comparable_list(
            original_cv.projects,
            ai_suggestions.revised_projects,
            ComparisonCVBuilder._create_comparison_project_item,
            "Project",
        )
        compared_awards = ComparisonCVBuilder._process_comparable_list(
            original_cv.awards,
            ai_suggestions.revised_awards,
            ComparisonCVBuilder._create_comparison_award_item,
            "Award",
        )
        compared_publications = ComparisonCVBuilder._process_comparable_list(
            original_cv.publications,
            ai_suggestions.revised_publications,
            ComparisonCVBuilder._create_comparison_publication_item,
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
            publications=(compared_publications if compared_publications else None),
            education=original_cv.education,
            certificates=original_cv.certificates,
            languages=original_cv.languages,
            ai_general_explanations=ai_suggestions.explanations,
            ai_suggestions=ai_suggestions.suggestions,
        )
