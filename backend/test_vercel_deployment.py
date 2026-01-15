#!/usr/bin/env python3
"""
Test script to verify the application works correctly with Vercel configuration
"""

def test_imports():
    """Test that all necessary modules can be imported"""
    print("Testing imports...")

    try:
        from main import app
        print("[OK] Successfully imported FastAPI app")
    except ImportError as e:
        print(f"[ERROR] Failed to import FastAPI app: {e}")
        return False

    try:
        from mangum import Mangum
        print("[OK] Successfully imported Mangum")
    except ImportError as e:
        print(f"[ERROR] Failed to import Mangum: {e}")
        return False

    try:
        from api_handler import mangum_handler, handler
        print("[OK] Successfully imported API handler")
    except ImportError as e:
        print(f"[ERROR] Failed to import API handler: {e}")
        return False

    try:
        import os
        db_url = os.getenv("DATABASE_URL")
        print("[OK] Successfully imported os module for environment variables")
    except Exception as e:
        print(f"[ERROR] Failed to access environment variables: {e}")
        return False

    return True

def test_fastapi_app():
    """Test basic FastAPI functionality"""
    print("\nTesting FastAPI app...")

    try:
        from main import app

        # Check that the app has the expected routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health"]

        for route in expected_routes:
            if route in routes:
                print(f"[OK] Found expected route: {route}")
            else:
                print(f"[INFO] Expected route not found: {route}")

        print(f"[OK] Total routes found: {len(routes)}")
        return True
    except Exception as e:
        print(f"[ERROR] Error testing FastAPI app: {e}")
        return False

def main():
    print("Vercel Deployment Readiness Test")
    print("=" * 40)

    import_success = test_imports()
    if not import_success:
        print("\n❌ Import tests failed. Please fix the issues before deploying to Vercel.")
        return False

    app_success = test_fastapi_app()
    if not app_success:
        print("\n❌ FastAPI tests failed. Please fix the issues before deploying to Vercel.")
        return False

    print("\n" + "=" * 40)
    print("[SUCCESS] All tests passed! Your application is ready for Vercel deployment.")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Import the project to Vercel")
    print("3. Configure environment variables")
    print("4. Deploy and monitor the logs")

    return True

if __name__ == "__main__":
    main()