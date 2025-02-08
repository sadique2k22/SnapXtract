# 📸 Snapchat Media Organizer

A Python script to automatically organize Snapchat media files based on their creation time. This script categorizes images, videos, and voice notes while preserving their original quality.

**🚨 This script only works on rooted Android devices.**


---

## 🛠Requirements

### 1️⃣Required Libraries

This script relies on the following Python libraries:

**Pillow** – For image processing

**tqdm** – For progress visualization


### 2️⃣Required Packages

Ensure your Android device has these packages installed:

**Git** – Required to clone this repository

**Python** – Required to run the script

**FFmpeg** – Used to process media files

**Tsu** – Grants root access



---

## 🔧Installation

**Step 1**: Install Required Packages

Run the following command in Termux to install all required packages:

```bash
pkg install git python ffmpeg tsu -y
```
**Step 2**: Clone the Repository

```bash
git clone https://github.com/sadique2k22/SnapXtract.git
cd SnapXtract
```
**Step 3**: Install Required Python Libraries

```bash
pip install pillow tqdm
```

---

## 🚀 Usage

1. Navigate to the script’s directory (if not already there):

```bash
cd /path/to/the/script
```

2. Run the script with sudo:

```bash
sudo python main.py <option> [--date dd,mm,yyyy]
```


**Options**:

onehour → Organizes media created in the last 1 hour

today → Organizes media created today

date → Organizes media from a specific date


**Example**:
To organize today's media:

```bash
sudo python main.py today
```
To organize media from 5th February 2025:

```bash
sudo python main.py date --date 05,02,2025
```

---

### 📂 Output Structure

The organized files will be saved in:
📁 /storage/emulated/0/snap/.<date>/

📂 images/ → Saves Snapchat images

📂 videos/ → Saves Snapchat videos

📂 audios/ → Saves Snapchat voice notes

📂 empty/ → Placeholder directory



---

### ⚠️ Disclaimer

**This script is for educational purposes only. The author is not responsible for any misuse.**
