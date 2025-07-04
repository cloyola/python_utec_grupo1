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

## 🔧 Setting Up a Virtual Environment in VS Code (Command Prompt)

Follow these steps to set up and activate a virtual environment in your project using Visual Studio Code with the `Command Prompt` terminal:

### 1. Open the terminal in VS Code
- Open VS Code.
- Use the shortcut: `Ctrl + ` (backtick) or go to **View > Terminal**.
- Make sure you are using `Command Prompt` as the terminal. You can switch terminals from the dropdown menu in the top-right corner of the terminal panel.

### 2. Validate Python installation
Make sure you have **Python 3.8+** installed.

```bash
python
```

### 3. Create the virtual environment
Run the following command in the root of your project:

```bash
python -m venv venv
```
This will create a folder named venv containing your virtual environment.


### 4. Activate the virtual environment
In Command Prompt, run:

```bash
venv\Scripts\activate
```

### 5. Install dependencies
After activation, install the required packages in the next step.

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

Run the main script:

```bash
streamlit run ui.py
```

You will be prompted to input or confirm product data. The tool will:

1. ✅ Generate a short deep link  
2. ✅ Create marketing text  
3. ✅ Produce and save a QR code  

---

## 📁 Output

- QR code is saved in the `qr/` directory  
- Log stored in `yape_scan.log`
- Dynamic text outputs are printed or stored depending on the function  

---

## 👨‍👩‍👧‍👦 Team Members

- Carlos Loyola [@cloyola](https://github.com/cloyola)  
- Diego Nasra  
- Ana Cecilia Zegarra 
- Brenda Zambrano  
- Mónica Saldías  
- Nicolás Nugent  
