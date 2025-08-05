"""
Enhanced Book Publisher API with Interactive Dashboard
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import uuid
from datetime import datetime
from typing import Optional

app = FastAPI(title="Automated Book Publisher", version="1.0.0")

# Store workflows in memory (for demo)
workflows = {}

class WorkflowRequest(BaseModel):
    source_url: Optional[str] = None
    search_query: Optional[str] = None
    enhancement_type: str = "creative_rewrite"
    target_audience: str = "general"
    include_audio: bool = True
    require_human_approval: bool = False

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Automated Book Publisher</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; color: #34495e; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .status { margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; display: none; }
            .example { background: #e8f4fd; padding: 10px; border-radius: 5px; margin-top: 5px; font-size: 14px; }
            .checkbox-group { display: flex; align-items: center; gap: 10px; }
            .checkbox-group input { width: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Automated Book Publisher</h1>
            <p style="text-align: center; color: #7f8c8d;">Transform any web content into an enhanced, publishable book with AI</p>
            
            <form id="workflowForm">
                <div class="form-group">
                    <label for="sourceUrl">Source URL (optional):</label>
                    <input type="url" id="sourceUrl" placeholder="https://en.wikisource.org/wiki/Frankenstein/Chapter_1">
                    <div class="example">
                        <strong>Examples:</strong><br>
                        • https://en.wikisource.org/wiki/Frankenstein/Chapter_1<br>
                        • https://en.wikisource.org/wiki/Alice%27s_Adventures_in_Wonderland/Chapter_1<br>
                        • Any public web page with text content
                    </div>
                </div>

                <div class="form-group">
                    <label for="searchQuery">Or Search Query (optional):</label>
                    <input type="text" id="searchQuery" placeholder="The Gates of Morning Chapter 1">
                    <div class="example">
                        <strong>Examples:</strong> "Alice in Wonderland", "Frankenstein Chapter 1", "Shakespeare Hamlet"
                    </div>
                </div>

                <div class="form-group">
                    <label for="enhancementType">Enhancement Type:</label>
                    <select id="enhancementType">
                        <option value="creative_rewrite">Creative Rewrite - More engaging and readable</option>
                        <option value="academic_style">Academic Style - Formal, scholarly tone</option>
                        <option value="narrative_style">Narrative Style - Story-like presentation</option>
                        <option value="chapter_expansion">Chapter Expansion - Add more detail and depth</option>
                        <option value="content_summarization">Content Summarization - Concise key points</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="targetAudience">Target Audience:</label>
                    <select id="targetAudience">
                        <option value="general">General Public</option>
                        <option value="academic">Academic/Scholarly</option>
                        <option value="children">Children/Young Adult</option>
                        <option value="professional">Professional/Business</option>
                    </select>
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="includeAudio" checked>
                        <label for="includeAudio">Generate Audio Book Version</label>
                    </div>
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="requireApproval">
                        <label for="requireApproval">Require Human Approval Before Publishing</label>
                    </div>
                </div>

                <div class="form-group">
                    <button type="button" onclick="startWorkflow()">🚀 Start Book Publishing Workflow</button>
                </div>
            </form>

            <div id="status" class="status">
                <h3>Workflow Status</h3>
                <div id="statusContent">No active workflow</div>
                <button type="button" onclick="checkStatus()" style="margin-top: 10px;">Refresh Status</button>
            </div>

            <div style="margin-top: 30px; text-align: center; color: #7f8c8d;">
                <p><a href="/docs" style="color: #3498db;">📚 View API Documentation</a> | 
                   <a href="/health" style="color: #3498db;">💚 System Health</a></p>
            </div>
        </div>

        <script>
            let currentSessionId = null;

            async function startWorkflow() {
                const sourceUrl = document.getElementById('sourceUrl').value;
                const searchQuery = document.getElementById('searchQuery').value;
                const enhancementType = document.getElementById('enhancementType').value;
                const targetAudience = document.getElementById('targetAudience').value;
                const includeAudio = document.getElementById('includeAudio').checked;
                const requireApproval = document.getElementById('requireApproval').checked;

                if (!sourceUrl && !searchQuery) {
                    alert('Please provide either a source URL or search query');
                    return;
                }

                const request = {
                    source_url: sourceUrl || null,
                    search_query: searchQuery || null,
                    enhancement_type: enhancementType,
                    target_audience: targetAudience,
                    include_audio: includeAudio,
                    require_human_approval: requireApproval
                };

                try {
                    document.getElementById('statusContent').innerHTML = '🔄 Starting workflow...';
                    document.getElementById('status').style.display = 'block';

                    const response = await fetch('/api/workflow/start', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(request)
                    });

                    const result = await response.json();

                    if (result.session_id) {
                        currentSessionId = result.session_id;
                        document.getElementById('statusContent').innerHTML = 
                            `<strong>✅ Workflow Started!</strong><br>
                             Session ID: ${result.session_id}<br>
                             Status: ${result.status}<br>
                             <em>Processing your request...</em>`;
                        
                        // Auto-refresh status every 5 seconds
                        setTimeout(checkStatus, 5000);
                    } else {
                        document.getElementById('statusContent').innerHTML = 
                            `<strong>❌ Error:</strong> ${result.detail || 'Unknown error'}`;
                    }
                } catch (error) {
                    document.getElementById('statusContent').innerHTML = 
                        `<strong>❌ Error:</strong> ${error.message}`;
                }
            }

            async function checkStatus() {
                if (!currentSessionId) {
                    document.getElementById('statusContent').innerHTML = 'No active workflow';
                    return;
                }

                try {
                    const response = await fetch(`/api/workflow/status/${currentSessionId}`);
                    const status = await response.json();

                    document.getElementById('statusContent').innerHTML = 
                        `<strong>Session:</strong> ${status.session_id}<br>
                         <strong>Status:</strong> ${status.status}<br>
                         <strong>Stage:</strong> ${status.stage}<br>
                         <strong>Progress:</strong> ${status.progress}%<br>
                         <strong>Last Updated:</strong> ${new Date(status.updated_at).toLocaleString()}`;

                    // Continue checking if not completed
                    if (status.status === 'processing') {
                        setTimeout(checkStatus, 5000);
                    }
                         
                } catch (error) {
                    document.getElementById('statusContent').innerHTML = 
                        `<strong>❌ Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/workflow/start")
async def start_workflow(request: WorkflowRequest):
    """Start a new book publishing workflow"""
    session_id = str(uuid.uuid4())
    
    # Simulate workflow creation
    workflow = {
        "session_id": session_id,
        "status": "processing",
        "stage": "scraping",
        "progress": 10,
        "source_url": request.source_url,
        "search_query": request.search_query,
        "enhancement_type": request.enhancement_type,
        "target_audience": request.target_audience,
        "include_audio": request.include_audio,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    workflows[session_id] = workflow
    
    return {
        "session_id": session_id,
        "status": "started",
        "message": "Workflow initiated successfully"
    }

@app.get("/api/workflow/status/{session_id}")
async def get_workflow_status(session_id: str):
    """Get workflow status"""
    if session_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows[session_id]
    
    # Simulate progress
    if workflow["status"] == "processing":
        workflow["progress"] = min(workflow["progress"] + 15, 90)
        workflow["updated_at"] = datetime.now().isoformat()
        
        # Simulate completion
        if workflow["progress"] >= 90:
            workflow["status"] = "completed"
            workflow["stage"] = "publication"
            workflow["progress"] = 100
    
    return workflow

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "book-publisher",
        "timestamp": datetime.now().isoformat(),
        "active_workflows": len(workflows)
    }

if __name__ == "__main__":
    print("🌐 Starting Enhanced Book Publisher...")
    print("📱 Dashboard: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
