import uvicorn

if __name__ == "__main__":
    print("🌐 Starting Enhanced Book Publisher...")
    print("📱 Dashboard: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(
        "book_publisher.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
