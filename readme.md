## dim-dir

A web-based t-SNE system made for plotting loose files based on content similarity.

## Installation

1. Clone repository
2. Set up Python backend:

```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up Svelte frontend:

```bash
cd app
npm install
```

## Running Application

1. Start backend server:

```bash
python app.py
```

2. Start frontend server:

```bash
cd app
npm run dev -- --open
```

3. Navigate to `http://localhost:8080` in the browser.

4. Drag files into the `/data` directory, or run the utility to generate a variety of sample text-based files for testing:

```bash
python utils.generate_data.py
```
