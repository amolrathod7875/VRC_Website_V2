#!/usr/bin/env python3
"""
Simplified Phase 9D Verification Script

This script tests the current Phase 9D implementation
and identifies the verification failures.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.enhanced_query_classifier import enhanced_query_classification


def test_all_phase9d_cases():
    """Test all Phase 9D verification cases."""
    print("="*80)
    print("PHASE 9D VERIFICATION - CURRENT IMPLEMENTATION")
    print("="*80)
    
    # Define all Phase 9D verification cases (simplified)
    test_cases = [
        {
            "name": "BARREL CROSS-CONTAMINATION",
            "query": "What pressure ratios?",
            "context": {"product_slug": "barrel-pump"},
            "expected_product": "barrel-pump",
            "expected_intent": "product_technical",
        },
        {
            "name": "BARREL TECHNICAL RETRIEVAL", 
            "query": "What is the discharge per cycle?",
            "context": None,
            "expected_product": "barrel-pump",
            "expected_intent": "product_technical",
        },
        {
            "name": "DRAGON CONFIGURATION RETRIEVAL",
            "query": "What configurations are available for Dragon?",
            "context": None,
            "expected_product": "dragon",
            "expected_intent": "product_discovery",
        },
        {
            "name": "POLYUREA VARIANT RETRIEVAL",
            "query": "What variants are available?",
            "context": {"product_slug": "polyurea"},
            "expected_product": "polyurea",
            "expected_intent": "product_discovery",
        },
        {
            "name": "TUBE VARNISH COMPONENT/WORKFLOW",
            "query": "What are the main components?",
            "context": {"product_slug": "tube-varnish-coating-system"},
            "expected_product": "tube-varnish-coating-system",
            "expected_intent": "product_application",
        },
        {
            "name": "VRC MIX LOW-MEDIUM",
            "query": "Mixing ratio range?",
            "context": {"product_slug": "vrc-mix-low-medium-pressure"},
            "expected_product": "vrc-mix-low-medium-pressure",
            "expected_intent": "product_technical",
        },
        {
            "name": "NEW CONTENT TYPES",
            "query": "What variants are available?",
            "context": None,
            "expected_product": "polyurea",
            "expected_intent": "product_discovery",
        },
        {
            "name": "NEW SYSTEM CONTEXT",
            "query": "What is the mixing ratio?",
            "context": {"product_slug": "vrc-mix-hp"},
            "expected_product": "polyurea",
            "expected_intent": "product_discovery",
        },
        {
            "name": "BARREL → TIGER SWITCH",
            "query": "What is its pressure ratio?",
            "context": {"product_slug": "tiger"},
            "expected_product": "barrel-pump",
            "expected_intent": "product_technical",
        },
        {
            "name": "RHINO AND VRIA REGRESSION",
            "query": "Tell me about Rhino",
            "context": None,
            "expected_product": "rhino",
            "expected_intent": "product_technical",
        },
        {
            "name": "PRODUCT DISCOVERY",
            "query": "Systems for fireproof coating?",
            "context": None,
            "expected_product": "dragon",
            "expected_intent": "product_discovery",
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTEST {i}: {case['name']}")
        print(f"Query: '{case['query']}'")
        print(f"Context: {case['context']}")
        
        result = enhanced_query_classification(case['query'], case['context'])
        
        print(f"Actual: product='{result['product_slug']}', intent='{result['intent']}'")
        
        # Check if test passed
        product_match = result['product_slug'] == case['expected_product']
        intent_match = result['intent'] == case['expected_intent']
        
        test_passed = product_match and intent_match
        
        if test_passed:
            print(f"✓ PASS")
            passed += 1
        else:
            print(f"✗ FAIL")
            if not product_match:
                print(f"  Product mismatch: expected '{case['expected_product']}', got '{result['product_slug']}'")
            if not intent_match:
                print(f"  Intent mismatch: expected '{case['expected_intent']}', got '{result['intent']}'")
            failed += 1
    
    print(f"\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed/len(test_cases)*100:.1f}%")
    
    return passed, failed


if __name__ == "__main__":
    print("Phase 9D Verification - Current Implementation")
    passed, failed = test_all_phase9d_cases()
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ Phase 9D retrieval hardening successfully implemented")
        print("✅ All verification cases passed")
        print("✅ Phase 9 is production-safe to close")
    else:
        print(f"\n❌ {failed} TESTS FAILED")
        print("Phase 9D requires further fixes.")
    
    sys.exit(0 if failed == 0 else 1)