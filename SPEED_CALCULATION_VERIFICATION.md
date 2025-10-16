# Verifikasi Perhitungan Speed di Tennis Analysis System

## Perhitungan Ball Shot Speed

### Formula yang digunakan:
```python
ball_shot_time_in_seconds = (end_frame - start_frame) / 30.0  # Assuming 30 FPS
distance_covered_meters = convert_pixel_distance_to_meters(distance_covered_pixels, ...)
speed_of_ball_shot = distance_covered_meters / ball_shot_time_in_seconds * 3.6
```

### Analisis:
1. **Waktu (Time)**: 
   - `(end_frame - start_frame) / FPS` = waktu dalam detik ✅
   - Contoh: (90 - 60) / 30 = 1 detik

2. **Jarak (Distance)**:
   - `distance_covered_pixels` = jarak pixel di mini court
   - `convert_pixel_distance_to_meters()` = konversi ke meter ✅
   - Menggunakan DOUBLE_LINE_WIDTH (23.77m) sebagai referensi

3. **Kecepatan (Speed)**:
   - `distance_covered_meters / ball_shot_time_in_seconds` = m/s
   - `m/s * 3.6` = km/h ✅
   - Rumus: 1 m/s = 3.6 km/h

### Contoh Perhitungan:
Jika bola bergerak 10 meter dalam 0.5 detik:
- Speed = 10 / 0.5 = 20 m/s
- Speed = 20 * 3.6 = 72 km/h ✅

## Perhitungan Player Speed (Opponent)

### Formula yang digunakan:
```python
distance_covered_pixels_opponent = measure_distance(
    player_mini_court_detections[start_frame][opponent_player_id],
    player_mini_court_detections[end_frame][opponent_player_id]
)
distance_covered_meters_opponent = convert_pixel_distance_to_meters(...)
speed_of_opponent_player = distance_covered_meters_opponent / ball_shot_time_in_seconds * 3.6
```

### Analisis:
- Sama seperti ball speed, tapi untuk player ✅
- Menggunakan waktu yang sama (ball_shot_time) ✅
- Mengukur jarak yang ditempuh player saat bola di-hit

## FPS Issue - PERHATIAN! ⚠️

### Masalah Potensial:
```python
ball_shot_time_in_seconds = (end_frame - start_frame) / 30.0  # Assuming 30 FPS
```

**HARDCODED 30 FPS!** Ini bisa jadi masalah jika video bukan 30 FPS.

### Solusi:
Harus menggunakan FPS aktual dari video:
```python
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
ball_shot_time_in_seconds = (end_frame - start_frame) / fps
```

## Kesimpulan:

✅ **BENAR**: Formula perhitungan speed sudah tepat (m/s * 3.6 = km/h)
✅ **BENAR**: Konversi pixel ke meter menggunakan referensi yang benar
⚠️ **PERLU DIPERBAIKI**: FPS hardcoded di 30, harus dinamis

## Nilai Speed yang Wajar untuk Tenis:

### Ball Speed:
- **Servis Profesional**: 150-250 km/h
- **Groundstroke**: 80-130 km/h
- **Volley**: 60-100 km/h
- **Drop shot**: 30-60 km/h

### Player Speed:
- **Sprint**: 15-30 km/h
- **Normal movement**: 5-15 km/h
- **Positioning**: 1-8 km/h

Jika hasil perhitungan jauh dari range ini, kemungkinan masalah:
1. FPS tidak sesuai (30 vs actual)
2. Court keypoint detection tidak akurat
3. Ball/player detection error
