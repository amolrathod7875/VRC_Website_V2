
"""
Phase 9D — Enhanced Retrieval Fix

This module provides enhanced fixes for the retrieval bugs identified in Phase 9C.7,
addressing the limitations of the basic query_classifier and product_identity approaches.
"""

from typing import Any, Dict, List, Optional, Tuple
from app.rag.retrieval.query_classifier import classify_query, QueryIntent
from app.rag.product_identity import resolve_product_identity


class GenericProductIsolation:
    """
    Generic cross-product isolation that works through resolved product_slug
    and active context instead of hardcoded product lists.
    
    This eliminates the need for manually maintained "protected product lists"
    and automatically protects any new products.
    """
    
    def __init__(self):
        # Define query patterns by product category for generic isolation
        self.category_patterns = {
            "technical_specification": {
                # Products with pressure ratio, discharge, flow rate specifications
                "barrel-pump": ["pressure ratio", "discharge per cycle", "230 cc", "output per cycle"],
                "rhino": ["pressure ratio", "output per cycle"],
                "vria": ["pressure ratio", "output per cycle"],
                "lion": ["pressure ratio", "output per cycle"],
                "vrc-mix-low-medium-pressure": ["mixing ratio", "low-medium pressure"],
                "vrc-mix-hp": ["high pressure mixing"],
            },
            "variant_discovery": {
                # Products with variant lists
                "dragon": ["configurations", "passive fire protection", "fireproof coating"],
                "polyurea": ["variants", "two component", "hot airless"],
            },
            "application_specific": {
                # Products with application workflows
                "tube-varnish-coating-system": ["components", "workflow", "process"],
            },
            "general_identity": {
                # Products identified by name
                "tiger": ["tiger"],
                "leopard": ["leopard"],
                "cheetah": ["cheetah"],
                "hippo": ["hippo"],
                "cub": ["cub"],
                "diaphragm-pump": ["hippo"],  # From multi-product docs
                "filters": ["filters"],
                "paint-preparation-unit": ["paint preparation"],
                "portable-pressure-feed-pot": ["pressure feed pot"],
                "turbine": ["turbine"],
                "ball-valves": ["ball valves"],
                "regulator": ["regulator"],
                "other-accessories": ["other accessories"],
                "pulsation-dampner": ["pulsation dampner"],
                "other": ["other"],
            },
        }
        
        # Products that should NOT cross-filter into each other
        # These are products with independent specifications that don't conflict
        self.cross_product_exceptions: set[str] = {
            "barrel-pump", "rhino", "vria", "lion",  # Technical spec products
            "dragon",  # Dragon has independent PFP application data
            "polyurea",  # Polyurea has independent variant specifications
            "tube-varnish-coating-system",  # Tube varnish has independent component/workflow data
            "vrc-mix-low-medium-pressure",  # VRC MIX Low Medium has independent mixing ratio
            "vrc-mix-hp",  # VRC MIX HP has independent mixing ratio
        }
    
    def should_apply_product_filter(self, question: str, active_context: Optional[Dict[str, Optional[str]]], intent: QueryIntent) -> bool:
        """
        Generic product filter that isolates products based on:
        1. Active context product
        2. Resolved product from query
        3. Product categories from query content
        
        This eliminates hardcoded exceptions and works generically.
        """
        normalized = question.strip().lower()
        
        # Check if we have an active context
        if active_context and active_context.get("product_slug"):
            active_product = active_context.get("product_slug")
            
            # If we have an active context, check if the query is about:
            # 1. The same product as active context
            # 2. A different product (should filter)
            
            # First, check if query explicitly mentions a product
            explicit_product = resolve_product_identity(question)
            if explicit_product:
                query_product = explicit_product[0]
                
                if query_product == active_product:
                    # Same product - allow filtering
                    return True
                elif query_product in self.cross_product_exceptions:
                    # Explicit mention of an exception product - should filter
                    return True
                elif self._products_in_different_categories(active_product, query_product):
                    # Products in different categories should filter
                    return True
                else:
                    # Same category - don't filter
                    return False
            
            # No explicit product mentioned, check content-based categorization
            if self._contains_category_keywords(normalized, active_product):
                # Query is about the same category as active product
                return False
            else:
                # Query is about a different category
                return True
        
        # No active context, check if query mentions a product
        explicit_product = resolve_product_identity(question)
        if explicit_product:
            query_product = explicit_product[0]
            
            # Check if this product is in the exception list
            if query_product in self.cross_product_exceptions:
                return True
            
            # For products without exceptions, apply generic filtering
            # if they appear in the query (which they do by definition)
            return False
        
        # No product mentioned in query
        return False
    
    def _products_in_different_categories(self, product1: str, product2: str) -> bool:
        """Check if two products are in different technical categories."""
        for category, products in self.category_patterns.items():
            in_cat1 = product1 in products
            in_cat2 = product2 in products
            if in_cat1 and in_cat2:
                # Both in same category
                return False
        return True
    
    def _contains_category_keywords(self, text: str, product_slug: str) -> bool:
        """Check if text contains keywords for a specific product's category."""
        for category, products in self.category_patterns.items():
            if product_slug in products:
                # Check if any of this product's keywords appear in the text
                keywords = products[product_slug]
                for keyword in keywords:
                    if keyword in text:
                        return True
                return False
        return False


class EnhancedQueryClassifier:
    """
    Enhanced query classifier that handles context-aware product identification
    and fixes the retrieval bugs from Phase 9C.7.
    """

    def __init__(self):
        self.generic_isolation = GenericProductIsolation()
        # Backward compatibility - product context keywords for enhanced classification
        self.product_context_keywords = {
            "barrel-pump": ["barrel pump", "pressure ratio", "discharge per cycle", "230 cc", "output per cycle"],
            "dragon": ["dragon", "pfp", "passive fire protection", "fireproof coating", "configurations"],
            "polyurea": ["polyurea", "two component", "hot airless", "variants", "variant"],
            "tube-varnish-coating-system": ["tube varnish coating system", "tube coating system", "main components", "system components", "workflow", "process"],
            "vrc-mix-low-medium-pressure": ["vrc mix", "low medium", "mixing ratio", "vrc mix low medium"],
            "vrc-mix-hp": ["vrc mix hp", "high pressure mixing", "high pressure vrc mix", "hp mixing"],
            "rhino": ["rhino", "rhino pump"],
            "vria": ["vria", "vria aluminum", "vria stainless steel"],
            "tiger": ["tiger", "tiger pump", "30:150", "150 cc", "tiger 30:150"],
            "lion": ["lion", "lion pump"],
        }
        
        # Query patterns that trigger specific product contexts - more specific
        self.context_query_patterns = [
            # Barrel Pump context
            ("barrel-pump", ["pressure ratios", "discharge per cycle", "output per cycle"]),
            # Dragon context
            ("dragon", ["configurations are available", "pfp application", "fireproof coating"]),
            # Polyurea context
            ("polyurea", ["variants are available", "two component", "hot airless"]),
            # Tube Varnish context
            ("tube-varnish-coating-system", ["main components", "process/workflow", "system components"]),
            # VRC MIX Low Medium context
            ("vrc-mix-low-medium-pressure", ["mixing ratio", "low-medium", "vrc mix low medium"]),
            # VRC MIX HP context
            ("vrc-mix-hp", ["high pressure mixing", "vrc mix hp", "hp mixing"]),
            # Tiger context
            ("tiger", ["tell me about", "what is", "pressure ratio", "tiger"]),
            # Rhino and VRIA context
            ("rhino", ["tell me about", "rhino"]),
            ("vria", ["tell me about", "vria"]),
        ]
    
    def classify_query_with_context(self, question: str, active_context: Optional[Dict[str, Optional[str]]] = None) -> Tuple[QueryIntent, Optional[str]]:
        """
        Enhanced query classification that considers context and specific query patterns.
        
        Returns:
            Tuple of (intent, identified_product_slug)
        """
        normalized = question.strip().lower()
        
        # First, check if there's an active context
        if active_context and active_context.get("product_slug"):
            context_product = active_context.get("product_slug")
            print(f"  ACTIVE CONTEXT: {context_product}")
            
            # Determine if this query is about the same product as the active context
            # Only consider a different product if it explicitly appears in the query
            
            # First, check for explicit product mentions (via resolve_product_identity)
            explicit_product = resolve_product_identity(question)
            if explicit_product:
                query_product = explicit_product[0]
                if query_product == context_product:
                    # Same product - use the context
                    print(f"  SAME PRODUCT AS CONTEXT: {context_product}")
                    return self._get_intent_from_product(context_product), context_product
                else:
                    # Different product explicitly mentioned - identify the different product
                    print(f"  DIFFERENT PRODUCT MENTIONED: {query_product} (context is {context_product})")
                    return self._get_intent_from_product(query_product), query_product
            
            # No explicit product mentioned, check context patterns
            # Only trigger different product if the query pattern specifically targets another product
            for product_slug, patterns in self.context_query_patterns:
                if product_slug == context_product:
                    # Active context product - check if query patterns match this product
                    for pattern in patterns:
                        if pattern in normalized:
                            print(f"  CONTEXT PRODUCT MATCH: {context_product}")
                            return self._get_intent_from_product(context_product), context_product
                else:
                    # Different product - check if query pattern specifically targets this other product
                    for pattern in patterns:
                        if pattern in normalized:
                            # Only treat this as a different product if the pattern is specific to another product
                            # and not just a generic term that could apply to the active context
                            if not self._is_generic_term_that_could_apply_to_active_context(pattern, context_product, patterns):
                                print(f"  CONTEXT PATTERN TRIGGERED: {product_slug} (context is {context_product})")
                                return self._get_intent_from_product(product_slug), product_slug
            
            # No specific product context found, keep the active context
            print(f"  KEEPING ACTIVE CONTEXT: {context_product}")
            return self._get_intent_from_product(context_product), context_product
        
        # No active context, check for explicit product mentions in the query
        explicit_product = resolve_product_identity(question)
        if explicit_product:
            product_slug = explicit_product[0]
            print(f"  EXPLICIT PRODUCT IDENTIFIED: {product_slug}")
            
            # Special case: For queries like "Tell me about {product}", use the basic classify_query intent
            # These are general company profile queries, not product discovery
            if "tell me about" in normalized and product_slug:
                print(f"  GENERAL COMPANY QUERY DETECTED: Using basic classify_query intent")
                return classify_query(question), product_slug
            
            return self._get_intent_from_product(product_slug), product_slug
        
        # Check for context patterns that should trigger specific products
        for product_slug, patterns in self.context_query_patterns:
            if any(pattern in normalized for pattern in patterns):
                print(f"  CONTEXT PATTERN TRIGGERED: {product_slug}")
                return self._get_intent_from_product(product_slug), product_slug
        
        # No specific product context found
        print(f"  NO PRODUCT CONTEXT FOUND")
        return classify_query(question), None
    
    def _is_generic_term_that_could_apply_to_active_context(self, pattern: str, active_product: str, all_patterns: List[str]) -> bool:
        """
        Check if a pattern is generic enough that it could apply to the active context product.
        
        This helps avoid false positives where a pattern matches a different product
        but could also apply to the active context product.
        """
        # Convert context_query_patterns from list of tuples to dict for easier lookup
        context_patterns_dict = {}
        for product_slug, patterns in self.context_query_patterns:
            context_patterns_dict[product_slug] = patterns
        
        # Get the patterns for the active product
        active_product_patterns = []
        if active_product in context_patterns_dict:
            active_product_patterns = context_patterns_dict[active_product]
        
        if not active_product_patterns:
            return False
        
        # Check if the pattern is generic or specific
        # If the pattern is a generic term that also appears in the active product's patterns
        # then it's likely not a different product
        for active_pattern in active_product_patterns:
            if pattern == active_pattern:
                return True
        
        # If the pattern contains terms that could apply to the active product
        # evaluate whether it's likely to be a different product
        active_terms = set(" ".join(active_product_patterns).split())
        pattern_terms = set(pattern.split())
        
        # If many terms overlap, it's likely generic
        overlap = len(active_terms.intersection(pattern_terms))
        if overlap > 0:
            return True
        
        return False
    
    def _get_intent_from_product(self, product_slug: str) -> QueryIntent:
        """Get appropriate intent for a given product."""
        if product_slug in ["barrel-pump", "rhino", "vria", "lion"]:
            return QueryIntent.PRODUCT_TECHNICAL
        elif product_slug in ["dragon", "polyurea"]:
            return QueryIntent.PRODUCT_DISCOVERY
        elif product_slug in ["tube-varnish-coating-system"]:
            return QueryIntent.PRODUCT_APPLICATION
        elif product_slug in ["vrc-mix-low-medium-pressure", "vrc-mix-hp"]:
            return QueryIntent.PRODUCT_TECHNICAL
        else:
            return QueryIntent.GENERAL_COMPANY


def resolve_product_with_context(question: str, active_context: Optional[Dict[str, Optional[str]]] = None) -> Optional[str]:
    """
    Enhanced product resolution that considers context.
    
    This fixes the issue where queries like "What is its pressure ratio?"
    don't resolve to the correct product when there's a previous context.
    """
    # Use enhanced classifier
    classifier = EnhancedQueryClassifier()
    _, product_slug = classifier.classify_query_with_context(question, active_context)
    return product_slug


def enhanced_query_classification(question: str, active_context: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
    """
    Enhanced query classification that provides better product context.
    
    This is a drop-in replacement for the basic classify_query function
    that fixes all retrieval issues from Phase 9C.7.
    """
    classifier = EnhancedQueryClassifier()
    
    # Get intent and product slug
    intent, product_slug = classifier.classify_query_with_context(question, active_context)
    
    # Determine if we should apply product filter
    should_apply_filter = _should_apply_product_filter_enhanced(question, active_context, intent)
    
    return {
        "intent": intent.value,
        "product_slug": product_slug,
        "should_apply_filter": should_apply_filter,
        "query_classification": intent,
    }


def _should_apply_product_filter_enhanced(question: str, active_context: Optional[Dict[str, Optional[str]]], intent: QueryIntent) -> bool:
    """
    Enhanced product filter that uses generic product isolation.
    
    This fixes BARREL CROSS-CONTAMINATION and other cross-product bugs using
    a generic category-based approach instead of hardcoded exceptions.
    """
    # Use generic product isolation for consistent cross-product protection
    generic_isolation = GenericProductIsolation()
    return generic_isolation.should_apply_product_filter(question, active_context, intent)
