# 🔗 Python UTEC - Grupo 1: QR & Deep Link Generator

This project was developed by **Grupo 1** from UTEC as part of a Python course. It provides tools to generate QR codes, deep links, and dynamic promotional descriptions for marketing or e-commerce campaigns.

---

## 🚀 Features

- ✅ Generate product **deep links** with tracking
- ✅ Create **descriptions** from product data
- ✅ Produce **QR codes** for campaigns
- ✅ Save and organize generated outputs

---

## 🗂 Project Structure

```
├── main.py                  # Main entry point
├── generate_deeplink.py     # Deep link generation logic
├── generate_description.py  # Description creation logic from image
├── generate_qr.py           # QR code creation logic
├── generate_text.py         # Utility to assemble content
├── content/                 # Input content/data, CSV to search data
├── img/                     # Bills to scan
├── qr/                      # Stored QR data
├── requirements.txt         # Python dependencies
```

---

## 📦 Requirements

Make sure you have **Python 3.8+** installed.

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

Run the main script:

```bash
python main.py
```

You will be prompted to input or confirm product data. The tool will:

1. ✅ Generate a short deep link  
2. ✅ Create marketing text  
3. ✅ Produce and save a QR code  

---

## 📁 Output

- QR codes are saved in the `img/` directory  
- Associated data is stored in `qr/`  
- Dynamic text outputs are printed or stored depending on the function  

---

## 👨‍👩‍👧‍👦 Team Members

- Carlos Loyola [@cloyola](https://github.com/cloyola)  
- Diego Nasra  
- Ana Cecilia Zegarra 
- Brenda Zambrano  
- Mónica Saldías  
- Nicolás Nugent  
