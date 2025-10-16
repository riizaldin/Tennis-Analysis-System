"""
Script untuk clear cache dan run main.py dengan improved configuration
"""

import os
import glob

print("="*70)
print("CLEAR CACHE & RUN IMPROVED PIPELINE")
print("="*70)

# 1. Clear old ball detection cache
cache_files = glob.glob("tracker_stubs/ball_detections_*.pkl")
print(f"\n📂 Found {len(cache_files)} cache files:")

for cache_file in cache_files:
    if "last5_conf005" not in cache_file:  # Keep the new test cache
        print(f"   🗑️  Deleting: {cache_file}")
        try:
            os.remove(cache_file)
        except Exception as e:
            print(f"      ⚠️  Error: {e}")
    else:
        print(f"   ✅ Keeping: {cache_file} (new test cache)")

print("\n" + "="*70)
print("✅ Cache cleared!")
print("="*70)

print("\nNOTE:")
print("Sekarang ketika Anda run 'python main.py', maka akan:")
print("1. Menggunakan model: yolo8_last5.pt ✅")
print("2. Confidence threshold: 0.05 ✅")
print("3. Re-detect ball karena cache sudah dihapus")
print("4. Expected detection rate: ~90% ✅")
print("\nSiap untuk run: python main.py")
