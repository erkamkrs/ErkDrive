# 🚀 ErkDrive

ErkDrive is a full-stack cloud file management application (Google Drive clone) built using:

- 🔧 **Frontend**: SvelteKit (TypeScript, TailwindCSS)
- ⚙️ **Backend**: FastAPI
- 🗄️ **Storage**: MinIO (S3-compatible object storage)
- 🧠 **Database**: MongoDB
- 🔐 **Auth**: JWT (JSON Web Token)

---

## ✨ Features

- 🔐 User authentication (register & login with JWT)
- 📂 Folder creation and file management
- 📤 Upload files to folders
- 📥 Download files
- ✏️ Rename files
- 🗑️ Delete files
- 🎯 Protected routes with redirect if not logged in

---

## 

<details>
<summary>Click to view</summary>

![Login Page](https://via.placeholder.com/600x300?text=Login+Page)
![File Browser](https://via.placeholder.com/600x300?text=File+Browser)

</details>

---

## 🏗️ Project Structure

```bash
.
├── frontend/         # SvelteKit app
│   ├── src/routes/
│   └── src/lib/stores/
├── backend/          # FastAPI app
│   └── app/
│       ├── auth.py
│       └── main.py
└── .env              # Environment variables
