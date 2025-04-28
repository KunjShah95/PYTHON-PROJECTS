# Desk Cleanup Script

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

🧹 This Python script helps you organize your desktop (or any folder) by automatically sorting files into categorized folders. It also clears temporary files from your system.

## Features

-   **File Categorization:** Sorts files into folders like Images, Documents, Videos, Music, Archives, Scripts, and Others.
-   **Customizable:** Easily add or modify file type categories and their associated extensions.
-   **Temporary File Cleanup:** Clears temporary files from the system's temporary folder.
-   **Error Handling:** Gracefully handles errors during file deletion.

## How to Use

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    ```
2.  **Modify the `folder_to_clean` Variable:**
    -   Open `MAIN.PY` and change the `folder_to_clean` variable to the path of the folder you want to organize.
    ```python
    folder_to_clean = r'C:\Users\YourUsername\Desktop'  # <-- Change this to your desired folder
    ```
3.  **Run the Script:**
    ```bash
    python MAIN.PY
    