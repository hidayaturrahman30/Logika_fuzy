-- =====================================================
-- PRAKTIKUM LOGIKA FUZZY — MODUL 3
-- Gabungan Semua SQL
-- =====================================================

-- 1. Buat Database
CREATE DATABASE IF NOT EXISTS db_logika_fuzzy_tugas2;
USE db_logika_fuzzy_tugas2;

-- 2. Buat Tabel
CREATE TABLE IF NOT EXISTS usia_remaja (
    pengenal INT PRIMARY KEY AUTO_INCREMENT,
    usia_min INT NOT NULL,
    usia_maks INT NOT NULL,
    nilai_fuzzy VARCHAR(100) NOT NULL
);

-- 3. Masukkan Data Interval
INSERT INTO usia_remaja (usia_min, usia_maks, nilai_fuzzy) VALUES
(0, 10, '0'),
(10, 15, 'fungsi_remaja_naik'),
(15, 20, 'fungsi_remaja_turun'),
(20, 150, '0');

-- 4. Cek Data
SELECT * FROM usia_remaja;

-- 5. Cari Fungsi untuk Nilai Tertentu (contoh x = 17)
SELECT usia_min, usia_maks, nilai_fuzzy
FROM usia_remaja
WHERE 17 >= usia_min 
  AND 17 <= usia_maks;
