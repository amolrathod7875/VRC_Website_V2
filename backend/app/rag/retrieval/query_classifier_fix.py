"""
Phase 9D — Retrieval Hardening Fixes

This module fixes the retrieval bugs identified in Phase 9C.7.
"""

from typing import Any, Dict, List, Optional
from app.rag.retrieval.query_classifier import classify_query, QueryIntent
from app.rag.product_identity import resolve_product_identity
from app.rag.constants import SOURCE_TYPE_CATALOGUE
from app.rag.config import rag_settings


# Product filter exceptions - products that should NOT have cross-product filtering
# These are products with independent specifications that don't conflict with others
CROSS_PRODUCT_FILTER_EXCEPTIONS = {
    "barrel-pump": "Barrel Pump has independent pressure ratio specifications",
    "dragon": "Dragon has independent PFP application data",
    "polyurea": "Polyurea has independent variant specifications",
    "tube-varnish-coating-system": "Tube varnish has independent component/workflow data",
    "vrc-mix-low-medium-pressure": "VRC MIX Low Medium has independent mixing ratio",
    "vrc-mix-hp": "VRC MIX HP has independent mixing ratio",
    "rhino": "Rhino has independent pressure ratio",
    "vria": "VRIA has independent pressure ratio",
}


def _should_apply_product_filter_improved(
    question: str,
    active_context: Optional[Dict[str, Optional[str]]],
    intent: QueryIntent,
) -> bool:
    """
    Improved product filter that excludes cross-product filtering for specific products.
    
    Fixes BARREL CROSS-CONTAMINATION and other cross-product bugs.
    """
    # Check active_context first
    if active_context and active_context.get("product_slug"):
        if intent.value in ("product_comparison", "governance"):
            return False
        if intent.value == "general_company":
            return False
        
        # Check if the product is in the exception list
        product_slug = active_context.get("product_slug")
        if product_slug in CROSS_PRODUCT_FILTER_EXCEPTIONS:
            return False
        
        resolved = resolve_product_identity(question)
        if resolved:
            if intent.value in ("product_comparison", "governance"):
                return False
            if intent.value == "general_company":
                return False
            normalized = f" {question.strip().lower()} "
            comparison_hints = [" compare ", " vs ", " versus ", "difference between "]
            if any(hint in normalized for hint in comparison_hints):
                return False
            return True
        return False
    
    # No active_context, check question for explicit product mention
    resolved = resolve_product_identity(question)
    if resolved:
        if intent.value in ("product_comparison", "governance"):
            return False
        if intent.value == "general_company":
            return False
        
        # Check if the product is in the exception list
        product_slug = resolved[0]
        if product_slug in CROSS_PRODUCT_FILTER_EXCEPTIONS:
            return False
        
        normalized = f" {question.strip().lower()} "
        comparison_hints = [" compare ", " vs ", " versus ", "difference between "]
        if any(hint in normalized for hint in comparison_hints):
            return False
        return True
    
    return False


def _get_intent_metadata_improved(intent: QueryIntent) -> dict:
    """
    Improved intent metadata that includes system content types.
    
    Fixes new content type retrieval issues.
    """
    base_metadata = {
        QueryIntent.GENERAL_COMPANY: {
            "prefer_sections": ["company overview", "about", "company profile", "canonical profile", "manufacturing", "business overview", "product portfolio"],
            "downrank_sections": ["change log", "governance", "unknown_register", "internal notes", "dataset goals", "document maintenance"],
            "prefer_source_types": ["company_master"],
        },
        QueryIntent.PRODUCT_COMPARISON: {
            "prefer_sections": ["technical_model", "description", "features", "applications", "technical specifications"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        },
        QueryIntent.PRODUCT_TECHNICAL: {
            "prefer_sections": ["technical specifications", "technical_model", "specifications"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue"],
        },
        QueryIntent.PRODUCT_APPLICATION: {
            "prefer_sections": ["applications", "technical specifications", "technical_model"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        },
        QueryIntent.PRODUCT_DISCOVERY: {
            "prefer_sections": ["applications", "technical specifications", "technical_model", "description", "features", "technical_variant", "system_component", "system_workflow", "system_comparison"],
            "downrank_sections": ["change log", "governance", "unknown_register", "full product master", "controlled search / seo terminology", "deployment / rag answering policy"],
            "prefer_source_types": ["catalogue"],
        },
        QueryIntent.CONTACT_LOCATION: {
            "prefer_sections": ["contact", "locations", "regional contacts", "head office"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["company_master"],
        },
        QueryIntent.GOVERNANCE: {
            "prefer_sections": ["unknown", "tbc", "governance", "data status", "register"],
            "downrank_sections": ["technical specifications", "company overview"],
            "prefer_source_types": ["company_master"],
        },
        QueryIntent.MODEL_IDENTIFIER: {
            "prefer_sections": ["technical specifications", "technical_model"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        },
        QueryIntent.CATALOGUE_REQUEST: {
            "prefer_sections": ["technical specifications", "technical_model", "specifications"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue"],
        },
    }
    
    return base_metadata.get(intent, {"prefer_sections": [], "downrank_sections": [], "prefer_source_types": []})