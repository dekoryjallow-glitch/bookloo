"""
Direct HTTP test of the init->approve flow to capture exact errors.
"""
import httpx
import json
import asyncio
import time

API_BASE = "http://localhost:8000"

async def test_full_flow():
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: Init Book
        print("=" * 60)
        print("Step 1: Initialize Book")
        print("=" * 60)
        
        init_payload = {
            "child_name": "Max",
            "theme": "space",
            "child_photo_url": "https://firebasestorage.googleapis.com/dummy.jpg",
            "user_id": "test-user-123",
            "style": "pixar_3d",
        }
        
        try:
            resp = await client.post(f"{API_BASE}/api/books/init", json=init_payload)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
            
            if resp.status_code != 200:
                print("   ❌ Init failed!")
                return
                
            data = resp.json()
            book_id = data["id"]
            print(f"   ✅ Book created: {book_id}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Wait for character generation
        print("\n" + "=" * 60)
        print("Step 2: Wait for Character Generation")
        print("=" * 60)
        
        for i in range(30):  # Max 30 attempts (30 seconds)
            await asyncio.sleep(1)
            try:
                resp = await client.get(f"{API_BASE}/api/books/{book_id}/status")
                status_data = resp.json()
                status = status_data.get("status")
                print(f"   [{i+1}s] Status: {status}")
                
                if status == "waiting_for_approval":
                    print(f"   ✅ Character ready!")
                    break
                elif status == "failed":
                    print(f"   ❌ Character generation FAILED!")
                    return
            except Exception as e:
                print(f"   ⚠️ Poll error: {e}")
        
        # Step 3: Approve Character
        print("\n" + "=" * 60)
        print("Step 3: Approve Character")
        print("=" * 60)
        
        try:
            resp = await client.post(f"{API_BASE}/api/books/{book_id}/approve")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
            
            if resp.status_code != 200:
                print("   ❌ Approve failed!")
                return
                
            print("   ✅ Approval request sent!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Step 4: Wait for preview generation
        print("\n" + "=" * 60)
        print("Step 4: Wait for Preview Generation")
        print("=" * 60)
        
        for i in range(120):  # Max 2 minutes for scene generation
            await asyncio.sleep(2)
            try:
                resp = await client.get(f"{API_BASE}/api/books/{book_id}/status")
                status_data = resp.json()
                status = status_data.get("status")
                progress = status_data.get("progress", 0)
                print(f"   [{i*2}s] Status: {status}, Progress: {progress}%")
                
                if status == "ready_for_purchase":
                    print(f"   ✅ Preview ready!")
                    print(f"   Preview images: {status_data.get('preview_images', [])}")
                    break
                elif status == "failed":
                    print(f"   ❌ Preview generation FAILED!")
                    return
            except Exception as e:
                print(f"   ⚠️ Poll error: {e}")
        
        print("\n" + "=" * 60)
        print("✅ FULL FLOW COMPLETED!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_full_flow())
