# How To run

```
https://github.com/GagukPurnotow/Meghamol
```
```
cd Meghamol
```

Pakai virtual environment biar tiap project nggak saling bentrok dependensinya:
```
python -m venv env
source env/bin/activate  # kalau pakai Mac/Linux
.\env\Scripts\activate   # kalau pakai Windows
```

Setelah itu install ulang package

```
pip3 install -r requirements.txt
```
```
pip3 install web3
```
```
pip3 install seleniumbase
```

# Jika terjadi error

```
pip install --upgrade pip setuptools
pip install 'urllib3<2'
```
seleniumbase versi sekarang kamu pakai (4.37.2) hanya kompatibel dengan urllib3<2.
Jadi, aman gunakan urllib3==1.26.20 atau upgrade seleniumbase juga kalau mau ke urllib3 v2.

Cek dependency lainnya: Untuk pastikan environment bersih, kamu bisa jalankan:

```
pip check
```
