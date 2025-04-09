#!/usr/bin/env python
"""
Candidate Self-Evaluation Test Script

This script helps candidates test their implementation of the AI-Powered Product 
Description Generator by running a series of basic tests on both the backend API
and the content generation quality.

Usage:
    python candidate_test.py

Requirements:
    - Your FastAPI server must be running on http://localhost:5000
    - You must have requests and pytest libraries installed
"""

import json
import requests
import time
import sys

API_BASE_URL = "http://localhost:5000/api"

def print_header(message):
    print("\n" + "="*80)
    print(f" {message}")
    print("="*80)

def print_result(test_name, result, message=None):
    status = "✅ PASSED" if result else "❌ FAILED"
    print(f"{status} - {test_name}")
    if message and not result:
        print(f"  → {message}")

def test_api_availability():
    """Test that the API is available and responding"""
    try:
        response = requests.get(f"{API_BASE_URL}/products")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def test_products_endpoint():
    """Test that the products endpoint returns the expected data structure"""
    try:
        response = requests.get(f"{API_BASE_URL}/products")
        data = response.json()
        
        # Check that we have a list of products
        if not isinstance(data, list):
            return False, "Expected a list of products"
        
        # Check that we have at least 10 products
        if len(data) < 10:
            return False, "Expected at least 10 products"
        
        # Check that each product has the required fields
        required_fields = ["id", "name", "price", "brand"]
        for product in data[:5]:  # Check the first 5 products
            for field in required_fields:
                if field not in product:
                    return False, f"Product missing required field: {field}"
        
        return True, None
    except Exception as e:
        return False, str(e)

def test_generate_content_endpoint():
    """Test that the generate-content endpoint works with basic request"""
    try:
        # Create a simple test request
        product_id = "prod001"  # First product from sample data
        
        request_data = {
            "product_id": product_id,
            "content_types": ["product_description"],
            "style": {
                "tone": "professional",
                "length": "medium",
                "audience": "general",
                "keywords": []
            }
        }
        
        response = requests.post(f"{API_BASE_URL}/generate-content", json=request_data)
        
        # Check response status
        if response.status_code != 200:
            return False, f"Expected status code 200, got {response.status_code}"
        
        data = response.json()
        
        # Check that we have the right structure
        if "product" not in data:
            return False, "Response missing 'product' field"
            
        if "generated_content" not in data:
            return False, "Response missing 'generated_content' field"
            
        if "product_description" not in data["generated_content"]:
            return False, "Response missing 'product_description' in generated_content"
        
        return True, None
    except Exception as e:
        return False, str(e)

def test_seo_content_generation():
    """Test that SEO content generation works"""
    try:
        # Create a test request for SEO content
        product_id = "prod002"  # Second product from sample data
        
        request_data = {
            "product_id": product_id,
            "content_types": ["seo"],
            "style": {
                "tone": "professional",
                "length": "medium",
                "audience": "general",
                "keywords": ["premium", "audio", "wireless"]
            }
        }
        
        response = requests.post(f"{API_BASE_URL}/generate-content", json=request_data)
        data = response.json()
        
        # Check that SEO content has the right structure
        if "seo" not in data.get("generated_content", {}):
            return False, "Response missing 'seo' in generated_content"
            
        seo_content = data["generated_content"]["seo"]
        
        if "title" not in seo_content:
            return False, "SEO content missing 'title'"
            
        if "description" not in seo_content:
            return False, "SEO content missing 'description'"
            
        # Check SEO title length
        if len(seo_content["title"]) < 30 or len(seo_content["title"]) > 70:
            return False, f"SEO title length ({len(seo_content['title'])}) outside recommended range (30-70 characters)"
            
        # Check SEO description length
        if len(seo_content["description"]) < 120 or len(seo_content["description"]) > 160:
            return False, f"SEO description length ({len(seo_content['description'])}) outside recommended range (120-160 characters)"
        
        return True, None
    except Exception as e:
        return False, str(e)

def test_missing_fields_generation():
    """Test that missing fields generation works"""
    try:
        # Create a test request for a product with missing fields
        product_id = "prod004"  # Product with missing fields
        
        request_data = {
            "product_id": product_id,
            "content_types": ["missing_fields"],
            "style": {
                "tone": "professional",
                "length": "medium",
                "audience": "general"
            }
        }
        
        response = requests.post(f"{API_BASE_URL}/generate-content", json=request_data)
        data = response.json()
        
        # Check that missing fields content has been generated
        if "missing_fields" not in data.get("generated_content", {}):
            return False, "Response missing 'missing_fields' in generated_content"
            
        missing_fields = data["generated_content"]["missing_fields"]
        
        # Check that at least some fields have been generated
        if len(missing_fields) == 0:
            return False, "No missing fields were generated"
        
        return True, None
    except Exception as e:
        return False, str(e)

def test_complete_product_endpoint():
    """Test that the complete-product endpoint works"""
    try:
        # Create a test request with partial product data
        partial_product = {
            "name": "Test Custom Bluetooth Speaker",
            "price": 79.99,
            "brand": "AudioTest",
            "basic_description": "A portable speaker with great sound quality."
        }
        
        request_data = {
            "product_data": partial_product
        }
        
        response = requests.post(f"{API_BASE_URL}/complete-product", json=request_data)
        
        # Check response status
        if response.status_code != 200:
            return False, f"Expected status code 200, got {response.status_code}"
        
        data = response.json()
        
        # Check that we have the right structure
        if "original_product" not in data:
            return False, "Response missing 'original_product' field"
            
        if "completed_product" not in data:
            return False, "Response missing 'completed_product' field"
        
        # Check that completed product has more fields than original
        original_fields = set(data["original_product"].keys())
        completed_fields = set(data["completed_product"].keys())
        
        if not completed_fields.issuperset(original_fields):
            return False, "Completed product is missing some original fields"
            
        if len(completed_fields) <= len(original_fields):
            return False, "Completed product doesn't have any new fields"
        
        # Check that important fields have been added
        important_fields = ["category", "features", "tags"]
        missing_important_fields = [field for field in important_fields if field not in completed_fields]
        
        if missing_important_fields:
            return False, f"Completed product missing important fields: {', '.join(missing_important_fields)}"
        
        return True, None
    except Exception as e:
        return False, str(e)

def test_image_generation():
    """Test that product image generation works"""
    try:
        # Create a test request for image generation
        product_data = {
            "name": "Premium Wireless Headphones",
            "price": 199.99,
            "brand": "SoundTech",
            "category": "Electronics",
            "subcategory": "Audio",
            "colors": ["Black"],
            "materials": ["Premium leather", "Aluminum"]
        }
        
        style_options = {
            "background": "white",
            "lighting": "studio",
            "angle": "front"
        }
        
        request_data = {
            "product_data": product_data,
            "style": style_options
        }
        
        response = requests.post(f"{API_BASE_URL}/generate-image", json=request_data)
        
        # Check response status
        if response.status_code != 200:
            return False, f"Expected status code 200, got {response.status_code}"
        
        data = response.json()
        
        # Check that we have the right structure
        if "image_result" not in data:
            return False, "Response missing 'image_result' field"
            
        image_result = data["image_result"]
        
        if "image_url" not in image_result:
            return False, "Image result missing 'image_url'"
            
        if "prompt" not in image_result:
            return False, "Image result missing 'prompt'"
        
        # Verify that the prompt contains critical product information
        prompt = image_result["prompt"]
        if "Premium Wireless Headphones" not in prompt:
            return False, "Prompt doesn't include product name"
            
        if "SoundTech" not in prompt:
            return False, "Prompt doesn't include brand name"
            
        if "Electronics" not in prompt or "Audio" not in prompt:
            return False, "Prompt doesn't include category information"
        
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print_header("AI-Powered Product Description Generator - Self-Evaluation Test")
    
    # Test API availability
    api_available = test_api_availability()
    print_result("API Availability", api_available, 
                "API not available. Make sure your FastAPI server is running on http://localhost:5000")
    
    if not api_available:
        print("\nCannot proceed with tests as the API is not available.")
        print("Please make sure your FastAPI server is running before executing this test script.")
        sys.exit(1)
    
    # Test products endpoint
    products_result, products_message = test_products_endpoint()
    print_result("Products Endpoint", products_result, products_message)
    
    # Test generate-content endpoint
    generate_content_result, generate_content_message = test_generate_content_endpoint()
    print_result("Generate Content Endpoint", generate_content_result, generate_content_message)
    
    # Test SEO content generation
    seo_result, seo_message = test_seo_content_generation()
    print_result("SEO Content Generation", seo_result, seo_message)
    
    # Test missing fields generation
    missing_fields_result, missing_fields_message = test_missing_fields_generation()
    print_result("Missing Fields Generation", missing_fields_result, missing_fields_message)
    
    # Test complete-product endpoint
    complete_product_result, complete_product_message = test_complete_product_endpoint()
    print_result("Complete Product Endpoint", complete_product_result, complete_product_message)
    
    # Test image generation
    image_generation_result, image_generation_message = test_image_generation()
    print_result("Image Generation", image_generation_result, image_generation_message)
    
    # Summary
    print("\n" + "-"*80)
    tests_passed = sum([
        api_available, 
        products_result, 
        generate_content_result, 
        seo_result,
        missing_fields_result,
        complete_product_result,
        image_generation_result
    ])
    total_tests = 7
    
    print(f"Tests passed: {tests_passed}/{total_tests} ({tests_passed/total_tests*100:.0f}%)")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! Your implementation meets the basic requirements.")
    else:
        print("\n⚠️  Some tests failed. Review the output above to see what needs improvement.")
    
    print("\nNote: This is just a basic test script. The actual evaluation will be more thorough.")
    print("Make sure to thoroughly test your prompt engineering and user experience beyond these tests.")

if __name__ == "__main__":
    main()