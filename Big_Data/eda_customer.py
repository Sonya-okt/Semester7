# -*- coding: utf-8 -*-


# Mengimpor pustaka yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Mengimpor data dari file CSV
file_path = 'telecustomer.csv'
data = pd.read_csv(file_path)

# 2. Pembersihan Data
# Menghilangkan kolom dengan banyak nilai NaN dan kolom 'customerID'
data_cleaned = data.dropna(axis=1, how='all')  # Menghilangkan kolom dengan semua nilai NaN
data_cleaned = data_cleaned.drop(['customerID'], axis=1)  # 'customerID' tidak relevan untuk analisis

# Konversi 'TotalCharges' dari tipe objek ke numerik
# Menghilangkan baris dengan nilai NaN di 'TotalCharges'
data_cleaned['TotalCharges'] = pd.to_numeric(data_cleaned['TotalCharges'], errors='coerce')
data_cleaned = data_cleaned.dropna(subset=['TotalCharges'])

# 3. Analisis Eksploratif Data (EDA)
# Statistik Deskriptif
desc_stats = data_cleaned.describe(include='all')

# Visualisasi
# Distribusi variabel target 'Churn'
plt.figure(figsize=(6,4))
sns.countplot(x='Churn', data=data_cleaned)
plt.title('Distribution of Churn')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.tight_layout()

# Korelasi antara fitur numerik dan 'Churn'
plt.figure(figsize=(8, 6))
sns.heatmap(data_cleaned.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.tight_layout()

# Distribusi 'MonthlyCharges' berdasarkan 'Churn'  membandingkan  antara pelanggan yang churn dan yang tidak.
plt.figure(figsize=(6,4))
sns.boxplot(x='Churn', y='MonthlyCharges', data=data_cleaned)
plt.title('Monthly Charges by Churn')
plt.xlabel('Churn')
plt.ylabel('Monthly Charges')
plt.tight_layout()

# Distribusi 'tenure' berdasarkan 'Churn'
plt.figure(figsize=(6,4))
sns.boxplot(x='Churn', y='tenure', data=data_cleaned)
plt.title('Tenure by Churn')
plt.xlabel('Churn')
plt.ylabel('Tenure')
plt.tight_layout()

desc_stats

"""
Pembersihan Data:

    Menghilangkan kolom yang tidak berguna (semua nilai NaN) dan kolom 'customerID'.
    Mengkonversi 'TotalCharges' ke tipe numerik dan menghilangkan baris dengan nilai NaN pada kolom ini.

EDA - Statistik Deskriptif: Menghasilkan statistik deskriptif untuk setiap kolom.
EDA - Visualisasi:

    Membuat plot untuk distribusi churn.
    Membuat heatmap untuk melihat korelasi antar fitur, terutama terhadap 'Churn'.
    Membuat boxplot untuk membandingkan 'MonthlyCharges' dan 'tenure' antara pelanggan yang churn dan yang tidak.

Menampilkan Plot: Menampilkan semua plot yang telah dibuat.
Mengembalikan Statistik Deskriptif: Menampilkan ringkasan statistik dari dataset.
"""
