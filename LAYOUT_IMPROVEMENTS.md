# 🎨 Layout Improvements - Mini Court & Stats Box

## 📊 Changes Made

### 1. **Mini Court Size Reduction**

**File**: `mini_court/mini_court.py`

**Before:**
```python
self.drawing_rectangle_width = 180
self.drawing_rectangle_height = 360
self.buffer = 40
self.padding_court = 15
self.baseline_extension = 30
```

**After:**
```python
self.drawing_rectangle_width = 150  # ↓ 17% smaller
self.drawing_rectangle_height = 300  # ↓ 17% smaller
self.buffer = 30                     # ↓ 25% smaller
self.padding_court = 12              # ↓ 20% smaller
self.baseline_extension = 25         # ↓ 17% smaller
```

**Result:**
- Mini court sekarang ~17% lebih kecil
- Tidak memakan banyak ruang di layar
- Masih tetap jelas dan readable

---

### 2. **Stats Box Repositioning**

**File**: `utils/player_stats_drawer_utils.py`

**Before:**
```python
width = 350
height = 230

# Position: bottom-right corner
start_x = frame.shape[1] - 400  # From right edge
start_y = frame.shape[0] - 500  # From bottom edge
```

**After:**
```python
width = 320   # Slightly smaller
height = 210  # Slightly smaller

# Position: top-left corner, below mini court
start_x = 40   # Align with mini court
start_y = 370  # Below mini court (50 + 300 + 20 margin)
```

**Layout Calculation:**
```
Mini Court:
- Position: (50, 50)
- Height: ~300 pixels (with buffer)
- Bottom edge: ~350

Stats Box:
- Position: (40, 370)
- Margin from mini court: 20 pixels
- Aligned vertically on left side
```

---

## 🎯 Visual Layout

```
┌─────────────────────────────────────────┐
│                                         │
│  ┌───────────┐                         │
│  │ MINI      │                         │
│  │ COURT     │  ← Smaller (150×300)   │
│  │           │                         │
│  │           │                         │
│  │           │                         │
│  └───────────┘                         │
│                                         │
│  ┌─────────────────┐                   │
│  │ PLAYER STATS    │  ← Below mini     │
│  │ Player 1  P2    │     court         │
│  │ Shot Speed...   │                   │
│  │ Player Speed... │                   │
│  │ Avg speeds...   │                   │
│  └─────────────────┘                   │
│                                         │
│         MAIN VIDEO VIEW                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📐 Exact Coordinates

### Mini Court:
- **X**: 50 (left padding)
- **Y**: 50 (top padding)
- **Width**: 150 pixels
- **Height**: 300 pixels

### Stats Box:
- **X**: 40 (slightly inset from left)
- **Y**: 370 (50 + 300 + 20 margin)
- **Width**: 320 pixels
- **Height**: 210 pixels

### Total Vertical Space Used:
- Mini court: 50 → 350 (300px)
- Gap: 20px
- Stats box: 370 → 580 (210px)
- **Total**: ~580 pixels from top

---

## ✅ Benefits

1. **Less Screen Real Estate** 📺
   - Mini court 17% smaller
   - Stats box slightly smaller (320×210 vs 350×230)
   - More space for main video view

2. **Better Organization** 📋
   - Both elements grouped together on left side
   - Vertical stacking (mini court → stats)
   - Clean, organized layout

3. **Improved Readability** 👁️
   - Stats box not in bottom-right (often has important action)
   - Left side typically less critical in tennis videos
   - All info in one glance area

4. **Professional Look** ✨
   - Aligned left margins (40-50px)
   - Consistent spacing (20px gap)
   - Balanced proportions

---

## 🎨 Stats Box Content

**Displayed Metrics:**
```
     Player 1     Player 2
Shot Speed      XX.X km/h    XX.X km/h
Player Speed    XX.X km/h    XX.X km/h
avg. S. Speed   XX.X km/h    XX.X km/h
avg. P. Speed   XX.X km/h    XX.X km/h
```

**Font Sizes:**
- Header: 0.55 (white, bold)
- Labels: 0.45 (white, normal)
- Values: 0.50 (white, bold)

---

## 🔍 Code Changes Summary

### `mini_court.py` (Line 18-25):
- Reduced all dimensions by ~17-25%
- Maintains aspect ratio
- Preserves functionality

### `player_stats_drawer_utils.py` (Line 15-28):
- Changed from dynamic bottom-right positioning
- Fixed top-left positioning below mini court
- Reduced box size slightly
- Adjusted text positions proportionally

---

## 🚀 Testing

To verify changes work correctly:

```bash
cd c:\KULIAH\SKRIPSI\tennis_analysis
python main.py
```

**Check:**
- ✅ Mini court appears smaller in top-left
- ✅ Stats box appears below mini court
- ✅ Both elements aligned on left side
- ✅ Text in stats box is readable
- ✅ Player/ball dots visible on mini court
- ✅ No overlap with main video content

---

## 📊 Before vs After Comparison

| Element | Before | After | Change |
|---------|--------|-------|--------|
| **Mini Court Width** | 180px | 150px | -17% |
| **Mini Court Height** | 360px | 300px | -17% |
| **Stats Width** | 350px | 320px | -9% |
| **Stats Height** | 230px | 210px | -9% |
| **Stats Position** | Bottom-right | Top-left, below court | Relocated |
| **Total V-Space** | ~590px | ~580px | -2% |

---

## 🎓 Perfect for Presentation!

Layout sekarang:
- ✅ **Kompak**: Mini court & stats tidak memakan banyak ruang
- ✅ **Terorganisir**: Semua overlay di satu area (kiri atas)
- ✅ **Profesional**: Alignment & spacing konsisten
- ✅ **Jelas**: Mudah dibaca, tidak mengganggu video utama

**Ready untuk demo skripsi!** 🎾✨
