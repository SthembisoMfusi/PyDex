#!/usr/bin/env python3
"""
Simple test script for PyDex
This script helps verify that PyDex is working correctly.
"""

import subprocess
import sys
import os

def run_pokedex(pokemon_name):
    """Run PyDex with a given Pokémon name and return the output."""
    try:
        result = subprocess.run(
            [sys.executable, "pokedex.py", pokemon_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout: Command took too long to execute"
    except Exception as e:
        return -1, "", str(e)

def test_pokemon(pokemon_name, expected_in_output=None):
    """Test PyDex with a specific Pokémon."""
    print(f"🧪 Testing with {pokemon_name}...")
    
    returncode, stdout, stderr = run_pokedex(pokemon_name)
    
    if returncode == 0:
        print(f"✅ {pokemon_name} test passed!")
        if expected_in_output:
            if expected_in_output.lower() in stdout.lower():
                print(f"✅ Found expected output: '{expected_in_output}'")
            else:
                print(f"⚠️  Expected '{expected_in_output}' not found in output")
        print(f"   Output: {stdout.strip()}")
    else:
        print(f"❌ {pokemon_name} test failed!")
        print(f"   Error: {stderr.strip()}")
    
    print()
    return returncode == 0

def main():
    print("🧪 Running PyDex tests...")
    print()
    
    # Check if pokedex.py exists
    if not os.path.exists("pokedex.py"):
        print("❌ pokedex.py not found! Make sure you're in the right directory.")
        sys.exit(1)
    
    # Test cases
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Valid Pokémon (Pikachu)
    total_tests += 1
    if test_pokemon("pikachu", "Pikachu"):
        tests_passed += 1
    
    # Test 2: Valid Pokémon with multiple types (Charizard)
    total_tests += 1
    if test_pokemon("charizard", "Charizard"):
        tests_passed += 1
    
    # Test 3: Invalid Pokémon (should show error)
    print("🧪 Testing with invalid Pokémon...")
    returncode, stdout, stderr = run_pokedex("fake-pokemon")
    total_tests += 1
    if returncode == 0 and "not found" in stdout.lower():
        print("✅ Invalid Pokémon test passed!")
        print(f"   Output: {stdout.strip()}")
        tests_passed += 1
    else:
        print("❌ Invalid Pokémon test failed!")
        print(f"   Expected error message, got: {stdout.strip()}")
    print()
    
    # Test 4: No arguments (should show usage)
    print("🧪 Testing with no arguments...")
    try:
        result = subprocess.run(
            [sys.executable, "pokedex.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        total_tests += 1
        if result.returncode != 0 and "usage" in result.stdout.lower():
            print("✅ No arguments test passed!")
            print(f"   Output: {result.stdout.strip()}")
            tests_passed += 1
        else:
            print("❌ No arguments test failed!")
            print(f"   Expected usage message, got: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ No arguments test failed with exception: {e}")
        total_tests += 1
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"   Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! PyDex is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
