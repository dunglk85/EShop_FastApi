# Product FastAPI Application

This is a FastAPI application named "Product" that utilizes SQLModel for managing product data. 

## Project Structure

```
Product
├── src
│   ├── main.py               # Entry point of the FastAPI application
│   ├── models
│   │   └── product.py        # SQLModel class for Product data model
│   ├── api
│   │   └── endpoints.py      # API endpoints for CRUD operations
│   └── db
│       └── session.py        # Database session management
├── .devcontainer
│   ├── devcontainer.json     # Development container configuration
│   └── Dockerfile            # Docker image setup for development
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd Product
   ```

2. **Open in a development container:**
   Use the provided `.devcontainer` configuration to open the project in a development container. This will ensure that all dependencies are installed and the environment is set up correctly.

3. **Install dependencies:**
   If not using the development container, install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   Start the FastAPI application by running:
   ```
   uvicorn src.main:app --reload
   ```

5. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Usage

This application allows you to perform CRUD operations on products. You can create, read, update, and delete products through the API endpoints defined in `src/api/endpoints.py`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.