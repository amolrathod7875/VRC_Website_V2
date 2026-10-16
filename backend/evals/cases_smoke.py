"""Smoke test cases for fast evaluation."""
from __future__ import annotations

from evals.case_schema import case as c

CASES = [
    c('smoke-01', 'identity', 'What is Tiger?', expected_product_slug='tiger', expected_document_names=['Tiger.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-02', 'identity', 'What is Dragon?', expected_product_slug='dragon', expected_document_names=['dragon.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-03', 'identity', 'What is Polyurea?', expected_product_slug='polyurea', expected_document_names=['polyurea.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-04', 'identity', 'What is VRIA?', expected_product_slug='vria', expected_document_names=['AUTOMATIC_gun.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-05', 'identity', 'What is VRC MIX Low-Medium?', expected_product_slug='vrc-mix-low-medium-pressure', expected_document_names=['VRC MIX (LOW - MEDIUM) PRESSURE.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-06', 'identity', 'What is LION?', expected_product_slug='lion', expected_document_names=['LION_Catalogue.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-07', 'identity', 'What is Rhino?', expected_product_slug='rhino', expected_document_names=['rhino.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-08', 'identity', 'What is Barrel Pump?', expected_product_slug='barrel-pump', expected_document_names=['Barrel Pump.pdf'], expected_intent='general_company', severity='HIGH'),
    c('smoke-09', 'technical', 'What is the pressure ratio of Tiger 30:150?', expected_product_slug='tiger', expected_model='30:150', expected_document_names=['Tiger.pdf'], expected_required_facts=['30:1'], severity='HIGH'),
    c('smoke-10', 'technical', 'What is the output per cycle of Tiger 30:150?', expected_product_slug='tiger', expected_model='30:150', expected_document_names=['Tiger.pdf'], expected_required_facts=['150 cc'], severity='HIGH'),
    c('smoke-11', 'technical', 'What is the pressure ratio of LION?', expected_product_slug='lion', expected_document_names=['LION_Catalogue.pdf'], expected_required_facts=['0.14:1'], severity='HIGH'),
    c('smoke-12', 'table', 'CUB 2:400 pressure ratio', expected_product_slug='cub', expected_model='2:400', expected_document_names=['cub.pdf'], expected_required_facts=['2:1'], severity='HIGH'),
    c('smoke-13', 'multi-product', 'Which products are available from VR Coatings?', expected_document_names=[], expected_required_facts=[], severity='MEDIUM'),
    c('smoke-14', 'discovery', 'What products are available?', expected_intent='product_discovery', severity='MEDIUM'),
]
