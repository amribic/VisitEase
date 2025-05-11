# VisitEase

## CDTM HACKS Project
- **Team ID**: 1613
- **Team Name**: CDTM Hacks @ TUM
- **Project Name**: VisitEase

## Links
- **Demo (Patient-Side)**: [https://visit-ease.vercel.app/](https://visit-ease.vercel.app/)
- **Demo (Medical-Staff-Side)**: [https://visit-ease-doctor.vercel.app/](https://visit-ease-doctor.vercel.app/)

> Note: Due to limited hosting resources, the demo links may occasionally be unavailable. Below are instructions for running the application locally.

## One-Sentence Pitch
A structurization engine for complex, incomplete, and variable data.

## What Is VisitEase?

Planning to visit a healthcare professional? Patients often forget to bring relevant medical records such as medical history, recent lab results, and specific medication names. This significantly increases the complexity for doctors to provide effective care. VisitEase solves this problem by enabling better healthcare for patients of all technical backgrounds through easy and dynamic data uploads. No more forgotten documents, confusion, or unnecessary waiting. Doctors benefit from a structured dashboard with dynamic interactions powered by LLMs, allowing them to view patient data efficiently. Through technical innovation, VisitEase is shaping the future of patient visits and establishing itself as a cornerstone in medical technology.

## How We Built It

VisitEase's infrastructure consists of two main components:

### Backend
- Flask server handling multiple POST and GET requests
- User authentication (login/signup)
- Image upload and PDF conversion
- Integration with Gemini API for data analysis
- Firestore database integration

### Frontend
- Two separate responsive frontends:
  - **VisitEase**: Patient-facing app for data upload (Svelte)
  - **VisitEaseDoc**: Doctor's dashboard for structured data viewing (React)
- Hosted on Vercel (frontend) and Render (backend)

## Challenges Faced

1. **Platform Decision**: After consulting with the avi team, we decided to build a responsive web app.
2. **Audio Integration**: Implementing a talking agent presented significant challenges due to the complexity of sharing audio between frontend and backend. We overcame this by:
   - Using OpenAI API for audio processing
   - Generating text responses
   - Converting responses to audio using Gemini text-to-speech API

## Competition Categories

### Celonis - Best use of AI to improve processes
VisitEase leverages multiple AI models:
- Basic text generation
- PDF analysis using Gemini-2.0-flash
- Complex voice agent using OpenAI API and Gemini speech-to-text API
- Streamlined data upload process with minimal user effort

### Tanso - Why Not? Biggest Creative Risk
We took a significant creative risk by developing a working speaking agent to enhance patient data:
- Added multi-modal dimension to data capture
- Captured thoughts and feelings beyond traditional medical data
- Successfully implemented voice-based insights despite technical challenges

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Google Cloud account (for Gemini API and Firestore)
- OpenAI API key

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/amribic/VisitEase.git
   cd VisitEase
   ```

2. Set up the Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys

4. Start the Flask server:
   ```bash
   python main.py
   ```

### Frontend Setup (Patient App)
1. Navigate to the patient frontend directory:
   ```bash
   cd VisitEase/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```
   VITE_API_URL=http://localhost:8080
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Frontend Setup (Doctor App)
1. Navigate to the doctor frontend directory:
   ```bash
   cd VisitEaseDoctor/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```
   VITE_API_URL=http://localhost:8080
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Contributing

We welcome contributions to VisitEase! Here's how you can help:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure your code follows our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don't hold you liable.