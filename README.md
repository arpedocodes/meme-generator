# 🎭 Meme Generator

Upload a photo, draw text boxes wherever you want the captions, and let AI write the jokes. Meme Generator turns any image into four ready-to-share meme variations in seconds.

---

## 🌟 Highlights

* 🖼️ Interactive canvas editor — upload an image and place caption boxes exactly where you want them
* 🤖 AI-generated captions tailored to your image
* 🎯 Custom rectangle placement, resizing, and rotation for full creative control
* 🧠 Smart text-fitting logic that drops AI-generated text neatly into your chosen regions
* 🎲 Generates 4 unique meme variations per submission
* ⚡ Simple, fast frontend-to-backend pipeline

---

## ℹ️ Overview

Meme Generator is a full-stack app that combines manual image annotation with AI-powered text generation. Instead of typing your own captions, you mark *where* the text should go — and the AI figures out *what* it should say.

The workflow is simple:

1. **Upload** an image on the frontend.
2. **Annotate** it by drawing one or more rectangles over the areas where you want captions, then position, resize, or rotate them as needed.
3. **Submit** — the annotated image (along with rectangle coordinates) is sent to the backend.
4. The backend forwards the image to an **AI model**, which generates caption text based on the image content.
5. Backend logic places the generated text inside your defined rectangles, producing **4 distinct meme variations**.
6. The finished memes are sent back and displayed on the frontend, ready to download.

---

## 🎥 Demo

A short walkthrough of the upload → annotate → generate → download flow.

**Watch the demo:**


https://github.com/user-attachments/assets/d37229bc-a6f0-4cb4-8f92-e45850b0d2e0


---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                         FRONTEND                          │
│                                                           │
│   Upload Image → Draw/Position Rectangles → Submit        │
└───────────────────────────┬───────────────────────────────┘
                            │  (image + rectangle coordinates)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                          BACKEND                           │
│                                                           │
│   server.py                                               │
│       │                                                   │
│       ▼                                                   │
│   encode_image.py  ──►  AI Model (caption generation)     │
│       │                                                   │
│       ▼                                                   │
│   memegenerator.py + place_text.py                         │
│       (places generated text into rectangle regions)      │
│       │                                                   │
│       ▼                                                   │
│   4 Meme Images (output/)                                  │
└───────────────────────────┬───────────────────────────────┘
                            │  (4 image paths/URLs)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                         FRONTEND                           │
│              Displays & lets you download memes            │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
backend/
├── server.py                      # Entry point — handles incoming requests
├── requirements.txt               # Python dependencies
├── Procfile                        # Process file for deployment (e.g. Railway/Heroku)
├── .env                             # Environment variables (API keys, config)
│
└── logic/
    ├── components/
    │   ├── jsonconverter.py        # Converts data to/from JSON for processing
    │   └── memegenerator.py        # Core meme generation logic
    │
    ├── config/
    │   └── prompt.json              # AI prompt templates/config
    │
    ├── server/
    │   ├── data/                    # Stores uploaded/incoming images
    │   └── output/                  # Stores generated meme images
    │
    ├── main.py                      # Core processing pipeline orchestration
    │
    └── utils/
        ├── encode_image.py          # Encodes images for sending to the AI model
        └── place_text.py             # Places generated captions into the rectangle regions
```

---

## ⚙️ How It Works (Step by Step)

1. **Frontend** — User uploads an image and draws rectangles to mark caption zones.
2. **Submission** — The annotated image + rectangle coordinates (position, size, angle) are POSTed to the backend.
3. **`server.py`** — Receives the request and routes it into the processing pipeline.
4. **`encode_image.py`** — Encodes the image into a format suitable for the AI model.
5. **AI Model** — Analyzes the image and generates caption text.
6. **`jsonconverter.py`** — Converts AI responses and rectangle data into a usable structured format.
7. **`memegenerator.py`** — Orchestrates the meme creation process.
8. **`place_text.py`** — Renders the generated captions inside the specified rectangle areas, accounting for font size, wrapping, and positioning.
9. **Output** — 4 unique meme variations are saved to `output/` and their paths are returned to the frontend.
10. **Frontend** — Displays the 4 memes for preview and download.

---

## ⬇️ Installation

```bash
git clone https://github.com/arpedocodes/meme-generator.git
cd meme-generator/backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
GITHUB_TOKEN=your_github_token
HF_TOKEN=your_huggingface_token
```

> **Note:** A `GITHUB_TOKEN` and a Hugging Face `HF_TOKEN` are required for AI caption generation to work — the app won't be able to call the model without them.

---

## ▶️ Running the Project

### 1. Backend

```bash
cd backend
uvicorn server:app --reload
```

The backend will be running at:

```
http://127.0.0.1:8000
```

### 2. Frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

The frontend will be running at:

```
http://localhost:3000
```

> Make sure the backend is running **before** starting the frontend, since the frontend submits images directly to the backend API.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React, Fabric.js (canvas annotation), Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| AI | Hugging Face model(s) for caption generation (image-to-text) |
| Image Processing | PIL / image manipulation utilities |
| Deployment | Procfile-based (Railway / Heroku compatible) |

---

## 🚀 API Overview

### `POST /meme`

Accepts the annotated image, original image, and rectangle data, and returns 4 generated meme image paths.

**Request (multipart/form-data):**

| Field | Type | Description |
|---|---|---|
| `annotatedImage` | file | The image with rectangle overlays |
| `originalImage` | file | The original, unmodified image |
| `rectangleData` | string (JSON) | Array of rectangle coordinates, size, and angle |

**Response:**
```json
{
  "data": {
    "images": [
      "output/meme1.png",
      "output/meme2.png",
      "output/meme3.png",
      "output/meme4.png"
    ]
  }
}
```

---

## 📌 Roadmap

- [ ] Support custom fonts and text styling per rectangle
- [ ] Allow users to regenerate captions without re-uploading
- [ ] Add caption tone/style selector (sarcastic, wholesome, dark humor, etc.)
- [ ] Persistent gallery of previously generated memes
- [ ] Rate limiting and caching for AI requests

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
