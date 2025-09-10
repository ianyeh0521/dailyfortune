#!/usr/bin/env python3
"""
Web-based Daily Fortune App for testing
Simple HTTP server with HTML interface
"""

import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from fortune_data import FortuneManager
from datetime import datetime
import os

class FortuneWebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.fortune_manager = FortuneManager()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_main_page()
        elif parsed_path.path == '/api/fortune':
            self.handle_fortune_api()
        elif parsed_path.path == '/api/stats':
            self.handle_stats_api()
        elif parsed_path.path == '/api/generate':
            self.handle_generate_api()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html_content = self.get_html_page()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_fortune_api(self):
        fortune = self.fortune_manager.get_todays_fortune()
        can_generate = self.fortune_manager.can_generate_fortune()
        
        response = {
            'fortune': fortune,
            'can_generate': can_generate
        }
        
        self.send_json_response(response)
    
    def handle_stats_api(self):
        stats = self.fortune_manager.get_stats()
        self.send_json_response(stats)
    
    def handle_generate_api(self):
        try:
            if not self.fortune_manager.can_generate_fortune():
                response = {
                    'success': False,
                    'error': 'Fortune already generated for today'
                }
            else:
                fortune = self.fortune_manager.generate_fortune()
                response = {
                    'success': True,
                    'fortune': fortune
                }
        except Exception as e:
            response = {
                'success': False,
                'error': str(e)
            }
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def get_html_page(self):
        today = datetime.now().strftime("%B %d, %Y")
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔮 Daily Fortune</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        h1 {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .date {{
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .fortune-box {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        
        .fortune-text {{
            font-size: 1.4em;
            font-style: italic;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .fortune-meta {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .buttons {{
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        button {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        button:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}
        
        .stats {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        }}
        
        .loading {{
            opacity: 0.7;
        }}
        
        @media (max-width: 480px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 20px; }}
            h1 {{ font-size: 2em; }}
            .buttons {{ flex-direction: column; }}
            button {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 Daily Fortune</h1>
        <div class="date">{today}</div>
        
        <div class="fortune-box" id="fortuneBox">
            <div id="fortuneContent">Click "Get Today's Fortune" to receive your daily fortune!</div>
        </div>
        
        <div class="buttons">
            <button id="generateBtn" onclick="generateFortune()">Get Today's Fortune</button>
            <button onclick="showStats()">View Stats</button>
            <button onclick="refreshPage()">Refresh</button>
        </div>
        
        <div class="stats" id="statsBox" style="display: none;"></div>
    </div>

    <script>
        let currentFortune = null;
        let canGenerate = true;

        // Load initial state when page loads
        window.onload = function() {{
            loadCurrentFortune();
        }};

        async function loadCurrentFortune() {{
            try {{
                const response = await fetch('/api/fortune');
                const data = await response.json();
                
                currentFortune = data.fortune;
                canGenerate = data.can_generate;
                
                if (currentFortune) {{
                    displayFortune(currentFortune);
                    document.getElementById('generateBtn').textContent = 'Fortune Already Generated';
                    document.getElementById('generateBtn').disabled = true;
                }} else if (!canGenerate) {{
                    document.getElementById('fortuneContent').innerHTML = 
                        "You've already received your fortune for today. Come back tomorrow!";
                    document.getElementById('generateBtn').textContent = 'Come Back Tomorrow';
                    document.getElementById('generateBtn').disabled = true;
                }}
            }} catch (error) {{
                console.error('Error loading fortune:', error);
            }}
        }}

        async function generateFortune() {{
            if (!canGenerate) return;
            
            const btn = document.getElementById('generateBtn');
            const originalText = btn.textContent;
            btn.textContent = 'Generating...';
            btn.disabled = true;
            
            try {{
                const response = await fetch('/api/generate');
                const data = await response.json();
                
                if (data.success) {{
                    currentFortune = data.fortune;
                    displayFortune(currentFortune);
                    btn.textContent = 'Fortune Generated!';
                    canGenerate = false;
                    
                    // Show success message
                    alert(`Your fortune for today:\\n\\n"${{data.fortune.text}}"`);
                }} else {{
                    alert('Error: ' + data.error);
                    btn.textContent = originalText;
                    btn.disabled = false;
                }}
            }} catch (error) {{
                console.error('Error generating fortune:', error);
                alert('Failed to generate fortune. Please try again.');
                btn.textContent = originalText;
                btn.disabled = false;
            }}
        }}

        function displayFortune(fortune) {{
            const timestamp = fortune.generated_at ? 
                new Date(fortune.generated_at).toLocaleTimeString() : '';
            
            document.getElementById('fortuneContent').innerHTML = `
                <div class="fortune-text">"${{fortune.text}}"</div>
                <div class="fortune-meta">
                    Category: ${{fortune.category.charAt(0).toUpperCase() + fortune.category.slice(1)}}
                    ${{timestamp ? '<br>Generated at: ' + timestamp : ''}}
                </div>
            `;
        }}

        async function showStats() {{
            try {{
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                const statsBox = document.getElementById('statsBox');
                
                if (stats.total_fortunes === 0) {{
                    statsBox.innerHTML = `
                        <h3>📊 Statistics</h3>
                        <p>No fortunes generated yet!<br>Get your first fortune to see statistics.</p>
                    `;
                }} else {{
                    statsBox.innerHTML = `
                        <h3>📊 Your Fortune Statistics</h3>
                        <p><strong>Total Fortunes:</strong> ${{stats.total_fortunes}}</p>
                        <p><strong>Current Streak:</strong> ${{stats.streak}} days</p>
                        <p><strong>First Fortune:</strong> ${{stats.first_fortune}}</p>
                        <p><strong>Latest Fortune:</strong> ${{stats.last_fortune}}</p>
                        <p><em>Keep up the great work! Come back daily to maintain your streak.</em></p>
                    `;
                }}
                
                statsBox.style.display = statsBox.style.display === 'none' ? 'block' : 'none';
            }} catch (error) {{
                console.error('Error loading stats:', error);
                alert('Failed to load statistics. Please try again.');
            }}
        }}

        function refreshPage() {{
            location.reload();
        }}
    </script>
</body>
</html>
"""

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FortuneWebHandler)
    
    print(f"🔮 Daily Fortune Web App")
    print(f"Server running at: http://localhost:{port}")
    print(f"Opening browser...")
    
    # Open browser automatically
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()